from datetime import date
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar, DateEntry

import sqlite3

with sqlite3.connect("database.db") as db:
    cursor = db.cursor()
db.set_trace_callback(print)
# appt_id
# appt_date
# appt_time
# patient_id
# appt_status - Missed, Completed, Upcoming


# Create Database Table for Patients
cursor.execute("""CREATE TABLE IF NOT EXISTS appointments(appt_id integer PRIMARY KEY AUTOINCREMENT, appt_date text 
NOT NULL, appt_time text NOT NULL, appt_status text NOT NULL,patient_id integer, FOREIGN KEY(patient_id) REFERENCES 
patients(patient_id)); """)

###################### MAIN FUNCTIONS ###########################


# Add New Appointment
def add_new_appointment():
    add_appointment_window = Tk()
    add_appointment_window.title("VCC Appointments - Add New Appointment ")
    add_appointment_window.geometry("800x800")


    # Enter Appointment Date
    label1 = Label(add_appointment_window, text="Enter Appointment Date:", font='Helvetica 14 bold')
    label1.grid(row=0, column=0, padx=10, pady=10, sticky='w')
    #
    appt_date = DateEntry(add_appointment_window, width=12, background='white',foreground='darkblue', borderwidth=2,mindate=date.today())
    appt_date.grid(row=0, column=1, padx=40, pady=20)


    # Enter Appointment Time
    timeOptions = ["9:00 AM","9:30 AM","10:00 AM","10:30 AM","11:00 AM","11:30 AM","12:00 PM","12:30 PM","1:00 PM","1:30 PM","2:00 PM","2:30 PM","3:00 PM","3:30 PM","4:00 PM","4:30 PM"]
    label2 = Label(add_appointment_window, text="Enter Appointment Time:", font='Helvetica 14 bold')
    label2.grid(row=1, column=0, padx=10, pady=10, sticky='w')

    #
    def callbackFunc(event):
        appt_time = event.widget.get()
        print(appt_time)

    appt_time = ttk.Combobox(add_appointment_window, value=timeOptions, width=25)
    appt_time.current(0)
    appt_time.bind("<<ComboboxSelected>>", callbackFunc)
    appt_time.grid(row=1, column=1, padx=40, pady=20)

    # Enter Email Address
    label4 = Label(add_appointment_window, text="Enter Patient Email Address:", font='Helvetica 14 bold')
    label4.grid(row=2, column=0, padx=10, pady=10, sticky='w')
    #
    email_address = Entry(add_appointment_window, text="")
    email_address.grid(row=2, column=1, padx=40, pady=20)

    def submitAppointment():
        newApptDate = appt_date.get()
        newApptTime = appt_time.get()
        patEmailAddress = email_address.get()
        apptStatus = "Upcoming"

        def getPatID():
            cursor.execute("SELECT patient_id from patients WHERE email_address='" + patEmailAddress + "'")
            patID= cursor.fetchone()[0]
            return patID

        cursor.execute(
            "SELECT COUNT(*) from appointments WHERE appt_date='" + newApptDate + "' AND appt_time='" + newApptTime + "' ")
        result = cursor.fetchone()
        if int(result[0]) > 0:
            messagebox.showwarning("Error","Error: Appointment Slot Occupied")
        else:
            messagebox.showinfo("Success","New Appointment Successfully Added")
            cursor.execute("INSERT INTO appointments(appt_date, appt_time, appt_status, patient_id)VALUES(?,?,?,?)",
                           (newApptDate, newApptTime, apptStatus, getPatID()))
        db.commit()

    # Button To Add Patient To Database
    create_appointment_button = Button(add_appointment_window, text="Create Appointment", command=submitAppointment)
    create_appointment_button.grid(row=3, columnspan=2, padx=20, ipady=10)



