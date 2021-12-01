from datetime import date
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar, DateEntry
import smtplib
from datetime import datetime

import sqlite3

with sqlite3.connect("database.db") as db:
    cursor = db.cursor()

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
        if newApptDate == "" or newApptTime == "" or patEmailAddress == "":
            messagebox.showwarning("Fields Empty", "Warning: No Fields Should Be Empty.")
        elif int(result[0]) > 0:
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
    # display_appointment_window.geometry("800x800")
    display_frame = LabelFrame(display_appointment_window, padx=10, pady=10)
    masterframe = display_frame
    display_frame.grid(row=2, columnspan=2, padx=10, pady=10)

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
    search_email.grid(row=1, column=1, padx=10, pady=10, sticky='w')

    # Function To Perform Search
    def search_db():
        input = search_email.get()

        def getPatID():
            cursor.execute("SELECT patient_id from patients WHERE email_address='" + input + "'")
            patID = cursor.fetchone()[0]
            return patID

        cursor.execute(
            "SELECT COUNT(*) from patients WHERE email_address='" + input + "' ")
        result = cursor.fetchone()
        if int(result[0]) == 0:
            messagebox.showwarning("Patient Not Found", "Patient Not Found. Please try again.")
            search_email.delete(0, END)
        else:
            cursor.execute(
                "SELECT COUNT(*) from appointments WHERE patient_id='" + str(getPatID()) + "' ")
            result = cursor.fetchone()

            if int(result[0]) == 0:
                messagebox.showwarning("Appointment Not Found", "No Appointment is Scheduled for this patient.")
                search_email.delete(0, END)


            sql = "SELECT * FROM appointments WHERE patient_id LIKE ?"
            res = cursor.execute(sql, (getPatID(),))
            i=0
            for row in res:
                i+=1
                appt_date1 = row[1]
                appt_time1 = row[2]
                appt_status1 = row[3]


                label0 = Label(masterframe, text="Date:", font='Helvetica 14 bold',width=10)
                label0.grid(row=i-1, column=0, padx=10, pady=10, sticky='w')
                #
                appt_date = Label(masterframe, text=appt_date1, font='Helvetica 14',width=10)
                appt_date.grid(row=i-1, column=1, padx=10, pady=10, sticky='w')

                # Display Appointment Time
                label1 = Label(masterframe, text="Time:", font='Helvetica 14 bold',width=10)
                label1.grid(row=i-1, column=2, padx=10, pady=10, sticky='w')
                #
                appt_time = Label(masterframe, text=appt_time1, font='Helvetica 14',width=10)
                appt_time.grid(row=i-1, column=3, padx=10, pady=10, sticky='w')

                # Display Appointment Status
                label2 = Label(masterframe, text="Status:", font='Helvetica 14 bold',width=10)
                label2.grid(row=i-1, column=4, padx=10, pady=10, sticky='w')
                #
                appt_status = Label(masterframe, text=appt_status1, font='Helvetica 14')
                appt_status.grid(row=i-1, column=5, padx=10, pady=10, sticky='w')


    # Search Button
    search = Button(master, text="Search Appointments", width=18, height=2, command=search_db)
    search.grid(row=3, columnspan=2, padx=10, pady=10)


