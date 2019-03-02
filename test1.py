import sys
import os
sys.path.append(os.path.abspath(__file__)[0:-8] + 'database')
from database_methods import (add,add_item,update, update_item, add_category,delete, delete_category, add_item, delete_item, update_item, connection_item_category,
get_all_items, get_item_categories, retrieve, retrieve_category)
from database_configuration import sql_db_interface

add({'name': 'book1', 'description': 'the first book', 'table_type': 'Items'}, add_item, sql_db_interface)
#delete({'name': 'books', 'table_type': 'Category'}, delete_category, sql_db_interface)
#add({'name': 'books', 'table_type': 'Category'}, add_category, sql_db_interface)
connection_item_category('book1', 'books', 'connect')

#delete({'name': 'book1', 'description': 'the best book', 'table_type': 'Items'}, delete_item, sql_db_interface)

print(str(retrieve({'name':'books', 'table_type': 'Category'}, retrieve_category, sql_db_interface)))










