import sqlite3

class ItemModel:
    def __init__(self, item_name, price):
        self.item_name = item_name
        self.price = price
    
    def json(self):
        return {'item_name': self.item_name, 'price': self.price}

    @classmethod
    def find_item_by_name(cls, item_name): #this is a class method because it uses the ItemModel class attributes
        connection = sqlite3.connect('data.db') #make the database connection where all data are in the file data.db
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE item_name=?"
        result = cursor.execute(query, (item_name,))
        row = result.fetchone() #to check if result is empty or not
        connection.close()
        if row:
            return cls(*row) #=cls(row[0], row[1]) #we type cls now because we want to return an object of calss ItemModel instead of returning a dictionary
    
    def Insert (self): #we changed that from (cls, item) to (self) as it is basically inserting itself now not taking an item in
        connection = sqlite3.connect('data.db') #make the database connection where all data are in the file data.db
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (self.item_name, self.price)) #and we will change item to self in the body of the method below as now it is inserting itself
        connection.commit()
        connection.close()

    def Update (self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE item_name=?"
        cursor.execute(query, (self.price, self.item_name))
        connection.commit()
        connection.close()