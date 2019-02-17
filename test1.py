import sys
import os
sys.path.append(os.path.abspath(__file__)[0:-8] + 'database')
from database_methods import add_item, delete_item, update_item, connection_item_category

connection_item_category("parrot", "pets", "connect")

