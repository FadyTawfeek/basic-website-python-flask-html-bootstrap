from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel
class Item(Resource):
    parser = reqparse.RequestParser() #initiate a parser that only accepts certain inputs (price only in our case) with certain conditions (such as float)
    parser.add_argument( 'price', #only accepts price even if we try to put name and price using postman
        type = float, #makes the value we pass for a price be always converted to a float
        required = True,#price is required
        help = 'This field can not be blank'
        ) #this parser was put up here so that we don't copy it twice in post and get

    @jwt_required() #require authentication first before getting an item
    # when we post the authorization (/auth) in postman with body of username, password, it returns a token
    #without this token, when we post an item normally, list of item will return it (by get all items because @jwt is not put before it in our case) but
    #get this specific item will return status 401 which indicates missing authentication, so in get this item
    #we should add header: key: Authorization, value: JWT "then the token we copied", this token will be produced only if the username and password we
    #entered matched the users information we have in our users list, note that @jwt_required could be added to any of the other request for verification

    def get(self, item_name): #self here means the same Item class
        item = ItemModel.find_item_by_name(item_name) # we now call ItemModel instead of self, in all functions
        if item:
            return item.json() #.json() was added here because now the find_item_by_name now return an return an object of calss ItemModel instead of returning a dictionary, so after adding .json() we now return the item itself
        
        return {'message': 'item requested not found'}, 404
             
    def post(self, item_name): #take the name input from the url
        item = ItemModel.find_item_by_name(item_name)       
        if item:
            return {'message':"An item with the name '{}' already exists.".format(item_name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(item_name, data['price'])
        try:
            item.Insert()
        except:
            return {'message': "An error occurred inserting an item"}, 500 #internal server error

        return item.json(), 201

    def put(self, item_name):
        item = ItemModel.find_item_by_name(item_name)
        data = Item.parser.parse_args()
        to_be_added_item = ItemModel(item_name, data['price'])
        if item:
            try:
                to_be_added_item.Update() #it should be item.Update() but we will understand later
            except:
                return {'message': "An error occurred updating an item"}, 500 #internal server error
        else:
            try:
                to_be_added_item.Insert()
            except:
                return {'message': "An error occurred inserting an item"}, 500 #internal server error
        return to_be_added_item.json(), 201

    def delete(self, item_name):
        item = ItemModel.find_item_by_name(item_name)
        if item:
            connection = sqlite3.connect('data.db') #make the database connection where all data are in the file data.db
            cursor = connection.cursor()
            query = "DELETE FROM items WHERE item_name=?" #note that to delete all row we should not use * with delete
            cursor.execute(query, (item_name,))
            connection.commit()
            connection.close()
            return {'message': "Item was deleted successfully"}, 201
        
        return {'message': "An item with the name '{}' does not exist.".format(item_name)}, 400 #meaning bad request for wanting to delete something not there
        
    
#remember that for all methods except get, we should add header of key: content type, value: app/json, and add body
#for get item method (or for any method that requires authentication), we should add header of key: authorization, value: JWT "then the token"

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result: #if we want to do something with each row
            items.append({'item_name': row[0], 'price': row[1]})

        connection.close()
        return {'all items': items}
        #return result will not work because we should return a json format only

#remember that in api