



def valid_category_data(category_data):
    """Returns True if all category_data is valid, False otherwise"""

    valid_category_name = isinstance(category_data['name'], str) and len(category_data['name']) > 0

    return valid_category_name

def valid_item_data(item_data):
    """Returns True if all item_data is valid, False otherwise"""

    valid_item_name = isinstance(item_data['name'], str) and len(item_data['name']) > 0
    valid_item_description = None or isinstance(item_data['description'], str)

    return valid_item_name and valid_item_description

def valid_user_data(user_data):

    pass 