# Update Appointment
def update_appointment():
    update_appointment_window = Toplevel()
    update_appointment_window.title("VCC Appointments - Update Appointment ")
    update_appointment_window.geometry("800x800")
    update_frame = LabelFrame(update_appointment_window, padx=10, pady=10)
    masterframe = update_frame
    update_frame.grid(row=2, columnspan=2, padx=10, pady=10)

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

        cursor.execute(
            "SELECT COUNT(*) from patients WHERE email_address='" + input + "' ")
        result = cursor.fetchone()
        if int(result[0]) == 0:
            messagebox.showwarning("Patient Not Found", "Patient Not Found. Please try again.")
            search_email.delete(0, END)
        else:
            cursor.execute(
                "SELECT COUNT(*) from appointments WHERE patient_id='" + str(getPatID()) + "' ")
            result = cursor.fetchone()

            if int(result[0]) == 0:
                messagebox.showwarning("Appointment Not Found", "No Appointment is Scheduled for this patient.")
                search_email.delete(0, END)

            sql = "SELECT * FROM appointments WHERE patient_id LIKE ?"
            res = cursor.execute(sql, (getPatID(),))
            i=0
            entries = []
            for row in res:
                i+=1
                appt_date1 = row[1]
                appt_time1 = row[2]
                appt_status1 = row[3]

                # Creating the Display Data -------------------------------------

                # Display Appointment Date
                label1 = Label(masterframe, text="Appointment Date:", font='Helvetica 14 bold')
                label1.grid(row=i-1, column=0, padx=10, pady=10, sticky='e')
                #
                appt_date = DateEntry(masterframe, width=12, background='white', foreground='darkblue',
                                      borderwidth=2, mindate=date.today())
                appt_date.delete(0,END)
                appt_date.insert(END, str(appt_date1))
                entries.append(appt_date.get())
                appt_date.grid(row=i-1, column=1, padx=10, pady=10)


                # Enter Appointment Time
                timeOptions = ["9:00 AM", "9:30 AM", "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM", "12:00 PM", "12:30 PM",
                               "1:00 PM", "1:30 PM", "2:00 PM", "2:30 PM", "3:00 PM", "3:30 PM", "4:00 PM", "4:30 PM"]
                label2 = Label(masterframe, text="Appointment Time:", font='Helvetica 14 bold')
                label2.grid(row=i-1, column=2, padx=10, pady=10, sticky='e')

                #
                def callbackFunc(event):
                    appt_time = event.widget.get()
                    print(appt_time)

                appt_time = ttk.Combobox(masterframe, value=timeOptions, width=25)
                appt_time.delete(0, END)
                appt_time.insert(END, str(appt_time1))
                appt_time.bind("<<ComboboxSelected>>", callbackFunc)
                entries.append(appt_time.get())
                appt_time.grid(row=i-1, column=3, padx=40, pady=20)

                # Update Appointment Status
                statusOptions = ["Upcoming", "Completed","Missed"]
                label3 = Label(masterframe,text="Appointment Status:", font='Helvetica 14 bold')
                label3.grid(row=i-1, column=4, padx=10, pady=10, sticky='e')

                #
                def callbackFunc(event):
                    appt_status = event.widget.get()
                    print(appt_status)

                appt_status = ttk.Combobox(masterframe, value=statusOptions)
                appt_status.delete(0, END)
                appt_status.insert(END, str(appt_status1))
                appt_status.bind("<<ComboboxSelected>>", callbackFunc)
                entries.append(appt_status.get())
                appt_status.grid(row=i-1, column=5, padx=10, pady=10, sticky='w')

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
                    if var1 == "" or var2 == "":
                        messagebox.showwarning("Fields Empty", "Warning: No Fields Should Be Empty.")
                    elif int(result[0]) > 0:
                        if appt_date1 == var1 and appt_time1 == var2:
                            messagebox.showinfo("Updated", "Successfully Updated.")
                            cursor.execute(query, (var1, var2, var3, getAptID(),))
                        else:
                            messagebox.showwarning("Error","Error: Appointment Slot Occupied")
                    else:
                        messagebox.showinfo("Updated", "Successfully Updated.")
                        cursor.execute(query, (var1, var2, var3, getAptID(),))
                    db.commit()

                # Update Button
                update = Button(masterframe, text="Update Appointment", width=18, height=2, command=update_db)
                update.grid(row=i-1, column=6, padx=10, pady=10)

    # Search Button
    search = Button(master, text="Search Appointment Database", width=18, height=2, command=search_db)
    search.grid(row=3, columnspan=2, padx=10, pady=10)

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

        cursor.execute(
            "SELECT COUNT(*) from patients WHERE email_address='" + input + "' ")
        result = cursor.fetchone()
        if int(result[0]) == 0:
            messagebox.showwarning("Patient Not Found", "Patient Not Found. Please try again.")
            search_email.delete(0, END)
        else:
            cursor.execute(
                "SELECT COUNT(*) from appointments WHERE patient_id='" + str(getPatID()) + "' ")
            result = cursor.fetchone()

            if int(result[0]) == 0:
                messagebox.showwarning("Appointment Not Found", "No Appointment is Scheduled for this patient.")
                search_email.delete(0, END)
                db.close()

            sql = "SELECT * FROM appointments WHERE patient_id LIKE ?"
            res = cursor.execute(sql, (getPatID(),))
            for row in res:
                appt_date1 = row[1]
                appt_time1 = row[2]
                appt_status1 = row[3]

        # Creating the Display Data -------------------------------------

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
                messagebox.showinfo("Success", "Deleted Successfully")
                db.commit()
                messagebox.showinfo("Success", "Deleted Successfully")
            else:
                db.close()

        # Delete Button
        delete = Button(master, text="Delete Appointment", width=18, height=2, command=delete_db)
        delete.grid(row=8, columnspan=2, padx=10, pady=10)

    # Search Button
    search = Button(master, text="Search Appointment Database", width=18, height=2, command=search_db)
    search.grid(row=2, columnspan=2, padx=10, pady=10)


