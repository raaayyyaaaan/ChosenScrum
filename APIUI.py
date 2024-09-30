from tkinter import *
from tkinter import messagebox
import requests #This library allows for the making of http requests to the server and the accessing of responses

'''The APIUI class sets up a tkinter window with five buttons: forward, backward, left, right, and stop. Once clicking the buttons, a text box will show the output of the corresponding API being run.
For instance, if you press the Forward button, the text box will show
{
  "forward": "(0,1)",
  "success": true
}'''
class APIUI:
    def send_request(self, url): #Sends requests to the host url
        x = requests.post(url)
        return x
    def show_response(self, textbox, x):
        textbox.config(state="normal") # Make the state normal
        textbox.delete("0.0", "end") #Delete the previous data in the textbox
        textbox.insert("end", f"{x.text}") #Display the API output
        textbox.config(state="disabled") # Make the state disabled again so that the text box is read only
#This is the code setting up the tkinter window
    def __init__(self):
# Creating a light gray window screen of size 640 x 480 titled "CHOSEN.net"
        root = Tk()
        root.title("CHOSEN.net")
        root.geometry("640x480")
        root.configure(bg="light gray")
# A frame which will contain the buttons, labels, and text boxes towards the bottom.
        frame1 = Frame(master=root, relief="raised", height=5, bd=3)
        frame1.pack(pady=30, side=BOTTOM)

# Then, we created a label button which displays “Welcome to Chosen Network” centered at the top bolded in Times New Roman.
        welcome = Label(master=root, text="Welcome to Chosen Network", font=("Times New Roman", 30, "bold"), justify=CENTER, bg="light gray")
        welcome.pack(side=TOP, pady=30)

#Created an expandable text box with dimensions 40x40 displaying the API Response
        text_box = Text(root, height=40, width=40)
        text_box.pack(expand=True)
        text_box.insert('end',"API Response:")
#Created the fwdbutton, which runs the output of the fwd() API in the textbox once the user clicks the Forward button using the functions show_response() and send_request()
        fwdbutton = Button(master=frame1, text="Forward", font=("Arial", 14), justify=CENTER, fg="blue", bg="blue", 
                           command=lambda: self.show_response(text_box, self.send_request('http://127.0.0.1:5000/fwd')))
        fwdbutton.grid(column=1,row=3)
#Created the bwdbutton, which runs the output of the bwd() API in the textbox once the user clicks the Backward button using the functions show_response() and send_request()
        bwdbutton = Button(master=frame1, text="Backward", font=("Arial", 14), justify=CENTER, fg="blue", bg="blue", command=lambda: self.show_response(text_box, self.send_request('http://127.0.0.1:5000/bwd')))
        bwdbutton.grid(column=2,row=3)
#Created the leftbutton, which runs the output of the left() API in the textbox once the user clicks the Left button using the functions show_response() and send_request()           
        leftbutton = Button(master=frame1, text="Left", font=("Arial", 14), justify=CENTER, fg="blue", bg="blue", command=lambda: self.show_response(text_box, self.send_request('http://127.0.0.1:5000/left')))
        leftbutton.grid(column=3,row=3)
#Created the rightbutton, which runs the output of the right() API in the textbox once the user clicks the Right button using the functions show_response() and send_request()
        rightbutton = Button(master=frame1, text="Right", font=("Arial", 14), justify=CENTER, fg="blue", bg="blue", command=lambda: self.show_response(text_box, self.send_request('http://127.0.0.1:5000/right')))
        rightbutton.grid(column=4,row=3)
#Created the stopbutton, which runs the output of the stop() API in the textbox once the user clicks the Stop button using the functions show_response() and send_request()
        stopbutton = Button(master=frame1, text="Stop", font=("Arial", 14), justify=CENTER, fg="blue", bg="blue", command=lambda: self.show_response(text_box, self.send_request('http://127.0.0.1:5000/stop')))
        stopbutton.grid(column=5,row=3)

#Makes sure the tkinter window keeps on running
        root.mainloop()

