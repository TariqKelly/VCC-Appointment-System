from tkinter import *
import sqlite3
from tkinter import ttk

with sqlite3.connect("database.db") as db:
    cursor = db.cursor()

#Create Database Table for Authorized Users
# Variables: id, user_fullname, user_email, login_id, password, secret_question, secret_answer
cursor.execute("""CREATE TABLE IF NOT EXISTS user_data(id integer PRIMARY KEY AUTOINCREMENT, user_fullname text NOT NULL, 
user_email text NOT NULL, login_id text NOT NULL, password text NOT NULL, secret_question text NOT NULL, 
secret_answer text NOT NULL); """)


# Add New User
def add_new_user():
    newUserfullname = user_fullname.get()
    newUseremail = user_email.get()
    newLoginID = login_id.get()
    newPassword = password.get()
    newSecretQues = secret_question.get()
    newSecretAns = secret_answer.get()

    cursor.execute("SELECT COUNT(*) from user_data WHERE login_id='" + newLoginID + "' ")
    result = cursor.fetchone()
    if int(result[0]) > 0:
        error["text"] = "Error: This Username Already Exists."
    else:
        error["text"] = "New Authorized User Created Successfully."
        cursor.execute("INSERT INTO user_data(user_fullname, user_email, login_id, password, secret_question, "
                       "secret_answer)VALUES(?,?,?,?,?,?)",(newUserfullname, newUseremail, newLoginID, newPassword,
                                                            newSecretQues,newSecretAns))
        db.commit()


###################################################################################################

sign_up_window = Tk()
sign_up_window.title("Add Authorized User")


#Designate Screen Size
app_width = 500
app_height = 480
screen_width = sign_up_window.winfo_screenwidth()
screen_height = sign_up_window.winfo_screenheight()
x = (screen_width/2) - (app_width/2)
y = (screen_height/2) - (app_height/2)
sign_up_window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')


#Display Heading For Log In Button
login_message = Label(text="Create Authorized User Account", font='Helvetica 24 bold')
login_message.grid(row = 0, columnspan = 2, padx=10, pady=20)

#Enter User Full Name
nameLabel = Label(text="Enter Name:",font='Helvetica 14 bold')
nameLabel.grid(row = 1, column = 0, padx=10, pady=10,sticky='e')
#
user_fullname = Entry(text="")
user_fullname.grid(row = 1, column = 1, padx=10, pady=10)

#Enter User Email user_email
emailLabel = Label(text="Enter Email Address:",font='Helvetica 14 bold')
emailLabel.grid(row = 2, column = 0, padx=10, pady=10,sticky='e')
#
user_email = Entry(text="")
user_email.grid(row = 2, column = 1, padx=10, pady=10)

#Enter Username login_id
loginIDLabel = Label(text="Enter Unique Username:",font='Helvetica 14 bold')
loginIDLabel.grid(row = 3, column = 0, padx=10, pady=10,sticky='e')
#
login_id = Entry(text="")
login_id.grid(row = 3, column = 1, padx=10, pady=10)


#Enter Password
passLabel = Label(text="Enter Password:",font='Helvetica 14 bold')
passLabel.grid(row = 4, column = 0, padx=10, pady=10,sticky='e')
#
password = Entry(text="",show='•')
password.grid(row = 4, column = 1, padx=10, pady=10)

#Enter Secret Question secret_question
SecretQuestionOptions = ["What Is The Name Of Your First Pet?","What Is Your Mother's Maiden Name?"]
secretQuesLabel = Label(text="Choose Your Secret Question:",font='Helvetica 14 bold')
secretQuesLabel.grid(row = 5, column = 0, padx=10, pady=10,sticky='e')
#
def callbackFunc(event):
    secret_question = event.widget.get()
    print(secret_question)

secret_question = ttk.Combobox(sign_up_window, value=SecretQuestionOptions, width=25)
secret_question.current(0)
secret_question.bind("<<ComboboxSelected>>",callbackFunc)
secret_question.grid(row=5,column=1)



#Enter Secret Answer secret_answer
secretAnsLabel = Label(text="Enter Unique Username:",font='Helvetica 14 bold')
secretAnsLabel.grid(row = 6, column = 0, padx=10, pady=10)
#
secret_answer = Entry(text="")
secret_answer.grid(row = 6, column = 1, padx=10, pady=10)




#Button To Add User To Database
button = Button(text="Add User", command=add_new_user)
button.grid(row = 7, columnspan = 2, pady=10, ipadx=20, ipady=10)

#Error Message
error = Message(text="",width=300)
error.grid(row = 8, columnspan = 2, pady=10)

sign_up_window.mainloop()
