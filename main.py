from flask import Flask
import sys
sys.path.append('./database')
from database_methods import retrieve_everything
from database_configuration import sql_db_interface
app = Flask(__name__)

@app.route('/')
def app_data():
    return jsonify(retrieve_everything(sql_db_interface, 1))

@app.route('/hello')

def HelloWorld():
    return "Hello World"

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
