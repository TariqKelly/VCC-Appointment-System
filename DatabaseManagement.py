from tkinter import *
from tkinter import ttk, messagebox

import sqlite3

with sqlite3.connect("database.db") as db:
    cursor = db.cursor()

# patient_id
# first_name
# last_name
# tel_num
# email_address

# Create Database Table for Patients
cursor.execute("""CREATE TABLE IF NOT EXISTS patients(patient_id integer PRIMARY KEY AUTOINCREMENT, first_name text 
NOT NULL, last_name text NOT NULL, tel_num text NOT NULL, email_address text NOT NULL); """)

###################### MAIN FUNCTIONS ###########################


# Update Patient - Window
"""
def update_patient_window():
    update_patient_window = Toplevel(add_patient_window)
    update_patient_window.title("VCC Appointments - Update Patient Record ")
    canvas = Canvas(update_patient_window, height = HEIGHT, width = WIDTH)
    canvas.pack()
"""


# Add New Patient
def add_new_patient():
    add_patient_window = Tk()
    add_patient_window.title("VCC Appointments - Add New Patient ")
    add_patient_window.geometry("800x800")

    # Heading Label
    heading = Label(add_patient_window, text="Add New Patient", font='Helvetica 18 bold')
    heading.grid(row=0, columnspan=2, padx=10, pady=10)

    # Enter First Name
    label1 = Label(add_patient_window, text="Enter Patient First Name:", font='Helvetica 14 bold')
    label1.grid(row=1, column=0, padx=10, pady=10, sticky='w')
    #
    first_name = Entry(add_patient_window, text="")
    first_name.grid(row=1, column=1, padx=40, pady=20)

    # Enter Last Name
    label2 = Label(add_patient_window, text="Enter Patient Last Name:", font='Helvetica 14 bold')
    label2.grid(row=2, column=0, padx=10, pady=10, sticky='w')
    #
    last_name = Entry(add_patient_window, text="")
    last_name.grid(row=2, column=1, padx=40, pady=20)

    # Enter Phone Number
    label3 = Label(add_patient_window, text="Enter Patient Phone Number:", font='Helvetica 14 bold')
    label3.grid(row=3, column=0, padx=10, pady=10, sticky='w')
    #
    tel_num = Entry(add_patient_window, text="")
    tel_num.grid(row=3, column=1, padx=40, pady=20)

    # Enter Email Address
    label4 = Label(add_patient_window, text="Enter Patient Email Address:", font='Helvetica 14 bold')
    label4.grid(row=4, column=0, padx=10, pady=10, sticky='w')
    #
    email_address = Entry(add_patient_window, text="")
    email_address.grid(row=4, column=1, padx=40, pady=20)

    # Button To Update Patient
    # update_patient_button = Button(text="Update Patient Record", command=lambda: update_patient_window())
    # update_patient_button.grid(row=3, column=3, padx=20, ipady=10)

    def submitPatient():
        newFirstName = first_name.get()
        newLastName = last_name.get()
        newTelNum = tel_num.get()
        newEmailAddress = email_address.get()

        cursor.execute(
            "SELECT COUNT(*) from patients WHERE email_address='" + newEmailAddress + "' OR tel_num='" + newTelNum + "' ")
        result = cursor.fetchone()
        if int(result[0]) > 0:
            success["text"] = "Sorry, this user has already been registered."
        else:
            success["text"] = "New Patient Created Successfully."
            cursor.execute("INSERT INTO patients(first_name,last_name,tel_num,email_address)VALUES(?,?,?,?)",
                           (newFirstName, newLastName, newTelNum, newEmailAddress))
        db.commit()

    # Button To Add Patient To Database
    create_patient_button = Button(add_patient_window, text="Create Patient Record", command=submitPatient)
    create_patient_button.grid(row=5, columnspan=2, padx=20, ipady=10)

    # Success Message
    success = Message(add_patient_window, text="", width=300)
    success.grid(row=6, columnspan=2, pady=10)