def remind_patient():
    display_appointment_window = Tk()
    display_appointment_window.title("VCC Appointments - View Patient Appointments ")
    # display_appointment_window.geometry("800x800")
    display_frame = LabelFrame(display_appointment_window, padx=10, pady=10)
    masterframe = display_frame
    display_frame.grid(row=2, columnspan=2, padx=10, pady=10)

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
    search_email.grid(row=1, column=1, padx=10, pady=10, sticky='w')

    # Function To Perform Search
    def search_db():
        input = search_email.get()

        def getPatID():
            cursor.execute("SELECT patient_id from patients WHERE email_address='" + input + "'")
            patID = cursor.fetchone()[0]
            return patID

        cursor.execute(
            "SELECT COUNT(*) from patients WHERE email_address='" + input + "' ")
        result = cursor.fetchone()
        if int(result[0]) == 0:
            messagebox.showwarning("Patient Not Found", "Patient Not Found. Please try again.")
            search_email.delete(0, END)
        else:
            cursor.execute(
                "SELECT COUNT(*) from appointments WHERE patient_id='" + str(getPatID()) + "' ")
            result = cursor.fetchone()

            if int(result[0]) == 0:
                messagebox.showwarning("Appointment Not Found", "No Appointment is Scheduled for this patient.")
                search_email.delete(0, END)


            sql = "SELECT * FROM appointments WHERE patient_id LIKE ?"
            res = cursor.execute(sql, (getPatID(),))
            i=0
            for row in res:
                i+=1
                appt_date1 = row[1]
                appt_time1 = row[2]
                appt_status1 = row[3]


                label0 = Label(masterframe, text="Date:", font='Helvetica 14 bold',width=10)
                label0.grid(row=i-1, column=0, padx=10, pady=10, sticky='w')
                #
                appt_date = Label(masterframe, text=appt_date1, font='Helvetica 14',width=10)
                appt_date.grid(row=i-1, column=1, padx=10, pady=10, sticky='w')

                # Display Appointment Time
                label1 = Label(masterframe, text="Time:", font='Helvetica 14 bold',width=10)
                label1.grid(row=i-1, column=2, padx=10, pady=10, sticky='w')
                #
                appt_time = Label(masterframe, text=appt_time1, font='Helvetica 14',width=10)
                appt_time.grid(row=i-1, column=3, padx=10, pady=10, sticky='w')

                # Display Appointment Status
                label2 = Label(masterframe, text="Status:", font='Helvetica 14 bold',width=10)
                label2.grid(row=i-1, column=4, padx=10, pady=10, sticky='w')
                #
                appt_status = Label(masterframe, text=appt_status1, font='Helvetica 14')
                appt_status.grid(row=i-1, column=5, padx=10, pady=10, sticky='w')

            def patientreminder():
                cursor.execute("SELECT first_name from patients WHERE email_address='" + input + "'")
                patName = cursor.fetchone()[0]
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login("comp2140project2021@gmail.com", "softwareengineering")
                mess = input
                name = patName
                appoint = appt_date1
                time = appt_time1
                body = " " + "\r\n" + "Hello " + name + "! " + "Your upcoming appointment at Vision Care Centre on " + appoint + " at " + time + " is coming up. If there are any changes or concerns, please contact our office. Have a great day!"
                message = 'Subject: {}\n\n{}'.format("Upcoming Visioncare Appointment", body)
                server.sendmail(

                    "comp2140project2021@gmail.com",

                    mess,

                    message)
                print("Email sent to " + name)
                print(mess)
                print(message)
                print(appoint)
                print(time)
                print(message)
                server.quit()

            # Remind
            remind = Button(master, text="Send Reminder", width=18, height=2, command=patientreminder)
            remind.grid(row=4, columnspan=2, padx=10, pady=10)
    # Search Button
    search = Button(master, text="Search Appointments", width=18, height=2, command=search_db)
    search.grid(row=3, columnspan=2, padx=10, pady=10)

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
img = PhotoImage(file="images/VCC-Logo.png")
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

# Delete Patient Button
remind_patient_button = Button(text="Remind Patient of Appointment",command=remind_patient)
remind_patient_button.grid(row=9, columnspan=2, padx=10, pady=10, ipadx=30, ipady=20, sticky='w')

appointment_window.mainloop()