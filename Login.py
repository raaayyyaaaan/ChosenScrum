#sqlite3 creates a database and allows us to edit the database to insert values, delete values, and parse through the values.
# from flask import g helps store data and allows us to initialize the database.
import sqlite3
from flask import g

DATABASE = 'database.db'

# Function to get the database connection.
def get_db():
   if 'db' not in g:  # If the connection doesn't exist, we create a new one
       g.db = sqlite3.connect(DATABASE, check_same_thread=False)
       g.db.row_factory = sqlite3.Row  # Allows column names to be accessed by the name of the rows.
   return g.db

# Function to close the database connection.
def close_db():
   if 'db' in g:
       g.db.close()

# Creating the table if the table does not exist.
def init_db():
   db = get_db()
   cursor = db.cursor()
   cursor.execute("""
       CREATE TABLE IF NOT EXISTS login_info (
           UserID INTEGER PRIMARY KEY AUTOINCREMENT,
           Username VARCHAR(20),
           Password VARCHAR(30)
       );
   """)
   db.commit()


# The Login class checks credentials. The Login module returns the values showing whether the account was found in the database, whether the password matches, and whether the user has access to the Chosen network.
class Login:
   LoginSuccessful = False
   bFoundAccount = False

# sendinfo sends whether the account is in the database and whether the user could successfully enter the Chosen Network. It takes in the username and password inputs as parameters.
   def sendinfo(self, user, password):
       init_db()
       db = get_db()  # Get the database connection for this request.
       cursor = db.cursor()


       # Use a parameterized query to prevent SQL injection.
       sql = "SELECT * FROM login_info WHERE Username = ?"
       cursor.execute(sql, (user,))
       account = cursor.fetchone()


       if account:
           self.bFoundAccount = True
           if password == account['Password']:
               self.LoginSuccessful = True
           else:
               self.LoginSuccessful = False # The user's password does not match their username.
       else:
           self.bFoundAccount = False # There is no account with this username in the database.

# Create a new username by adding their information to the swlite3 database. This function takes in the username and password and parameters.
   def create_user(self, user, password):
       db = get_db()  # Get the database connection for this request.
       cursor = db.cursor()
       # Insert a new user into the database.
       cursor.execute("INSERT INTO login_info (Username, Password) VALUES (?, ?)", (user, password))
       db.commit()