def display_patient():
    display_patient_window = Tk()
    display_patient_window.title("VCC Appointments - View Patient Record ")
    display_patient_window.geometry("800x800")

    row = None
    master = display_patient_window

    # Heading Label
    heading = Label(master, text="View Patient Record", font='Helvetica 18 bold')
    heading.grid(row=0, columnspan=2, padx=10, pady=10)

    # Search Criteria --> Email Address
    searchEmailLabel = Label(master, text="Enter Patient's Email:", font='Helvetica 14 bold')
    searchEmailLabel.grid(row=1, column=0, padx=10, pady=10, sticky='e')
    #
    search_email = Entry(master, width=30)
    search_email.grid(row=1, column=1, padx=10, pady=10)

    # Function To Perform Search
    def search_db():
        input = search_email.get()

        # Execute SQL
        sql = "SELECT * FROM patients WHERE email_address LIKE ?"
        res = cursor.execute(sql, (input,))
        for row in res:
            patient_id1 = row[0]
            first_name1 = row[1]
            last_name1 = row[2]
            tel_num1 = row[3]
            email_address1 = row[4]

        # Creating the Display Data

        # Display Patient ID
        label0 = Label(master, text="Patient ID:", font='Helvetica 14 bold')
        label0.grid(row=3, column=0, padx=10, pady=10, sticky='e')
        #
        patient_id = Label(master, text=patient_id1, font='Helvetica 14')
        patient_id.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        # Display First Name
        label1 = Label(master, text="First Name:", font='Helvetica 14 bold')
        label1.grid(row=4, column=0, padx=10, pady=10, sticky='e')
        #
        first_name = Label(master, text=first_name1, font='Helvetica 14')
        first_name.grid(row=4, column=1, padx=10, pady=10, sticky='w')

        # Display Last Name
        label2 = Label(master, text="Last Name:", font='Helvetica 14 bold')
        label2.grid(row=5, column=0, padx=10, pady=10, sticky='e')
        #
        last_name = Label(master, text=last_name1, font='Helvetica 14')
        last_name.grid(row=5, column=1, padx=10, pady=10, sticky='w')

        # Display Phone Number
        label3 = Label(master, text="Phone Number:", font='Helvetica 14 bold')
        label3.grid(row=6, column=0, padx=10, pady=10, sticky='e')
        #
        tel_num = Label(master, text=tel_num1, font='Helvetica 14')
        tel_num.grid(row=6, column=1, padx=10, pady=10, sticky='w')

        # Display Email Address
        label4 = Label(master, text="Email Address:", font='Helvetica 14 bold')
        label4.grid(row=7, column=0, padx=10, pady=10, sticky='e')
        #
        email_address = Label(master, text=email_address1, font='Helvetica 14')
        email_address.grid(row=7, column=1, padx=10, pady=10, sticky='w')

    # Search Button
    search = Button(master, text="Search Patient Database", width=18, height=2, command=search_db)
    search.grid(row=2, columnspan=2, padx=10, pady=10)


