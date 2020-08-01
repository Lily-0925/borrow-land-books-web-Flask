
from sqlalchemy import Column, String, Integer, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.libs.enums import PendingStatus

class Drift(Base):

    id = Column(Integer, primary_key=True)
    recipient_name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))
    # requester_id = Column(Integer, ForeignKey('user.id'))
    # requester = relationship('User')
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifter_nickname = Column(String(20))
    # gift_id = Column(Integer, ForeignKey('gift.id'))
    # gift = relationship('Gift')
    _pending = Column("pending", SmallInteger, default=1)

    @property
    def pending(self):
        return PendingStatus(self._pending)

    @pending.setter
    def pending(self, status):
        self._pending = status.value




