from flask import Flask, json, request, jsonify

app = Flask(__name__)

stores = [
        {'name': 'ads', 
        'items': [{'name': 'Bread', 'price': 45}, {'name': 'Cookies', 'price': 30}]
        },
        {'name': 'hns',
        'items': [{'name': 'Cheese', 'price': 100}]
        }]

# accepts name in json format in request body
@app.route('/store', methods = ['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {'name': request_data['name'], 'items': []}
    stores.append(new_store)
    return jsonify(new_store)

@app.route('/store/<name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    else:
        return 'Store does not exist'

@app.route('/store')
def get_stores():
    return jsonify({'stores' : stores})

# accepts store_name in url. Item name and price in json format are expected in request body
@app.route('/store/<store_name>/item', methods = ['POST'])
def create_item(store_name):
    request_data = request.get_json()
    item = {'name': request_data['name'], 'price': request_data['price']}
    for store in stores:
        if store['name'] == store_name:
            store['items'].append(item)
            return jsonify(item)
    else:
        return 'Store does not exist'

@app.route('/store/<store_name>/item')
def get_items(store_name):
    for store in stores:
        if store['name'] == store_name:
            return jsonify({'items': store['items']})
    else:
        return 'Store does not exist'

app.run(port = 5000, debug = True)