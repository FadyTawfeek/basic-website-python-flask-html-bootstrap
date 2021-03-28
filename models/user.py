import sqlite3
class UserModel: #class for initiating a user, finding the user and retrieving it (sign in)
    def __init__(self, _id, username, password): #id because id is a python keyword, but self.id is okay
        self.id = _id
        self.username = username
        self.password = password

    @classmethod #the next code is a method of the class User, so we use cls instead of self, User
    def find_by_username(cls, username): #a function to find user by his username
        connection = sqlite3.connect('data.db') #connecting to the data.db database
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?" #selecting all data with the same username we provided
        result = cursor.execute(query, (username,)) #putting the data of the selected user in result variable
        row = result.fetchone() #if this user was found it will be fetched in row
        if row:
            user = cls(*row) #retrieve data in the 3 columns in this user
        else:
            user = None

        connection.close()
        return user

    @classmethod #the next code is a method of the class User, so we use cls instead of self, User
    def find_by_id(cls, _id): #a function to find user by his id
        connection = sqlite3.connect('data.db') #connecting to the data.db database
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?" #selecting all data with the same id we provided
        result = cursor.execute(query, (_id,)) #putting the data of the selected user in result variable, the, format is because we want to indicate a tuple containing only id for the user
        row = result.fetchone() #if this user was found it will be fetched in row
        if row:
            user = cls(*row) #retrieve data in the 3 columns in this user
        else:
            user = None

        connection.close()
        return user
