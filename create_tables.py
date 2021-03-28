import sqlite3
connection = sqlite3.connect('data.db') #make the database connection where all data are in the file data.db
cursor = connection.cursor() #like our mouse cursor to indicate where we are in the database
create_users_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)" #the users table will have 3 columns, integer primary key to make id assigned automatically and incrementally
cursor.execute(create_users_table) #execute the creation

create_items_table= "CREATE TABLE IF NOT EXISTS items (item_name text, price real)"
cursor.execute(create_items_table) #execute the creation

connection.commit() # make the previous changes
connection.close()