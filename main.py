from flask import Flask, jsonify
from flask_cors import CORS
import json
import sys
sys.path.append('./database')
from database_methods import (retrieve_everything, retrieve_all, retrieve, retrieve_item, retrieve_category, add, delete, delete_item, add_item,
connection_item_category)
from database_configuration import sql_db_interface
from authorization import get_token_info, valid_user


app = Flask(__name__)
CORS(app)

@app.route('/')
def get_all_data():
    """Returns response with all the Item and Category data in json format needed for the frontend web application"""
    return jsonify(retrieve_everything(sql_db_interface, 1000))
@app.route('/items')
def get_all_items():
    """Returns response with all the Item data in json format needed for the frontend web application"""
    return jsonify(retrieve_all('Item', sql_db_interface, 'name', 1000))
@app.route('/categories')
def get_all_categories():
    """Returns response with all the Category data in json format needed for the frontend web application"""
    return jsonify(retrieve_all('Category', sql_db_interface, 'name', 1000))

@app.route('/items/<item_name>')

def get_item(item_name):
    """Returns response with item data in json format"""
    return jsonify(retrieve({'name': item_name, 'table_type': 'Item'}, retrieve_item,  sql_db_interface))
@app.route('/categories/<category_name>')    
def get_category(category_name):
    """Returns response with category data in json format"""
    return jsonify(retrieve({'name': category_name, 'table_type': 'Category'}, retrieve_category,  sql_db_interface))
@app.route('/login/<token>')
def validate_login(token):
    return jsonify(get_token_info(token))
@app.route('/items/create/<item>&<description>&<token>', methods=['POST'])
def create_item(item, description, token):
    """Create new item in db, if user has valid token"""
   
 
    authorized_user = valid_user(token)

    if authorized_user:
        item_added = add({'name': item, 'description': description, 'table_type': 'Item'}, add_item, sql_db_interface)
        if item_added: # send okay response 
            return "item added to DB", 201
        else: # send failure response
            return "item failed to be added to DB", 403
    else:
        return "invalid token", 403

@app.route('/items/delete/<item>&<token>', methods=['POST']) 
def remove_item(item, token):
    """Delete item in db, if user is authorized"""
    authorized_user = valid_user(token)

    if authorized_user:
        print("authorized")
        item_deleted = delete({'name': item, 'table_type': 'Items'}, delete_item, sql_db_interface)
        if item_deleted: # send okay response 
            return "item deleted", 201
        else: # send failure response
            return "item failed to be deleted from DB", 403
    else:
        return "invalid token", 403

@app.route('/items/<item>/<category>&<relationship>&<token>', methods=['POST'])
def change_category_item_relationship(item, category, relationship, token):
    """add or remove an existing category from item in db"""

    authorized_user = valid_user(token)

    if authorized_user and (relationship == 'connect' or relationship == 'disconnect'):
        print("authorized")
        category_changed = connection_item_category(item, category, relationship)
        if category_changed: # send okay response 
            return "category relationship to item changed", 201
        else: # send failure response
            return "category relationship to item not changed", 403
    else:
        return "invalid auth token", 403


    



if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
