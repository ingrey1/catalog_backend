from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from database_setup import Category, Item, User
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
            # item and category exists in DB 
            if item != None and category != None:
                if connection_status == "connect":
                    # add category to item / item to category
                    item.categories.append(category)
                    print("***item and category connected***")
                else:
                    for x in range(len(item.categories)):
                        if item.categories[x].name == category_name:
                            # remove item from category, remove category from item
                            item.categories.pop(x)
                            print("***item and category disconnected***")
                # commit changes to db
                current_session.commit()
                return True
                
            else:
                print("item and category (dis)connection failure")
                return False

            current_session.close()

        except (DBAPIError, SQLAlchemyError) as e:
            print("item category connection failure")
            return False



    print("item category connection failed")
    return False


