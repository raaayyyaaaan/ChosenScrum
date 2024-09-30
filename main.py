from Login import * #Importing the class with the login GUI
from APIUI import * #Importing the class with the API and robot movement GUI
import sqlite3 #Sql to connect all data to the database

#This is the main function, where we simply call the Login class and grant access to the APIUI class once the user logs in
connection = sqlite3.connect('database.db')
cursor = connection.cursor()
login = Login()
if login.LoginSuccessful: #Authenticates that the user entered Chosen.net, granting them access to the API
    APIUI()
