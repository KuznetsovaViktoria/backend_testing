from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
        'name': 'My Store',
        'items': [{
            'name': 'chair',
            'price': 1500
        }]
    }
]


@app.route('/store', methods=['POST'])
def create_store():
    data = request.get_json()
    store = {
        'name': data['name'],
        'items': []
    }
    stores.append(store)
    return jsonify(store)


@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name']== name:
            return jsonify(store)
    return jsonify({'message': 'page not found'})


@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})


@app.route('/store/<name>/item')
def get_item(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store['items'])
    return jsonify({'message': 'page not found'})


@app.route('/store/<name>/item', methods=['POST'])
def create_item(name):
    data = request.get_json()
    item = {
        'name': data['name'],
        'price': data['price']
    }
    for store in stores:
        if store['name'] == name:
            store['items'].append(item)
            return jsonify(item)
    return jsonify({'message': 'page not found'})

if __name__=='__main__':
    app.run(debug=True)
