from app.models.base import db, Base
from sqlalchemy import Column, Integer, String,Boolean,Float, ForeignKey,desc,func
from sqlalchemy.orm import relationship
from app.spider.YushuBook import YuShuBook



class Wish(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = relationship("User")
    uid = Column(Integer, ForeignKey("user.id"))
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)

    @classmethod
    def get_user_wish(cls, uid):
        my_wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(desc(Wish.id)).all()
        return my_wishes

    @classmethod
    def get_gift_count(cls, isbn_list):
        from .gift import Gift
        counts = db.session.query(func.count(Gift.id), Gift.isbn).filter(Gift.launched == False,
                                                                         Gift.isbn.in_(isbn_list),
                                                                         Gift.status == 1).group_by(Gift.isbn).all()

        counts = {w[1]: w[0] for w in counts}  # {"23424563366":1, "32453464342":2}
        return counts
        # [(1,"23424563366"),(2,"32453464342")]

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_for_isbn(self.isbn)
        return yushu_book.first