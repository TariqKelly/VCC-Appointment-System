import os
import sqlite3
from tkinter import *
from tkinter import ttk, messagebox

with sqlite3.connect("database.db") as db:
    cursor = db.cursor()


#Run the User Validation Function
def sign_up():
    if sys.platform.startswith('darwin'):
        os.system("python3 SignUp.py")
    else:
        os.system("python SignUp.py")

#Run the Patient Management Function
def manage_patients():
    if sys.platform.startswith('darwin'):
        os.system("python3 DatabaseManagement.py")
    else:
        os.system("python DatabaseManagement.py")

#Run the Appointment Management Function
def manage_appointments():
    if sys.platform.startswith('darwin'):
        os.system("python3 AppointmentScheduler.py")
    else:
        os.system("python AppointmentScheduler.py")



#Run the Report Generation Function
def generate_report():
    if sys.platform.startswith('darwin'):
        os.system("python3 ReportGeneration.py")
    else:
        os.system("python ReportGeneration.py")

# Validate Login
def validate_login():
    newLoginID = login_id.get()
    newPassword = password.get()

    cursor.execute("SELECT COUNT(*) from user_data WHERE login_id='" + newLoginID + "' AND password='" + newPassword + "'" )
    result = cursor.fetchone()
    if int(result[0]) == 1:
        login_successful()
    else:
        messagebox.showwarning("Incorrect Credentials", "Incorrect Credentials: Please Try Again")


#Reset Password Function
def reset_pass():
    resetWindow = Toplevel()
    resetWindow.title("Reset Password")

    id_label = Label(resetWindow, text="Login ID:", font='Helvetica 14 bold')
    id_label.grid(row = 1, column = 0, padx=10, pady=10)
    #
    id_label_ent = Entry(resetWindow, width=20)
    id_label_ent.grid(row = 1, column = 1, padx=10, pady=10)

    #Secret Question
    ques_label = Label(resetWindow, text="Secret Question:", font='Helvetica 14 bold')
    ques_label.grid(row = 2, column = 0, padx=10, pady=10)

    # List of questions
    OptionList = ["What Is The Name Of Your First Pet?","What Is Your Mother's Maiden Name?"]

    # OptionMenu
    reset_var = StringVar(resetWindow)
    reset_var.set(OptionList[0])

    opt = OptionMenu(resetWindow, reset_var, *OptionList)
    opt.config(width=30, font=('Helvetica', 14))
    opt.grid(row = 2, column = 1, padx=10, pady=10)
    ques_num = 0


    def callback(*args):
        for i in range(len(OptionList)):  # assign question number to for query in the database
            if OptionList[i] == reset_var.get():
                break

        ques_num = i
        print(str(ques_num) + ": " + OptionList[i])


    reset_var.trace("w", callback)

    answer = Label(resetWindow, text="Your Answer:", font='Helvetica 14 bold')
    answer.grid(row = 3, column = 0, padx=10, pady=10)

    answer_ent = Entry(resetWindow, width=20)
    answer_ent.grid(row = 3, column = 1, padx=10, pady=10)

    new_pass = Label(resetWindow, text="New Password:", font='Helvetica 14 bold', fg='black')
    new_pass.grid(row = 4, column = 0, padx=10, pady=10)

    new_pass_ent = Entry(resetWindow, width=20, show='•')
    new_pass_ent.grid(row = 4, column = 1, padx=10, pady=10)


    def subAnswerSecretQues():
            currentID = id_label_ent.get()
            ans = answer_ent.get()
            newPass = new_pass_ent.get()

            # add sql query here:
            cursor.execute("SELECT COUNT(*) from user_data WHERE login_id='" + currentID + "' AND secret_answer='" + ans + "' ")
            result = cursor.fetchone()
            if id_label_ent.get() == "" or answer_ent.get() == "" or new_pass_ent.get() == "":
                messagebox.showwarning("Fields Empty", "Warning: No Fields Should Be Empty.")
            elif int(result[0]) == 0:
                messagebox.showwarning("Incorrect Credentials", "Incorrect Credentials: Please Try Again")
            else:
                messagebox.showinfo("Success", "Password Successfully Updated!")
                cursor.execute("UPDATE user_data SET password=? where login_id=?",(newPass, currentID, ))
                db.commit()
            # button to submit the answers

    submit_answer = Button(resetWindow, text="Submit",
                           command=subAnswerSecretQues)
    submit_answer.grid(row = 5, columnspan = 2, padx=10, pady=10,ipadx=20)

    # Reset Attempt Message
    reset_attempt_message = Message(resetWindow,text="", width=300)
    reset_attempt_message.grid(row=6, columnspan=2, pady=10)


