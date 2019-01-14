from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# core interface to database
engine = create_engine('sqlite:///:memory:', echo=True)


# keeps track of all the databases classes / tables
Base = declarative_base()

# category table class metadata

class Category(Base):
    __tablename__ = 'categories'
    # table column definitions
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<Category(id=%s, name=%s)>" % (self.id,jk self.name)


print(Category.__table__)