# Display Appointments
def display_appointment():
    display_appointment_window = Tk()
    display_appointment_window.title("VCC Appointments - View Patient Appointments ")
    display_appointment_window.geometry("800x800")

    row = None
    master = display_appointment_window

    # Heading Label
    heading = Label(master, text="View Patient Appointments", font='Helvetica 18 bold')
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

        def getPatID():
            cursor.execute("SELECT patient_id from patients WHERE email_address='" + input + "'")
            patID= cursor.fetchone()[0]
            return patID

        # Execute SQL
        sql = "SELECT * FROM appointments WHERE patient_id LIKE ?"
        res = cursor.execute(sql, (getPatID(),))
        for row in res:
            appt_date1 = row[1]
            appt_time1 = row[2]
            appt_status1 = row[3]

        # Creating the Display Data

        # Display Appointment Date
        label0 = Label(master, text="Date:", font='Helvetica 14 bold')
        label0.grid(row=3, column=0, padx=10, pady=10, sticky='e')
        #
        appt_date = Label(master, text=appt_date1, font='Helvetica 14')
        appt_date.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        # Display Appointment Time
        label1 = Label(master, text="Time:", font='Helvetica 14 bold')
        label1.grid(row=4, column=0, padx=10, pady=10, sticky='e')
        #
        appt_time = Label(master, text=appt_time1, font='Helvetica 14')
        appt_time.grid(row=4, column=1, padx=10, pady=10, sticky='w')

        # Display Appointment Status
        label2 = Label(master, text="Status:", font='Helvetica 14 bold')
        label2.grid(row=5, column=0, padx=10, pady=10, sticky='e')
        #
        appt_status = Label(master, text=appt_status1, font='Helvetica 14')
        appt_status.grid(row=5, column=1, padx=10, pady=10, sticky='w')

    # Search Button
    search = Button(master, text="Search Appointments", width=18, height=2, command=search_db)
    search.grid(row=2, columnspan=2, padx=10, pady=10)

# Update Appointment
def update_appointment():
    update_appointment_window = Tk()
    update_appointment_window.title("VCC Appointments - Update Appointment ")
    update_appointment_window.geometry("800x800")

    row = None
    master = update_appointment_window

    # Heading Label
    heading = Label(master, text="Update Appointment", font='Helvetica 18 bold')
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

        def getPatID():
            cursor.execute("SELECT patient_id from patients WHERE email_address='" + input + "'")
            patID = cursor.fetchone()[0]
            return patID


        # Execute SQL
        sql = "SELECT * FROM appointments WHERE patient_id LIKE ?"
        res = cursor.execute(sql, (getPatID(),))
        for row in res:
            appt_date1 = row[1]
            appt_time1 = row[2]
            appt_status1 = row[3]

        # Creating the Update Fields

        # Update Appt Date
        label1 = Label(master, text="Appointment Date:", font='Helvetica 14 bold')
        label1.grid(row=3, column=0, padx=10, pady=10, sticky='e')
        #
        appt_date = Entry(master, width=30)
        appt_date.insert(END, str(appt_date1))
        appt_date.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        # Update Appt Time
        label2 = Label(master, text="Appointment Time:", font='Helvetica 14 bold')
        label2.grid(row=4, column=0, padx=10, pady=10, sticky='e')
        #
        appt_time = Entry(master, width=30)
        appt_time.insert(END, str(appt_time1))
        appt_time.grid(row=4, column=1, padx=10, pady=10, sticky='w')

        # Update Appt Status
        label3 = Label(master, text="Appointment Status:", font='Helvetica 14 bold')
        label3.grid(row=5, column=0, padx=10, pady=10, sticky='e')
        #
        appt_status = Entry(master, width=30)
        appt_status.insert(END, str(appt_status1))
        appt_status.grid(row=5, column=1, padx=10, pady=10, sticky='w')

        # Function To Update Record
        def update_db():

            def getAptID():
                cursor.execute(
                    "SELECT appt_id from appointments WHERE appt_date='" + appt_date1 + "' AND appt_time='" + appt_time1 + "' ")
                aptID = cursor.fetchone()[0]
                return aptID

            # declaring the variables to update
            var1 = appt_date.get()  # Updated Date
            var2 = appt_time.get()  # Updated Time
            var3 = appt_status.get()  # Updated Status

            query = "UPDATE appointments SET appt_date=?, appt_time=?, appt_status=? WHERE appt_id=?"

            cursor.execute(
                "SELECT COUNT(*) from appointments WHERE appt_date='" + var1 + "' AND appt_time='" + var2 + "' ")
            result = cursor.fetchone()
            if int(result[0]) > 0:
                messagebox.showwarning("Error","Error: Appointment Slot Occupied")
            else:
                messagebox.showinfo("Updated", "Successfully Updated.")
                cursor.execute(query, (var1, var2, var3, getAptID(),))
            db.commit()


        # Update Button
        update = Button(master, text="Update Appointment", width=18, height=2, command=update_db)
        update.grid(row=6, columnspan=2, padx=10, pady=10, ipady=10)

    # Search Button
    search = Button(master, text="Search Patient Database", width=18, height=2, command=search_db)
    search.grid(row=2, columnspan=2, padx=10, pady=10)

