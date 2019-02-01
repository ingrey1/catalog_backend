from sqlalchemy import create_engine, Table, Column, Integer, String, Boolean, Sequence, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime


# create core interface to database - replace this with your own: 
engine = create_engine('postgresql://postgres:tyrion1234@localhost:5433/postgres', echo=True)


# keeps track of all the databases classes / tables
Base = declarative_base()




# establish many-to-many relationship table between items and categories
item_category_table = Table('item_category_association', Base.metadata,
    Column('categories_id', Integer, ForeignKey('categories.id') ),
    Column('items_id', Integer, ForeignKey('items.id')),
    Column('updated_on', DateTime, onupdate=datetime.datetime.now))


class Category(Base):
    __tablename__ = 'categories'
    # table column definitions
    id = Column(Integer, Sequence('category_id_seq'),  primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    items = relationship("Item", secondary=item_category_table, back_populates='categories')


    def __repr__(self):
        return "<Category(id=%s, name=%s)>" % (self.id, self.name)


# Item class metadata
class Item(Base):
    __tablename__ = 'items'
    # table column definitions
    id = Column(Integer, Sequence('item_id_seq'), primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String, server_default="This item has no description")
    categories = relationship("Category", secondary=item_category_table, back_populates='items')
     

    def __repr__(self):
        return "<Item(id=%s, name=%s, description=%s)>" % (self.id, self.name, self.description)

# User class metadata
class User(Base):
    __tablename__ = 'users'
    # table column definitions
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    full_name = Column(String(255), nullable=False)
    logged_in = Column(Boolean, nullable=False, default=False)
    latest_session_exp = Column(DateTime)
     

    def __repr__(self):
        return "<Item(id=%s, full_name=%s, logged_in=%s)>" % (self.id, self.full_name, self.logged_in)




# add schema to database 




if __name__ == 'main':
    Base.metadata.create_all(engine)






