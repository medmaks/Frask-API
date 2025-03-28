from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

stores = []

class Store(Resource):
    def get(self, name):
        for store in stores:
            if store['name'] == name:
                return store, 200
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if next((store for store in stores if store['name'] == name), None):
            return {'message': f"Store with name '{name}' already exists."}, 400
        store = {'name': name, 'items': []}
        stores.append(store)
        return store, 201

    def delete(self, name):
        global stores
        stores = [store for store in stores if store['name'] != name]
        return {'message': 'Store deleted'}, 200

class StoreList(Resource):
    def get(self):
        return {'stores': stores}, 200

class Item(Resource):
    def get(self, store_name, name):
        store = next((store for store in stores if store['name'] == store_name), None)
        if store:
            item = next((item for item in store['items'] if item['name'] == name), None)
            if item:
                return item, 200
            return {'message': 'Item not found in this store'}, 404
        return {'message': 'Store not found'}, 404

    def post(self, store_name, name):
        store = next((store for store in stores if store['name'] == store_name), None)
        if store:
            if next((item for item in store['items'] if item['name'] == name), None):
                return {'message': f"Item with name '{name}' already exists in store '{store_name}'."}, 400
            data = request.get_json()
            if 'price' not in data:
                return {'message': "Missing 'price' in request body."}, 400
            item = {'name': name, 'price': data['price']}
            store['items'].append(item)
            return item, 201
        return {'message': 'Store not found'}, 404

    def delete(self, store_name, name):
        store = next((store for store in stores if store['name'] == store_name), None)
        if store:
            store['items'] = [item for item in store['items'] if item['name'] != name]
            return {'message': 'Item deleted from store'}, 200
        return {'message': 'Store not found'}, 404

class ItemList(Resource):
    def get(self, store_name):
        store = next((store for store in stores if store['name'] == store_name), None)
        if store:
            return {'items': store['items']}, 200
        return {'message': 'Store not found'}, 404

api.add_resource(Store, '/stores/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/stores/<string:store_name>/items/<string:name>')
api.add_resource(ItemList, '/stores/<string:store_name>/items')

if __name__ == '__main__':
    app.run(debug=True)