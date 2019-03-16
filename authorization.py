import requests



def get_token_info(token):
    """Returns token info"""

    url = "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=%s" % (token)
    data = requests.get(url).json()
    
    return data

def valid_user(token):
    """Returns True if token is valid"""
    
    token_response = get_token_info(token) 
    print("token_response in valid user: %s " % (token_response) )
   
    if isinstance(token_response, dict):
        if 'exp' in token_response:

            valid_user = int(token_response['exp']) > 0
        else:
            valid_user = False    
    else:
        valid_user = False

    return valid_user   