def update_patient():
    update_patient_window = Tk()
    update_patient_window.title("VCC Appointments - View Patient Record ")
    update_patient_window.geometry("800x800")

    row = None
    master = update_patient_window

    # Heading Label
    heading = Label(master, text="Update Patient Record", font='Helvetica 18 bold')
    heading.grid(row=0, columnspan=2, padx=10, pady=10)

    # Search Criteria --> Email Address
    searchEmailLabel = Label(master, text="Enter Patient's Email:", font='Helvetica 14 bold')
    searchEmailLabel.grid(row=1, column=0, padx=10, pady=10, sticky='e')
    #
    search_email = Entry(master, width=30)
    search_email.grid(row=1, column=1, padx=10, pady=10)

    # Function To Perform Search
    def search_db():
        input = search_email.get()

        # Execute SQL
        sql = "SELECT * FROM patients WHERE email_address LIKE ?"
        res = cursor.execute(sql, (input,))
        for row in res:
            first_name1 = row[1]
            last_name1 = row[2]
            tel_num1 = row[3]
            email_address1 = row[4]

        # Creating the Update Fields

        # Update First Name
        label1 = Label(master, text="First Name:", font='Helvetica 14 bold')
        label1.grid(row=3, column=0, padx=10, pady=10, sticky='e')
        #
        first_name = Entry(master, width=30)
        first_name.insert(END, str(first_name1))
        first_name.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        # Update Last Name
        label2 = Label(master, text="Last Name:", font='Helvetica 14 bold')
        label2.grid(row=4, column=0, padx=10, pady=10, sticky='e')
        #
        last_name = Entry(master, width=30)
        last_name.insert(END, str(last_name1))
        last_name.grid(row=4, column=1, padx=10, pady=10, sticky='w')

        # Update Phone Number
        label3 = Label(master, text="Phone Number:", font='Helvetica 14 bold')
        label3.grid(row=5, column=0, padx=10, pady=10, sticky='e')
        #
        tel_num = Entry(master, width=30)
        tel_num.insert(END, str(tel_num1))
        tel_num.grid(row=5, column=1, padx=10, pady=10, sticky='w')

        # Update Email Address
        label4 = Label(master, text="Email Address:", font='Helvetica 14 bold')
        label4.grid(row=6, column=0, padx=10, pady=10, sticky='e')
        #
        email_address = Entry(master, width=30)
        email_address.insert(END, str(email_address1))
        email_address.grid(row=6, column=1, padx=10, pady=10, sticky='w')

        # Function To Update Record
        def update_db():
            # declaring the variables to update
            var1 = first_name.get()  # Updated First Name
            var2 = last_name.get()  # Updated Last Name
            var3 = tel_num.get()  # Updated Phone Number
            var4 = email_address.get()  # Updated Email Address

            query = "UPDATE patients SET first_name=?, last_name=?, tel_num=?, email_address=? WHERE email_address=?"
            cursor.execute(query, (var1, var2, var3, var4, search_email.get(),))
            db.commit()
            messagebox.showinfo("Updated", "Successfully Updated.")

        # Update Button
        update = Button(master, text="Update Patient Record", width=18, height=2, command=update_db)
        update.grid(row=7, columnspan=2, padx=10, pady=10, ipady=10)

    # Search Button
    search = Button(master, text="Search Patient Database", width=18, height=2, command=search_db)
    search.grid(row=2, columnspan=2, padx=10, pady=10)


