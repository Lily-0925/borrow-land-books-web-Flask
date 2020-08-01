from app.models.base import db, Base
from sqlalchemy import Column, Integer, String,Boolean,Float, ForeignKey,desc,func
from sqlalchemy.orm import relationship
from flask import current_app
from app.spider.YushuBook import YuShuBook


class Gift(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = relationship("User")
    uid = Column(Integer, ForeignKey("user.id"))
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)

    def is_yourself_gift(self, uid):
        return True if self.uid == uid else False

    @classmethod
    def get_user_gift(cls, uid):
        my_gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(desc(Gift.id)).all()
        return my_gifts
    @classmethod
    def get_wish_count(cls, isbn_list):
        from .wish import Wish
        counts = db.session.query(func.count(Wish.id),Wish.isbn).filter(Wish.launched == False,
                                                                        Wish.isbn.in_(isbn_list),
                                                                        Wish.status == 1).group_by(Wish.isbn).all()

        counts = {w[1]: w[0] for w in counts}  #{"23424563366":1, "32453464342":2}
        return counts
        #[(1,"23424563366"),(2,"32453464342")]

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_for_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def recent(cls):
        recent_gifts = Gift.query.filter_by(launched=False).group_by(Gift.isbn).order_by(desc(Gift.id)).limit(
            current_app.config["RECENT_BOOK_COUNT"]).distinct().all()
        return recent_gifts