# Delete Appointment
def delete_appointment():
    display_appointment_window = Tk()
    display_appointment_window.title("VCC Appointments - Delete Patient Appointments ")
    display_appointment_window.geometry("800x800")

    row = None
    master = display_appointment_window

    # Heading Label
    heading = Label(master, text="Delete Appointment", font='Helvetica 18 bold')
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

        def getPatID():
            cursor.execute("SELECT patient_id from patients WHERE email_address='" + input + "'")
            patID = cursor.fetchone()[0]
            return patID

        # Execute SQL
        sql = "SELECT * FROM appointments WHERE patient_id LIKE ?"
        res = cursor.execute(sql, (getPatID(),))
        for row in res:
            appt_date1 = row[1]
            appt_time1 = row[2]
            appt_status1 = row[3]

        # Creating the Display Data

        # Display Appointment Date
        label0 = Label(master, text="Date:", font='Helvetica 14 bold')
        label0.grid(row=3, column=0, padx=10, pady=10, sticky='e')
        #
        appt_date = Label(master, text=appt_date1, font='Helvetica 14')
        appt_date.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        # Display Appointment Time
        label1 = Label(master, text="Time:", font='Helvetica 14 bold')
        label1.grid(row=4, column=0, padx=10, pady=10, sticky='e')
        #
        appt_time = Label(master, text=appt_time1, font='Helvetica 14')
        appt_time.grid(row=4, column=1, padx=10, pady=10, sticky='w')

        # Display Appointment Status
        label2 = Label(master, text="Status:", font='Helvetica 14 bold')
        label2.grid(row=5, column=0, padx=10, pady=10, sticky='e')
        #
        appt_status = Label(master, text=appt_status1, font='Helvetica 14')
        appt_status.grid(row=5, column=1, padx=10, pady=10, sticky='w')

        def delete_db():
            def getAptID():
                cursor.execute(
                    "SELECT appt_id from appointments WHERE appt_date='" + appt_date1 + "' AND appt_time='" + appt_time1 + "' ")
                aptID = cursor.fetchone()[0]
                return aptID

            if messagebox.askyesno("Confirm Deletion", "Delete appointment for "+input+"? "):
                # delete the appointment
                sql2 = "DELETE FROM appointments WHERE appt_id = ?"
                cursor.execute(sql2, (getAptID(),))
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
appointment_window = Tk()
appointment_window.title("Appointment Management")

# Designate Screen Size
app_width = 500
app_height = 620
screen_width = appointment_window.winfo_screenwidth()
screen_height = appointment_window.winfo_screenheight()
x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height / 2)
appointment_window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

# Insert Company Logo
img = PhotoImage(file="images/Logo.png")
label = Label(appointment_window, image=img)
label.grid(row=0, columnspan=2)

# Display Welcome Message
welcome_message = Label(text="Manage Appointments", font='Helvetica 30 bold')
welcome_message.grid(row=1, columnspan=2, padx=10, pady=10)

# Add Patient Button
add_patient_button = Button(text="Add New Appointment",width=15, command=add_new_appointment)
add_patient_button.grid(row=7, column=0, padx=10, pady=10, ipadx=30, ipady=20, sticky='e')

# Display Patient Button
display_patient_button = Button(text="View Patient Appointments",width=15, command=display_appointment)
display_patient_button.grid(row=7, column=1, padx=10, pady=10, ipadx=30, ipady=20, sticky='w')

# Update Patient Button
update_patient_button = Button(text="Update Appointment",width=15, command=update_appointment)
update_patient_button.grid(row=8, column=0, padx=10, pady=10, ipadx=30, ipady=20, sticky='e')

# Delete Patient Button
delete_patient_button = Button(text="Delete Appointment",width=15, command=delete_appointment)
delete_patient_button.grid(row=8, column=1, padx=10, pady=10, ipadx=30, ipady=20, sticky='w')

appointment_window.mainloop()