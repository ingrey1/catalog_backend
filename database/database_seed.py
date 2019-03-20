from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database_setup import Category, Item, User
from database.database_configuration import sql_db_interface


# seed data

# stores alchemy class instances to populate DB
categories_alchemy = []

items_alchemy = []

users_alchemy = []


# categories data
categories = ['pets', 'reptiles', 'jobs']
# items data
pets = ['parrot', 'dog', 'cat']
reptiles = ['lizard', 'snake', 'turtle']
jobs = ['pilot', 'engineer', 'animal trainer']
# users data
users = ['ted pullman', 'james george', 'simba canote']


# create core interface to database
engine = create_engine(sql_db_interface, echo=True)
# class to produce instances of session
Session = sessionmaker(bind=engine)

current_session = Session()


default_category = current_session.query(
    Category).filter(Category.name == "None").first()


for x in range(len(categories)):

    categories_alchemy.append(Category(name=categories[x]))
    users_alchemy.append(User(name=users[x]))
    item1 = Item(name=pets[x])
    item1.categories.append(default_category)
    item2 = Item(name=reptiles[x])
    item2.categories.append(default_category)
    item3 = Item(name=jobs[x])
    item3.categories.append(default_category)
    items_alchemy.append(item1)
    items_alchemy.append(item2)
    items_alchemy.append(item3)

current_session.add_all(categories_alchemy)
current_session.add_all(items_alchemy)
current_session.add_all(users_alchemy)


current_session.commit()
current_session.close()
