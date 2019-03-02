from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from database_setup import Category, Item, User, ItemCategoryAssociation
from database_configuration import sql_db_interface
from data_validation import valid_category_data, valid_item_data



   


def add_item(data, db_session):
    """add new item to Items table in database"""

    

    if valid_item_data(data):


        item_status = db_session.query(Item).filter(Item.name == data['name']).first() 


        if not item_status:

            if data['description']:
                new_item = Item(name=data['name'], description=data['description'])
            else:
                new_item = Item(name=data['name'])



            default_category = db_session.query(Category).filter(Category.name == 'None').first()
            new_item.categories.append(default_category)
            db_session.add(new_item)
            item_exists = db_session.query(Item).filter(Item.name == new_item.name).first()
            if item_exists:
                print("***%s item record added to Items table***" % (data['name']))
                return True
            else:
                print("***%s item failed to be added to Items table***" % (data['name']))
                return False
        else:

            print("***%s item in DB***" % (data['name']))
            return False 

          




def delete_item(item_data, db_session):
   """delete item from Items table in database"""

   if valid_item_data(item_data):

        item = db_session.query(Item).filter(Item.name == item_data['name']).first()
        if item:
           # delete item
           db_session.delete(item)
           item_exists = db_session.query(Item).filter(Item.name == item_data['name']).first() 
           if not item_exists:
             print("***%s item record deleted***" % (item_data['name']))
             return True
           else:
             print("***%s item failed to be deleted***" % (item_data['name']))
             return False
   print("***%s item not in db***" % (item_data['name']))
   return False

def update_item(item_data, db_session):
    """update the description of Item with name in Items table"""

    
    if valid_item_data(item_data):
       
            item = db_session.query(Item).filter(Item.name == item_data['name']).first()
            if item:
                item.description = item_data['description']
                if item.description == item_data['description']:
                    print("***description update of %s item successfully changed***" % (item_data['name']))
                    return True
                else:
                    print("***description update of %s item failed***" % (item_data['name']))
                    return False
               
            else:
                print("***item with name doesnt exist in db***")
                return False

       
    else:
        print("***basic item data validation failed***")
        return False 

def connection_item_category(item_name, category_name, connection_status):
    """add item to category, and category to item in DB"""
    valid_item_name = isinstance(item_name, str) and len(item_name) > 0
    valid_category_name = isinstance(category_name, str) and len(category_name) > 0
    valid_connection_status = connection_status == "connect" or connection_status == "disconnect"
    if valid_item_name and valid_category_name and valid_connection_status:

        try:
            engine = create_engine(sql_db_interface, echo=True)
            Session = sessionmaker(bind=engine)
            current_session = Session()
            # get reference to item and category
            item = current_session.query(Item).filter(Item.name == item_name).first()
            category = current_session.query(Category).filter(Category.name == category_name).first()
            default_category = current_session.query(Category).filter(Category.name == "None").first()
            # item and category exists in DB 
            if item != None and category != None:
                if connection_status == "connect":
                    # delete 'None' category, if it exists
                    for x in range(len(item.categories)):
                        if item.categories[x].name == "None":
                            item.categories.pop(x)
                    # add category to item / item to category
                    item.categories.append(category)
                    print("***item and category connected***")
                else: # removing the category
                    for x in range(len(item.categories)):
                        if item.categories[x].name == category_name:
                            # remove item from category, remove category from item
                            item.categories.pop(x)
                    # add "None as a category" if there are no categories left
                    if len(item.categories) == 0:
                        item.categories.append(default_category)
                    print("***item and category disconnected***")
                # commit changes to db
                current_session.commit()
                current_session.close()
                return True
                
            
            print("item and category (dis)connection failure")
            current_session.close()
            return False

            

        except (DBAPIError, SQLAlchemyError) as e:
            print("item category connection failure")
            current_session.close()
            return False



    print("item category connection failed")
    return False




def get_item_categories(item_name):
    """Return list of Category instances that have item_name as an Item"""
    valid_item_name = isinstance(item_name, str) and len(item_name) > 0 

    if valid_item_name:
        try:
            engine = create_engine(sql_db_interface, echo=True)
            Session = sessionmaker(bind=engine)
            current_session = Session()
            # get reference to item 
            item = current_session.query(Item).filter(Item.name == item_name).first()
            if item != None:
                print("***item in DB***")
                categories = item.categories
                current_session.close()
                return categories
            
            print("***item not in DB***")
            current_session.close()
            return None 

        except (DBAPIError, SQLAlchemyError) as e:
            print("***couldn't retrieve categories***")
            current_session.close()
    print("invalid item name")
    return None        


