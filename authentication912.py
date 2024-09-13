# We are importing tkinter to create the GUI visual for users to input information, and sql to create a database with tables of information.
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

# Connects our code to a database online that exists on the host website
mydb = mysql.connector.connect(
 host="sql5.freesqldatabase.com",
 user="sql5730781",
 password="lyRG98lVQy",
 database="sql5730781"
)

# The plan for formatting the table to put the data in. 
"""     logininfo
UserID | Username | Password

"""

# sql object that allows us to update and change the database one row at a time.
mycursor = mydb.cursor()

# This function checks for inserted user and password to first figure out if the user is in the database, to either tell them to sign up (instead of sign in) or proceed to check their inputted password. If the username exists, the password must match the user, or else it will give the user a message box that the password is incorrect.
def sendinfo(u, p):
   sql = f"SELECT * FROM logininfo"
   try:
       mycursor.execute(sql)
       myresult = mycursor.fetchall()
       print(myresult)
       for x in myresult:
           if u == x[1]:
               if p == x[2]:
                   messagebox.showinfo(message="User exists")
                   break
               else:
                   messagebox.showinfo(message="Password does not match username, try again")
                   break
           else:
               messagebox.showinfo(message="User or password does not exist, please try again")
               break
   except mysql.connector.errors.ProgrammingError:
       messagebox.showinfo(message = "User does not exist")

# This function asks the user if they want to create a user with the information they entered. If the user returns yes, then it creates the user with that information. 
def call(u, p):
   val = [u, p]
   res = messagebox.askquestion('Create User', f'Would you like to create the user with this information:'
                                               f'\n{u}, {p}')
   if res == 'yes':
       return True
   else:
       return False

# This function takes input of the username and password, creating it into a variable, which gets inserted into the table and sends user a pop up message that their login was successful/ 
def createuser(u, p):
   val = [u, p]
   if call(u, p):
       print(u, p)
       try:
           ins = f"INSERT INTO logininfo (Username, Password) VALUES ({u}, {p})"
           message = f"Successfully created and added your information:\nUser- {u} Password- {p}\nto our database!"
           mycursor.execute(ins)
           mydb.commit()
       except mysql.connector.errors.ProgrammingError:
           root.destroy()
   else:
       root.destroy()

# A light gray window screen of size 400 x 250 titled “CHOSEN.net”
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
usertext = Label(master=frame1, text="USER ID", font=("Arial", 14), justify=CENTER)
usertext.grid(column=0, row=1)
uentry = Entry(master=frame1, textvariable=userid, width=25, background="light gray")
uentry.grid(column=1, row=1)


# The passtext label creates a label directly below the usertext label titled “PASSWORD”.
# The pentry label, to the right of the passid label, allows for the entry of the password and will store the entered information in the passid string variable.
password = StringVar()
passtext = Label(master=frame1, text="PASSWORD", font=("Arial", 14), justify=CENTER)
passtext.grid(column=0, row=2)
pentry = Entry(master=frame1, textvariable=password, width=25, background="light gray")
pentry.grid(column=1, row=2)

# The send button creates a button titled Sign In. It will take the information from userid and password and send it back to be used for the sendinfo function. This button is directly below the place to enter the password.
send = Button(master=frame1, text="Sign In", font=("Arial", 14), justify=CENTER, fg="blue", bg="blue",
            command=lambda: sendinfo(userid.get(), password.get()))
send.grid(column=1, row=3)

# The create button creates a button titled Sign Up. It will take the information from userid and password and send it back to be used for the createuser function. This button is directly below the label for the password.
create = Button(master=frame1, text="Sign Up", font=("Arial", 14), justify=CENTER, fg="blue", bg="blue",
            command=lambda: createuser(userid.get(), password.get()))
create.grid(column=0, row=3)

# This is a method so that we will continuously let the window run until the user exits the window
root.mainloop()
