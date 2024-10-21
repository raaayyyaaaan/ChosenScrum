from tkinter import *
from tkinter import messagebox
import sqlite3
from os.path import exists

# Code to create the table. The table will be organized by three columns: UserID, Username, and Password. The User ID is the primary key and the table autoincrements with each insertion.
if exists('database.db') == False:
    connection = sqlite3.connect('database.db')
    # sql object that allows us to update and change the database one row at a time.
    cursor = connection.cursor()
    login_info = """CREATE TABLE login_info (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username VARCHAR(20),
    Password VARCHAR(30));"""
    cursor.execute(login_info)
else:
    connection = sqlite3.connect('database.db')
    # sql object that allows us to update and change the database one row at a time.
    cursor = connection.cursor()


#The Login class controls the GUI allowing the user to log in or sign up by creating a new username and password.
class Login:
    LoginSuccessful = False
    
# This function checks for the inputted user and password to figure out if the user is in the database, to tell them to sign up (instead of sign in), or proceed to check their inputted password. If the username exists, the password must match the user, or else it will give the user a message box that the password is incorrect.
    def sendinfo(self, root, login, user, password):
        sql = f"SELECT * FROM login_info"
        cursor.execute(sql)
        myresult = cursor.fetchall() #Get a list of all accounts to iterate through and find the requested account
        bFoundAccount = False #Value showing whether the account was found
        if myresult == []:
            messagebox.showinfo(message="Username or password does not exist, please try again or make a new user")
        for account in myresult:
            if user == account[1]:
                if password == account[2]:
                    messagebox.showinfo(message="Successfully signed into Chosen.net!")
                    bFoundAccount = True
                    break
                else:
                    messagebox.showinfo(message="Password does not match with the username, please try again.")
                    break
        if bFoundAccount == False:
            messagebox.showinfo(message="Username or password does not exist. Please try again or make a new account.")
        else:
            login.LoginSuccessful = True
            root.destroy() #Close the Login Tkinter window

    
#This function asks the user if they want to create a user with the information they entered. If the user returns yes, then it creates the user with that information. 
    def call(self, user, password):
        response = messagebox.askquestion('Create User', f'Would you like to create the user with this information:\nUsername: {user}, Password: {password}')
        if response == 'yes':
            return True
        else:
            return False
            
            
#This function takes input of the username and password, creating it into a variable, which gets inserted into the table and sends user a pop up message that their login was successful.
    def create_user(self, user, password):
        if self.call(user, password):
            print(user, password)
            ins = f"INSERT INTO login_info (Username, Password) VALUES ('{user}', '{password}')" #Inserts username and password as values in the table
            print(ins)
            cursor.execute(ins)
            connection.commit() #Make sure the values are now committed to the database
            messagebox.showinfo(message=f"Successfully created and added your information:\nUsername: {user} Password: {password} into our database!")

#Code setting up the tkinter window
    def __init__(self):
# Creating a light gray window screen of size 400 x 250 titled "CHOSEN.net"
        root = Tk()
        root.title("CHOSEN.net")
        root.geometry("400x250")
        root.configure(bg="light gray")

# A frame which will contain the buttons and labels for signing in shown towards the bottom.

        frame1 = Frame(master=root, relief="raised", height=5, bd=3)
        frame1.pack(pady=30, side=BOTTOM)

# Then, we created a label button which displays “Welcome to Chosen Network” centered at the top bolded in Times New Roman.
        welcome = Label(master=root, text="Welcome to Chosen Network", font=("Times New Roman", 30, "bold"), justify=CENTER, bg="light gray")
        welcome.pack(side=TOP, pady=30)


# The usertext label creates a label at the top left of the frame titled “USER ID”.
# The entry label, to the right of the userid label, allows for the entry of the username and will store the entered information in the userid string variable.
        userid = StringVar()
        usertext = Label(master=frame1, text="USERNAME", font=("Arial", 14), justify=CENTER)
        usertext.grid(column=0, row=1)
        uentry = Entry(master=frame1, textvariable=userid, width=25, background="light gray")
        uentry.grid(column=1, row=1)


#The passtext label creates a label directly below the usertext label titled “PASSWORD”. The pentry label, to the right of the passid label, allows for the entry of the password and will store the entered information in the passid string variable.

        password = StringVar()
        passtext = Label(master=frame1, text="PASSWORD", font=("Arial", 14), justify=CENTER)
        passtext.grid(column=0, row=2)
        pentry = Entry(master=frame1, textvariable=password, width=25, background="light gray")
        pentry.grid(column=1, row=2)


# This makes the button to sign in. It then gets the username and password. 
        send = Button(master=frame1, text="Sign In", font=("Arial", 14), justify=CENTER, fg="blue", bg="blue",
                        command=lambda: self.sendinfo(root, self, userid.get(), password.get()))
        send.grid(column=1, row=3)


# This makes the button to sign up. It also gets the username and password. 
        create = Button(master=frame1, text="Sign Up", font=("Arial", 14), justify=CENTER, fg="blue", bg="blue",
                        command=lambda: self.create_user(userid.get(), password.get()))
        create.grid(column=0, row=3)


# This makes the tkinter work and the code run properly. 
        root.mainloop()

    
