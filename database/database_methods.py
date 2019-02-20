from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from database_setup import Category, Item, User, ItemCategoryAssociation
from database_configuration import sql_db_interface


def add_item(name, description):
    """add new item to Items table in database"""

    valid_name =  isinstance(name, str) and len(description) > 0
    valid_description = isinstance(description, str) and len(description) > 0 

    if valid_name and valid_description:
        new_item = Item(name=name, description=description)
        try:
            # create core interface to database 
            engine = create_engine(sql_db_interface, echo=True)
            Session = sessionmaker(bind=engine)
            current_session = Session()
            default_category = current_session.query(Category).filter(Category.name == category_name).first()
            new_item.categories.append(default_category)
            current_session.add(new_item)
            current_session.commit()
            current_session.close()
            print("***item added to Items***")
            return True


        except (DBAPIError, SQLAlchemyError) as e:

            print("***item failed to be added to Items***")
            return False


    print("***basic validation failed, item not added to items***")    
    return False



def delete_item(name):
    """delete item from Items table in database"""

    try:
         engine = create_engine(sql_db_interface, echo=True)
         Session = sessionmaker(bind=engine)
         current_session = Session()
         # delete the record with name 
         current_session.delete(current_session.query(Item).filter(Item.name == name).first()) 
         # commit changes to db
         current_session.commit()
         current_session.close()
         print("***item successfully deleted***")       
         return True

    except (DBAPIError, SQLAlchemyError) as e:
        print("***item failed to be deleted***")
        return False

def update_item(name, new_description):
    """update the description of Item with name in Items table"""

    valid_name = isinstance(name, str) and len(name) > 0
    valid_description = isinstance(new_description, str) and len(new_description) > 0
    if valid_name and valid_description:
        try:
            engine = create_engine(sql_db_interface, echo=True)
            Session = sessionmaker(bind=engine)
            current_session = Session()
            # update the record with new description 
            item = current_session.query(Item).filter(Item.name == name).first()
            if item != None:
                item.description = new_description
                # commit changes to db
                current_session.commit()
                current_session.close()
                print("***item updated***")       
                return True
            else:
                print("***item with name doesnt exist in db***")
                return False

        except (DBAPIError, SQLAlchemyError) as e:
            print("***item update failed***")
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


def get_item(item_name):
    """get item from Items by name"""

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
                current_session.close()
                return item
            
            print("***item not in DB***")
            current_session.close()
            return None 
        except (DBAPIError, SQLAlchemyError) as e:
            print("***couldn't retrieve Item***")
            current_session.close()
            return None
    print("invalid item_name")
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


