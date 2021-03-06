import sys
sys.path.insert(0, '/home/ubuntu/.local/lib/python3.5/site-packages/')
from authorization import get_token_info, valid_user
from database_methods import *
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def get_all_data():
    """Returns response with all the Item and Category data
     in json format needed for the frontend web application"""
    return jsonify(retrieve_everything(sql_db_interface, 1000))


@app.route('/items')
def get_all_items():
    """Returns response with all the Item data in json format
     needed for the frontend web application"""
    return jsonify(retrieve_all('Item', sql_db_interface, 'name', 1000))


@app.route('/categories')
def get_all_categories():
    """Returns response with all the Category data in json format
     needed for the frontend web application"""
    return jsonify(retrieve_all('Category', sql_db_interface, 'name', 1000))


@app.route('/items/<item_name>')
def get_item(item_name):
    """Returns response with item data in json format"""
    return jsonify(retrieve(
        {'name': item_name, 'table_type': 'Item'},
        retrieve_item, sql_db_interface))


@app.route('/categories/<category_name>')
def get_category(category_name):
    """Returns response with category data in json format"""
    return jsonify(retrieve({'name': category_name,
                             'table_type': 'Category'},
                            retrieve_category,
                            sql_db_interface))


@app.route('/login/<token>')
def validate_login(token):
    return jsonify(get_token_info(token))


@app.route('/items/create/<item>&<description>&<token>', methods=['POST'])
def create_item(item, description, token):
    """Create new item in db, if user has valid token"""

    authorized_user = valid_user(token)

    if authorized_user:
        item_added = add({'name': item,
                          'description': description,
                          'table_type': 'Item'},
                         add_item,
                         sql_db_interface)
        if item_added:  # send okay response
            return "item added to DB", 201
        else:  # send failure response
            return "item failed to be added to DB", 403
    else:
        return "invalid token", 403


@app.route('/categories/create/<category>&<token>', methods=['POST'])
def create_category(category, token):
    """Create new category in db, if user has valid token"""

    authorized_user = valid_user(token)

    if authorized_user:
        category_added = add(
            {'name': category, 'table_type': 'Category'},
            add_category, sql_db_interface)
        if category_added:  # send okay response
            return "category added to DB", 201
        else:  # send failure response
            return "category failed to be added to DB", 403
    else:
        return "invalid token", 403


@app.route('/items/delete/<item>&<token>', methods=['POST'])
def remove_item(item, token):
    """Delete item in db, if user is authorized"""
    authorized_user = valid_user(token)

    if authorized_user:
        print("authorized")
        item_deleted = delete(
            {'name': item, 'table_type': 'Items'},
            delete_item, sql_db_interface)
        if item_deleted:  # send okay response
            return "item deleted", 201
        else:  # send failure response
            return "item failed to be deleted from DB", 403
    else:
        return "invalid token", 403


@app.route('/categories/delete/<category>&<token>', methods=['POST'])
def remove_category(category, token):
    """Delete item in db, if user is authorized"""
    authorized_user = valid_user(token)

    if authorized_user:
        print("authorized")
        category_deleted = delete({'name': category,
                                   'table_type': 'Categories'},
                                  delete_category,
                                  sql_db_interface)
        if category_deleted:  # send okay response
            return "category deleted", 201
        else:  # send failure response
            return "category failed to be deleted from DB", 403
    else:
        return "invalid token", 403


@app.route('/items/<item>/<category>&<relationship>&<token>', methods=['POST'])
@app.route(
    '/categories/<category>/<item>&<relationship>&<token>',
    methods=['POST'])
def change_category_item_relationship(item, category, relationship, token):
    """add or remove item / category connection in db"""

    authorized_user = valid_user(token)

    if authorized_user and (
            relationship == 'connect' or relationship == 'disconnect'):
        print("authorized")
        category_changed = connection_item_category(
            item, category, relationship)
        if category_changed:  # send okay response
            return "category relationship to item changed", 201
        else:  # send failure response
            return "category relationship to item not changed", 403
    else:
        return "invalid auth token", 403


@app.route('/items/<item>&<description>&<token>', methods=['POST'])
def update_item_description(item, description, token):
    """if authorized, update description of existing item in database"""

    authorized_user = valid_user(token)

    if authorized_user:
        print("authorized")
        item_updated = update({'name': item,
                               'description': description,
                               'table_type': 'Items'},
                              update_item,
                              sql_db_interface)
        if item_updated:  # send okay response
            return "item description updated", 201
        else:  # send failure response
            return "item description failed to be updated", 403
    else:
        return "invalid auth token", 403


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
