from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

"""
# FIRST FLASK APP
@app.route('/') # the string is the webpath so for this case: localhost:5000/
def home(): # can be named anything
    return "Hello, World!"


app.run(port=5000)
"""

# POST - used to receive data (from servers perspective)
# GET  - used to send data back only (from servers perspective)

# This is ugly, and it exists to follow protocol exclusively
STORES = [
    {
        'name': 'My Wonderful Store',
        'items': [
            {
                'name': 'My Item',
                'price': 15.99
            }
        ]
    }
]

@app.route('/')
def home():
    return render_template('index.html')
# POST /store data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    STORES.append(new_store)
    return jsonify(new_store)

# GET /store/<string:name>
@app.route('/store/<string:name>')
def get_store(name):
    """
    Iterate over stores, if the store name matches, return it
    if no matches, return an error message
    """
    for store in STORES:
        if store['name'] == name:
            return jsonify(store)

    return jsonify({'message': "Error! store: {} not found".format(name)})

# GET /store
@app.route('/store')
def get_stores():
    return jsonify({'stores': STORES})

# POST /store<string:name>/item
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in STORES:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'Error store not found'})


# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    for store in STORES:
        if store['name'] == name:
             return jsonify({'items': store['items']})
    return jsonify({'message': 'store not found'})


app.run(port=5000)