def delete_patient():
    delete_patient_window = Tk()
    delete_patient_window.title("VCC Appointments - Delete Patient Record ")
    delete_patient_window.geometry("800x800")

    row = None
    master = delete_patient_window

    # Heading Label
    heading = Label(master, text="Delete Patient Record", font='Helvetica 18 bold')
    heading.grid(row=0, columnspan=2, padx=10, pady=10)

    # Search Criteria --> Email Address
    searchEmailLabel = Label(master, text="Enter Patient's Email:", font='Helvetica 14 bold')
    searchEmailLabel.grid(row=1, column=0, padx=10, pady=10, sticky='e')
    #
    search_email = Entry(master, width=30)
    search_email.grid(row=1, column=1, padx=10, pady=10)

    # Function To Perform Search
    def search_db():

        input = search_email.get()

        # Execute SQL
        sql = "SELECT * FROM patients WHERE email_address LIKE ?"
        res = cursor.execute(sql, (input,))
        for row in res:
            patient_id1 = row[0]
            first_name1 = row[1]
            last_name1 = row[2]
            tel_num1 = row[3]
            email_address1 = row[4]

        # Creating the Display Data

        # Display Patient ID
        label0 = Label(master, text="Patient ID:", font='Helvetica 14 bold')
        label0.grid(row=3, column=0, padx=10, pady=10, sticky='e')
        #
        patient_id = Label(master, text=patient_id1, font='Helvetica 14')
        patient_id.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        # Display First Name
        label1 = Label(master, text="First Name:", font='Helvetica 14 bold')
        label1.grid(row=4, column=0, padx=10, pady=10, sticky='e')
        #
        first_name = Label(master, text=first_name1, font='Helvetica 14')
        first_name.grid(row=4, column=1, padx=10, pady=10, sticky='w')

        # Display Last Name
        label2 = Label(master, text="Last Name:", font='Helvetica 14 bold')
        label2.grid(row=5, column=0, padx=10, pady=10, sticky='e')
        #
        last_name = Label(master, text=last_name1, font='Helvetica 14')
        last_name.grid(row=5, column=1, padx=10, pady=10, sticky='w')

        # Display Phone Number
        label3 = Label(master, text="Phone Number:", font='Helvetica 14 bold')
        label3.grid(row=6, column=0, padx=10, pady=10, sticky='e')
        #
        tel_num = Label(master, text=tel_num1, font='Helvetica 14')
        tel_num.grid(row=6, column=1, padx=10, pady=10, sticky='w')

        # Display Email Address
        label4 = Label(master, text="Email Address:", font='Helvetica 14 bold')
        label4.grid(row=7, column=0, padx=10, pady=10, sticky='e')
        #
        email_address = Label(master, text=email_address1, font='Helvetica 14')
        email_address.grid(row=7, column=1, padx=10, pady=10, sticky='w')

        def delete_db():
            if messagebox.askyesno("Confirm Deletion", "Delete record of "+first_name1+"? "):
                # delete the appointment
                sql2 = "DELETE FROM patients WHERE email_address = ?"
                cursor.execute(sql2, (search_email.get(),))
                db.commit()
                messagebox.showinfo("Success", "Deleted Successfully")

        # Delete Button
        delete = Button(master, text="Delete Patient Record", width=18, height=2, command=delete_db)
        delete.grid(row=8, columnspan=2, padx=10, pady=10)

    # Search Button
    search = Button(master, text="Search Patient Database", width=18, height=2, command=search_db)
    search.grid(row=2, columnspan=2, padx=10, pady=10)


#########################################################################
# Set Up UI Screen
manage_db_window = Tk()
manage_db_window.title("Patient Records Management")

# Designate Screen Size
app_width = 500
app_height = 620
screen_width = manage_db_window.winfo_screenwidth()
screen_height = manage_db_window.winfo_screenheight()
x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height / 2)
manage_db_window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

# Insert Company Logo
img = PhotoImage(file="images/Logo.png")
label = Label(manage_db_window, image=img)
label.grid(row=0, columnspan=2)

# Display Welcome Message
welcome_message = Label(text="Manage Patient Records", font='Helvetica 30 bold')
welcome_message.grid(row=1, columnspan=2, padx=10, pady=10)

# Add Patient Button
add_patient_button = Button(text="Add Patient Record",width=15, command=add_new_patient)
add_patient_button.grid(row=7, column=0, padx=10, pady=10, ipadx=30, ipady=20, sticky='e')

# Display Patient Button
display_patient_button = Button(text="View Patient Record",width=15, command=display_patient)
display_patient_button.grid(row=7, column=1, padx=10, pady=10, ipadx=30, ipady=20, sticky='w')

# Update Patient Button
update_patient_button = Button(text="Update Patient Record",width=15, command=update_patient)
update_patient_button.grid(row=8, column=0, padx=10, pady=10, ipadx=30, ipady=20, sticky='e')

# Delete Patient Button
delete_patient_button = Button(text="Delete Patient Record",width=15, command=delete_patient)
delete_patient_button.grid(row=8, column=1, padx=10, pady=10, ipadx=30, ipady=20, sticky='w')

manage_db_window.mainloop()
