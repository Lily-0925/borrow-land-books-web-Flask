from flask_sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy import Column, SmallInteger

class Query(BaseQuery):
    def filter_by(self, **kwargs):
        kwargs["status"] = 1
        return super(Query, self).filter_by(**kwargs)

db = SQLAlchemy(query_class=Query)

class Base(db.Model):
    __abstract__ = True
    status = Column(SmallInteger, default = 1)

    def set_sttrs(self, dic):
        for key, value in dic.items():
            if hasattr(self, key) and key != "id":
                setattr(self,key,value)