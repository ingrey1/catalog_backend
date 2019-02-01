from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Item, User


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


for x in range(len(categories)):

    categories_alchemy.append(Category(name=categories[x]))
    users_alchemy.append(User(full_name=users[x]))
    items_alchemy.append(Item(name=pets[x]))
    items_alchemy.append(Item(name=reptiles[x]))
    items_alchemy.append(Item(name=jobs[x]))



# create core interface to database - replace this with your own: 
engine = create_engine('postgresql://postgres:tyrion1234@localhost:5433/postgres', echo=True)
# class to produce instances of session
Session = sessionmaker(bind=engine)

current_session = Session()


print(current_session.query(Item).all()[0])

#current_session.add_all(categories_alchemy)
#current_session.add_all(items_alchemy)
#current_session.add_all(users_alchemy)
#current_session.commit()
#current_session.close()