def login_successful():
    home_window = Toplevel()
    home_window.title("Welcome - VCC Patient Management System")
    home_frame = LabelFrame(home_window,padx=10,pady=10)
    master = home_frame
    home_frame.pack()

    def exit_btn():
        home_window.destroy()
        home_window.update()


    # Insert Company Logo
    img = PhotoImage(file="images/VCC-Logo.png")
    label = Label(master, image=img)
    label.grid(row=0, columnspan=2)
    label.img_ref=img

    # Display Welcome Message
    welcome_message = Label(master,text="Manage Patient Records", font='Helvetica 30 bold',fg='#596ebb')
    welcome_message.grid(row=1, columnspan=2, padx=10, pady=10)

    # Display Welcome Message To User
    welcome_message2 = Label(master, text="Welcome, " + login_id.get(),font='Helvetica 24 bold',fg='#56565c')
    welcome_message2.grid(row=2, columnspan=2, padx=10, pady=10)

    # Manage Patient Button
    manage_patients_button = Button(master,text="Manage Patients", width=15, command=manage_patients)
    manage_patients_button.grid(row=7, column=0, padx=10, pady=10, ipadx=30, ipady=20, sticky='e')

    # Manage Appointments
    manage_appointments_button = Button(master,text="Manage Appointments", width=15, command=manage_appointments)
    manage_appointments_button.grid(row=7, column=1, padx=10, pady=10, ipadx=30, ipady=20, sticky='w')

    # Generate A Report
    generate_report_button = Button(master,text="Generate A Report", width=15, command=generate_report)
    generate_report_button.grid(row=8, column=0, padx=10, pady=10, ipadx=30, ipady=20, sticky='e')

    # Log Out Button
    log_out_button = Button(master,text="Log Out", width=15, command=exit_btn)
    log_out_button.grid(row=8, column=1, padx=10, pady=10, ipadx=30, ipady=20, sticky='w')


###################################################################################################

#Set Up UI Screen
main_window = Tk()
main_window.title("Patient Management System")


#Designate Screen Size
app_width = 800
app_height = 800
screen_width = main_window.winfo_screenwidth()
screen_height = main_window.winfo_screenheight()
x = (screen_width/2) - (app_width/2)
y = (screen_height/2) - (app_height/2)
main_window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

main_window_frame = LabelFrame(main_window)
main_window_frame.pack(padx=10,pady=10)
master = main_window_frame

#Insert Company Logo
img = PhotoImage(file="images/VCC-Logo.png")
main_window.iconbitmap('images/VCC-Icon.ico')
label = Label(master, image=img)
label.grid(row = 0, columnspan = 2)

#Display Welcome Message
welcome_message = Label(master,text="Welcome to our Patient Management System", font='Helvetica 30 bold',fg='#596ebb')
welcome_message.grid(row = 1, columnspan = 2, padx=10, pady=10)

#Display Heading For Log In
login_message = Label(master,text="Please Log In ", font='Helvetica 24 bold',fg='#56565c')
login_message.grid(row = 2, columnspan = 2, padx=10, pady=20)

#Enter Username
label1 = Label(master,text="Enter Username:", font='Helvetica 16 bold',fg='#56565c')
label1.grid(row = 3, column = 0, padx=10, pady=10,sticky='e')
#
login_id = Entry(master,text="")
login_id.grid(row = 3, column = 1, padx=10, pady=10,sticky='w')

#Enter Password
label2 = Label(master,text="Enter Password:", font='Helvetica 16 bold',fg='#56565c')
label2.grid(row = 4, column = 0, padx=10, pady=10,sticky='e')
#
password = Entry(master,text="",show='•')
password.grid(row = 4, column = 1, padx=10, pady=10,sticky='w')

login_btn = Button(master,text="Log In",command=validate_login)
login_btn.grid(row = 5, columnspan = 2, padx=10, pady=20,ipadx=40, ipady=10)

reset_password_btn = Button(master,text="Forgot Password?",command=reset_pass)
reset_password_btn.grid(row = 6, columnspan = 2, padx=10)

#Display Heading For Sign Up Button
login_message = Label(master,text="Don't Have An Account? ", font='Helvetica 10')
login_message.grid(row = 7, columnspan = 2, padx=10, pady=10)

sign_up_button = Button(master,text="Sign Up",command = sign_up)
sign_up_button.grid(row = 8, columnspan = 2, padx=10,ipadx=20, ipady=10)


main_window.mainloop()