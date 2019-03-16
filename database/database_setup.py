from sqlalchemy import create_engine, Table, Column, Integer, String, Boolean, Sequence, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
from database_configuration import sql_db_interface


# create core interface to db - edit the value of sql_db_interface in the database_configuration file
engine = create_engine(sql_db_interface, echo=True)


# keeps track of all the databases classes / tables
Base = declarative_base()




# establish many-to-many relationship table between items and categories
"""item_category_table = Table('item_category_association', Base.metadata,
    Column('categories_id', Integer, ForeignKey('categories.id') ),
    Column('items_id', Integer, ForeignKey('items.id')),
    Column('updated_on', DateTime, onupdate=datetime.datetime.now, default=datetime.datetime.now))"""

class ItemCategoryAssociation(Base):
    __tablename__ = 'item_category_association'
    id = Column(Integer, Sequence('association_id_seq'), primary_key=True)
    items_id = Column('items_id', Integer, ForeignKey('items.id'))
    categories_id = Column('categories_id', Integer, ForeignKey('categories.id') )
    updated_on = Column('updated_on', DateTime, onupdate=datetime.datetime.now, default=datetime.datetime.now) 
    
    def __repr__(self):
        return "<Category(item_id=%s, category_id=%s, updated_on=%s)>" % (self.items_id, self.categories_id, self.updated_on)   


class Category(Base):
    __tablename__ = 'categories'
    # table column definitions
    id = Column(Integer, Sequence('category_id_seq'),  primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    items = relationship("Item", secondary='item_category_association', back_populates='categories')


    def __repr__(self):
        return "<Category(id=%s, name=%s)>" % (self.id, self.name)


# Item class metadata
class Item(Base):
    __tablename__ = 'items'
    # table column definitions
    id = Column(Integer, Sequence('item_id_seq'), primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String, server_default="This item has no description")
    categories = relationship("Category", secondary='item_category_association', back_populates='items')
     

    def __repr__(self):
        return "<Item(id=%s, name=%s, description=%s)>" % (self.id, self.name, self.description)

# User class metadata
class User(Base):
    __tablename__ = 'users'
    # table column definitions
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(255), nullable=False)
    logged_in = Column(Boolean, nullable=False, default=False)
    latest_session_exp = Column(DateTime)
     

    def __repr__(self):
        return "<User(id=%s, name=%s, logged_in=%s)>" % (self.id, self.name, self.logged_in)




# add schema to database 
if __name__ == '__main__':
    Base.metadata.create_all(engine)
    default_category = Category(name="None")
    engine = create_engine(sql_db_interface, echo=False)
    Session = sessionmaker(bind=engine)
    current_session = Session()
    current_session.add(default_category)
    current_session.commit()
    current_session.close()