def get_all_items(order_by, limit=1000):
    """returns a list of Item objects, ordered by order_by"""

    valid_order_by = order_by == "updated_on" or order_by == "name"
    valid_limit = limit > 0 and limit < 10000

    if valid_order_by and valid_limit:
        try:
            engine = create_engine(sql_db_interface, echo=True)
            Session = sessionmaker(bind=engine)
            current_session = Session()
            if order_by == "name": 
                items = current_session.query(Item).order_by(getattr(Item, order_by)).limit(limit).all()
            elif order_by == "updated_on":
                items = current_session.query(Item).join(ItemCategoryAssociation).order_by(ItemCategoryAssociation.updated_on.desc()).all()
                print(items) 
            current_session.close()
            return items            
        except (DBAPIError, SQLAlchemyError) as e:
                current_session.close()
                print("error")
                return None
    print("Invalid limit or order_by")        
    return None





def add_category(category_data, db_session):
    """adds new category from category_data to db associated with db_session"""

    if valid_category_data(category_data):

        category_exists = db_session.query(Category).filter(Category.name == category_data['name']).first()
        if category_exists:
            print("***the %s category is already in DB***" % (category_data['name'])  )
            return False
        else: # at category to do
            new_category = Category(name=category_data['name'])
            db_session.add(new_category)
            category_added = db_session.query(Category).filter(Category.name == category_data['name']).first()
            if category_added:
                print("***%s category record added to Category table***" % (category_data['name']))
                return True
            else: 
                print("***%s category record failed to be added to DB" % (category_data['name']))
                return False


    # basic validation failed for category data
    return False
    print("basic validation for category data failed")

def delete_category(category_data, db_session):
    """delete category from Category table"""

    if valid_category_data(category_data):

        category = db_session.query(Category).filter(Category.name == category_data['name']).first()
        if category:
           # delete category
           db_session.delete(category)
           category_exists = db_session.query(Category).filter(Category.name == category_data['name']).first() 
           if not category_exists:
             print("***%s category record deleted***" % (category_data['name']))
             return True
           else:
             print("***%s category failed to be deleted***" % (category_data['name']))
             return False
        print("***%s category not in db***" % (category_data['name']))
        return False 
           

        

    # basic validation failed for category data
    return False
    print("basic validation for category data failed")    


def add(data, data_f, db_connection_info):
    """uses db_connection_info to connect and add object to db."""
    try:
            # create core interface to database 
            engine = create_engine(db_connection_info, echo=True)
            Session = sessionmaker(bind=engine)
            current_session = Session()
            # add record to database
            added_object = data_f(data, current_session)

            if added_object:
                current_session.commit()
                current_session.close()
                return True
            else:
                raise SQLAlchemyError

    except (DBAPIError, SQLAlchemyError) as e:

            print("***%s failed to be added to the %s table***" % (data['name'], data['table_type']))
            current_session.close()
            return False

def delete(data, data_f, db_connection_info):
    """uses db_connection_info to connect and add object to db."""

    
    try:
            # create core interface to database 
            engine = create_engine(db_connection_info, echo=True)
            Session = sessionmaker(bind=engine)
            current_session = Session()
            # add record to database
            deleted_object = data_f(data, current_session)

            if deleted_object:
                current_session.commit()
                current_session.close()
                return True
            else:
                raise SQLAlchemyError

    except (DBAPIError, SQLAlchemyError) as e:

            print("***%s failed to be deleted from the %s table***" % (data['name'], data['table_type']))
            current_session.close()
            return False

def update(data, data_f, db_connection_info):
    """uses db_connection_info to connect and add object to db."""
    try:
            # create core interface to database 
            engine = create_engine(db_connection_info, echo=True)
            Session = sessionmaker(bind=engine)
            current_session = Session()
            # add record to database
            updated_object = data_f(data, current_session)

            if updated_object:
                current_session.commit()
                current_session.close()
                return True
            else:
                raise SQLAlchemyError

    except (DBAPIError, SQLAlchemyError) as e:

            print("***%s failed to be updated in the %s table***" % (data['name'], data['table_type']))
            current_session.close()
            return False



def retrieve_category(category_data, db_session):
    """returns dictionary  from DB"""
    if valid_category_data(category_data):
        category = db_session.query(Category).filter(Category.name == category_data['name']).first()
        if category:
            category_info = {'name': category.name, 'items': [item.name for item in category.items]}
            return category_info
        else:
            print("***%s category record not in Category table***" % (category_data['name']) )
            return None
    else:
        print("***Basic category data validation failed***")
        return None


def retrieve(data, data_f, db_connection_info):
    """return dictionary of record information from db"""


    try:
            # create core interface to database 
            engine = create_engine(db_connection_info, echo=True)
            Session = sessionmaker(bind=engine)
            current_session = Session()
            # add record to database
            retrieved_record_info = data_f(data, current_session)
            if retrieved_record_info:
                current_session.close()
                print("successfully retrieved %s record from %s " % (data['name'], data['table_type']))
                return retrieved_record_info
            else:
                raise SQLAlchemyError 
           

    except (DBAPIError, SQLAlchemyError) as e:

            print("***%s failed to be retrieved from the %s table***" % (data['name'], data['table_type']))
            current_session.close()
            return None