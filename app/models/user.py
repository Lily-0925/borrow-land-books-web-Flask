from app.models.base import db, Base
from sqlalchemy import Column, Integer, String,Boolean,Float
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from app import login_manager
from app.libs.helper_function import isbn_or_key
from app.spider.YushuBook import YuShuBook
from app.models.wish import Wish
from app.models.gift import Gift
from itsdangerous import JSONWebSignatureSerializer as Serializer
from flask import current_app
from app.libs.enums import PendingStatus
from app.models.drift import Drift

class User(UserMixin, Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(24), nullable=False)
    phonenumber = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    _password = Column("password", String(128), nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property
    def summary(self):
        return {"id":self.id, "nickname": self.nickname, "beans":self.beans,"email":self.email,
                "send_receive":str(self.send_counter)+"/"+str(self.receive_counter)}


    def can_send_drift(self):
        if self.beans < 1:
            return False
        current_sent_gift = Gift.query.filter_by(launched=True, uid=self.id).count()
        current_ask_wish = Drift.query.filter_by(requester_id=self.id, pending=PendingStatus.Success).count()
        return current_sent_gift//2 <= current_ask_wish



    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    def can_save_to_list(self, isbn):
        if isbn_or_key(isbn) != "isbn":
            return False
        else:
            yu_shubook = YuShuBook()
            yu_shubook.search_for_isbn(isbn)
            if not yu_shubook.first:
                return False
            gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
            wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
            if not gifting and not wishing:
                return True
            else:
                return False

    def generate_token(self, time=600):
        s = Serializer(current_app.config["SECRET_KEY"], time)
        return s.dumps({"id": self.id}).decode("utf-8")

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"))
        except:
            return False
        uid = data.get("id")
        try:
            user = User.query.get(uid)
            user.password = new_password
            db.session.add(user)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))