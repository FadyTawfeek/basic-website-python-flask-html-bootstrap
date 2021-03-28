import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
class UserRegister(Resource): #class for adding a new user (sign up)
    parser = reqparse.RequestParser() 
    parser.add_argument( 'username', 
        type = str, 
        required = True,
        help = 'This field can not be blank'
        )

    parser.add_argument( 'password', 
        type = str, 
        required = True,
        help = 'This field can not be blank'
        )


    def post(self):
        data = UserRegister.parser.parse_args()
        
        # query_signUp_noDuplicates = "SELECT * FROM users WHERE username = ?"
        # result=cursor.execute(query_signUp_noDuplicates, (data['username'],))
        # row = result.fetchone() #if this user was found it will be fetched in row
        # if row:
        #     return {'msg': 'this username is already taken'}
        # else:
        if UserModel.find_by_username(data['username']):    
            return {'msg': 'this username is already taken'}, 400
        else:    
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "INSERT INTO users VALUES (NULL, ?, ?)" #because id is already produced and incremented automatically                
            cursor.execute( query, (data['username'], data['password']) ) #user should be in a tuple and no need for "," because we have more than 1 item there
            connection.commit()
            connection.close()
            return{'message': 'User was registered successfully'}, 201
            #remember that now we should register users first before authenticating as now the database is not an array anymore

        