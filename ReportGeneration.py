from datetime import date
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from tkinter import colorchooser
from configparser import ConfigParser
from tkinter.ttk import Notebook
import re

from reportlab.platypus import SimpleDocTemplate,Paragraph,Table,TableStyle
from reportlab.lib import colors
from tkcalendar import DateEntry


# Allowed Characters for Name and Email Fields
regexEmail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
regexName = r'^[a-zA-Z- ]+( [a-zA-Z -]+)*$'


def generate_pdf():
    pdf = SimpleDocTemplate("samplereport.pdf")
    flow_obj = []
    td = [["Patient ID", "First Name", "Last Name", "Phone Number", "Email Address"]]

    # Create a database or connect to one that exists
    conn = sqlite3.connect('database.db')

    # Create a cursor instance
    c = conn.cursor()

    c.execute("SELECT * FROM patients")
    records = c.fetchall()
    for row in records:
        data = [row[0], row[1], row[2], row[3], row[4]]
        td.append(data)
    table = Table(td)
    ts = TableStyle([("GRID", (0, 0), (-1, -1), 2, colors.lightblue)])
    table.setStyle(ts)
    flow_obj.append(table)
    pdf.build(flow_obj)

def generate_ap_pdf():
    pdf = SimpleDocTemplate("sample_app_report.pdf")
    flow_obj = []
    td = [["Appt ID", "Date", "Time", "Status", "Patient ID", "First Name", "Last Name", "Email Address", "Phone Number"]]

    # Create a database or connect to one that exists
    conn = sqlite3.connect('database.db')

    # Create a cursor instance
    c = conn.cursor()

    c.execute("SELECT appointments.appt_id, appointments.appt_date, appointments.appt_time, appointments.appt_status, "
              "patients.patient_id, patients.first_name, patients.last_name, patients.email_address, patients.tel_num "
              "FROM appointments INNER JOIN patients ON appointments.patient_id=patients.patient_id")
    records = c.fetchall()
    fulldata = []
    for row in records:
        data = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]]
        td.append(data)
        fulldata.append(data)
        ts = TableStyle([("GRID", (0, 0), (-1, -1), 1, colors.black)])
        for i, row in enumerate(fulldata):
            if row[3] == "Missed":
                ts.add('TEXTCOLOR', (0,i+1), (-1,i+1), colors.red)
        print(row)
        print(row[3])
    print(list(enumerate(fulldata)))


    table = Table(td)

    table.setStyle(ts)
    flow_obj.append(table)
    pdf.build(flow_obj)

masterwindow = Tk()
masterwindow.title('Generate Reports')
#root.iconbitmap('')
masterwindow.geometry("1000x550")



# Read our config file and get colors
parser = ConfigParser()
parser.read("report.ini")
saved_primary_color = parser.get('colors', 'primary_color')
saved_secondary_color = parser.get('colors', 'secondary_color')
saved_highlight_color = parser.get('colors', 'highlight_color')


def query_database():
    # Clear the Treeview
    for record in my_tree.get_children():
        my_tree.delete(record)

    # Create a database or connect to one that exists
    conn = sqlite3.connect('database.db')

    # Create a cursor instance
    c = conn.cursor()

    c.execute("SELECT rowid, * FROM patients")
    records = c.fetchall()

    # Add our data to the screen
    global count
    count = 0

    # for record in records:
    #	print(record)

    for record in records:
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text='',
                           values=(record[1], record[2], record[3], record[4], record[5]),

                           tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='',
                           values=(record[1],record[2], record[3], record[4], record[5]),
                           tags=('oddrow',))
        # increment counter
        print(record)
        count += 1

    # Commit changes
    conn.commit()

    # Close our connection
    conn.close()
def query_ap_database():
    # Clear the Treeview
    for record in my_ap_tree.get_children():
        my_ap_tree.delete(record)

    # Create a database or connect to one that exists
    conn = sqlite3.connect('database.db')

    # Create a cursor instance
    c = conn.cursor()

    c.execute("SELECT appointments.appt_id, appointments.appt_date, appointments.appt_time, appointments.appt_status, "
              "patients.patient_id, patients.first_name, patients.last_name, patients.email_address, patients.tel_num "
              "FROM appointments INNER JOIN patients ON appointments.patient_id=patients.patient_id")
    records = c.fetchall()

    # Add our data to the screen
    global count
    count = 0

    # for record in records:
    #	print(record)

    for record in records:
        if count % 2 == 0:
            my_ap_tree.insert(parent='', index='end', iid=count, text='',
                           values=(record[0], record[1], record[2], record[3], record[4], record[5],record[6], record[7], record[8]),

                           tags=('evenrow',))
        else:
            my_ap_tree.insert(parent='', index='end', iid=count, text='',
                           values=(record[0], record[1], record[2], record[3], record[4], record[5],record[6], record[7], record[8]),
                           tags=('oddrow',))
        # increment counter
        print(record)
        count += 1

    # Commit changes
    conn.commit()

    # Close our connection
    conn.close()

def search_records():
    lookup_record = search_entry.get()
    # close the search box
    search.destroy()

    # Clear the Treeview
    for record in my_tree.get_children():
        my_tree.delete(record)

    # Create a database or connect to one that exists
    conn = sqlite3.connect('database.db')

    # Create a cursor instance
    c = conn.cursor()

    c.execute("SELECT rowid, * FROM patients WHERE last_name like ?", (lookup_record,))
    records = c.fetchall()

    # Add our data to the screen
    global count
    count = 0

    # for record in records:
    #	print(record)

    for record in records:
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text='',
                           values=(record[1], record[2], record[3], record[4]),
                           tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='',
                           values=(record[1], record[2], record[3], record[4]),
                           tags=('oddrow',))
        # increment counter
        count += 1

    # Commit changes
    conn.commit()

    # Close our connection
    conn.close()


def lookup_records():
    global search_entry, search

    search = Toplevel(masterwindow)
    search.title("Lookup Records")
    search.geometry("400x200")
    #search.iconbitmap('')

    # Create label frame
    search_frame = LabelFrame(search, text="Last Name")
    search_frame.pack(padx=10, pady=10)

    # Add entry box
    search_entry = Entry(search_frame, font=("Helvetica", 18))
    search_entry.pack(pady=20, padx=20)

    # Add button
    search_button = Button(search, text="Search Records", command=search_records)
    search_button.pack(padx=20, pady=20)


def primary_color():
    # Pick Color
    primary_color = colorchooser.askcolor()[1]

    # Update Treeview Color
    if primary_color:
        # Create Striped Row Tags
        my_tree.tag_configure('evenrow', background=primary_color)

        # Config file
        parser = ConfigParser()
        parser.read("report.ini")
        # Set the color change
        parser.set('colors', 'primary_color', primary_color)
        # Save the config file
        with open('report.ini', 'w') as configfile:
            parser.write(configfile)


def secondary_color():
    # Pick Color
    secondary_color = colorchooser.askcolor()[1]

    # Update Treeview Color
    if secondary_color:
        # Create Striped Row Tags
        my_tree.tag_configure('oddrow', background=secondary_color)

        # Config file
        parser = ConfigParser()
        parser.read("report.ini")
        # Set the color change
        parser.set('colors', 'secondary_color', secondary_color)
        # Save the config file
        with open('report.ini', 'w') as configfile:
            parser.write(configfile)


def highlight_color():
    # Pick Color
    highlight_color = colorchooser.askcolor()[1]

    # Update Treeview Color
    # Change Selected Color
    if highlight_color:
        style.map('Treeview',
                  background=[('selected', highlight_color)])

        # Config file
        parser = ConfigParser()
        parser.read("report.ini")
        # Set the color change
        parser.set('colors', 'highlight_color', highlight_color)
        # Save the config file
        with open('report.ini', 'w') as configfile:
            parser.write(configfile)


def reset_colors():
    # Save original colors to config file
    parser = ConfigParser()
    parser.read('report.ini')
    parser.set('colors', 'primary_color', 'lightblue')
    parser.set('colors', 'secondary_color', 'white')
    parser.set('colors', 'highlight_color', '#347083')
    with open('report.ini', 'w') as configfile:
        parser.write(configfile)
    # Reset the colors
    my_tree.tag_configure('oddrow', background='white')
    my_tree.tag_configure('evenrow', background='lightblue')
    style.map('Treeview',
              background=[('selected', '#347083')])


# Add Menu
my_menu = Menu(masterwindow)
masterwindow.config(menu=my_menu)

# Configure our menu
option_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Options", menu=option_menu)
# Drop down menu
option_menu.add_command(label="Primary Color", command=primary_color)
option_menu.add_command(label="Secondary Color", command=secondary_color)
option_menu.add_command(label="Highlight Color", command=highlight_color)
option_menu.add_separator()
option_menu.add_command(label="Reset Colors", command=reset_colors)
option_menu.add_separator()
option_menu.add_command(label="Exit", command=masterwindow.quit)

# Search Menu
search_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Search", menu=search_menu)
# Drop down menu
search_menu.add_command(label="Search", command=lookup_records)
search_menu.add_separator()
search_menu.add_command(label="Reset", command=query_database)

# Create a database or connect to one that exists
conn = sqlite3.connect('database.db')

# Create a cursor instance
c = conn.cursor()

# Add Some Style
style = ttk.Style()

# Pick A Theme
style.theme_use('default')

# Configure the Treeview Colors
style.configure("Treeview",
                background="#D3D3D3",
                foreground="black",
                rowheight=25,
                fieldbackground="#D3D3D3")

# Change Selected Color #347083
style.map('Treeview',
          background=[('selected', saved_highlight_color)])

Tabs = Notebook(masterwindow)
Tabs.pack()
patient_frame = Frame(Tabs,padx=20,pady=20)
appointment_frame = Frame(Tabs,padx=20,pady=20)
patient_tree_frame = Frame(patient_frame)
appointment_tree_frame = Frame(appointment_frame)
patient_tree_frame.pack()
appointment_tree_frame.pack()
Tabs.add(patient_frame, text ='Patients')
Tabs.add(appointment_frame, text ='Appointments')
#-----------------------------------------------------------------------------------------------------------------------------
# Create a Treeview Scrollbar
tree_scroll = Scrollbar(patient_tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# Create The Treeview
my_tree = ttk.Treeview(patient_tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
my_tree.pack()

# Configure the Scrollbar
tree_scroll.config(command=my_tree.yview)

# Define Our Columns
my_tree['columns'] = ("Patient ID","First Name", "Last Name", "Telephone Number", "Email Address")

# Format Our Columns
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Patient ID", anchor=W, width=60)
my_tree.column("First Name", anchor=W, width=140)
my_tree.column("Last Name", anchor=W, width=100)
my_tree.column("Telephone Number", anchor=W, width=140)
my_tree.column("Email Address", anchor=W, width=200)

# Create Headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("Patient ID", text="Patient ID", anchor=W)
my_tree.heading("First Name", text="First Name", anchor=W)
my_tree.heading("Last Name", text="Last Name", anchor=W)
my_tree.heading("Telephone Number", text="Telephone Number", anchor=W)
my_tree.heading("Email Address", text="Email Address", anchor=W)

# Create Striped Row Tags
my_tree.tag_configure('oddrow', background=saved_secondary_color)
my_tree.tag_configure('evenrow', background=saved_primary_color)

# Add Record Entry Boxes
data_frame = LabelFrame(patient_frame, text="Record")
data_frame.pack(fill="x", expand="yes", padx=20)

fn_label = Label(data_frame, text="First Name:")
fn_label.grid(row=0, column=0, padx=10, pady=10)
fn_entry = Entry(data_frame)
fn_entry.grid(row=0, column=1, padx=10, pady=10)

ln_label = Label(data_frame, text="Last Name:")
ln_label.grid(row=0, column=2, padx=10, pady=10)
ln_entry = Entry(data_frame)
ln_entry.grid(row=0, column=3, padx=10, pady=10)

phone_label = Label(data_frame, text="Phone Number:")
phone_label.grid(row=1, column=0, padx=10, pady=10)
phone_entry = Entry(data_frame)
phone_entry.grid(row=1, column=1, padx=10, pady=10)

email_label = Label(data_frame, text="Email Address:")
email_label.grid(row=1, column=2, padx=10, pady=10)
email_entry = Entry(data_frame)
email_entry.grid(row=1, column=3, padx=10, pady=10)


# Remove one record
def remove_one():
    x = my_tree.selection()[0]
    my_tree.delete(x)

    # Create a database or connect to one that exists
    conn = sqlite3.connect('database.db')

    # Create a cursor instance
    c = conn.cursor()

    # Delete From Database
    if messagebox.askokcancel("Confirm","Are You Sure You Want To Delete This Record?"):
        c.execute("DELETE from patients WHERE email_address='" + email_entry.get() + "'")

        # Commit changes
        conn.commit()

    # Close our connection
    conn.close()

    # Clear The Entry Boxes
    clear_entries()

    # Add a little message box for fun
    messagebox.showinfo("Deleted!", "Your Record Has Been Deleted!")


# Remove Many records
def remove_many():
    # Add a little message box for fun
    response = messagebox.askyesno("Warning", "This Will Delete EVERYTHING SELECTED From The Table\nAre You Sure?!")

    # Add logic for message box
    if response == 1:
        # Designate selections
        x = my_tree.selection()

        # Create List of ID's
        ids_to_delete = []

        # Add selections to ids_to_delete list
        for record in x:
            ids_to_delete.append(my_tree.item(record, 'values')[0])

        # Delete From Treeview
        for record in x:
            my_tree.delete(record)

        # Create a database or connect to one that exists
        conn = sqlite3.connect('database.db')

        # Create a cursor instance
        c = conn.cursor()

        # Delete Everything From The Table
        c.executemany("DELETE FROM patients WHERE patient_id = ?", [(a,) for a in ids_to_delete])

        # Reset List
        ids_to_delete = []

        # Commit changes
        conn.commit()

        # Close our connection
        conn.close()

        # Clear entry boxes if filled
        clear_entries()


# Clear entry boxes
def clear_entries():
    # Clear entry boxes
    fn_entry.delete(0, END)
    ln_entry.delete(0, END)
    phone_entry.delete(0, END)
    email_entry.delete(0, END)


# Select Record
def select_record(e):
    # Clear entry boxes
    fn_entry.delete(0, END)
    ln_entry.delete(0, END)
    phone_entry.delete(0, END)
    email_entry.delete(0, END)

    # Grab record Number
    selected = my_tree.focus()
    # Grab record values
    values = my_tree.item(selected, 'values')

    # outputs to entry boxes

    fn_entry.insert(0, values[1])
    ln_entry.insert(0, values[2])
    phone_entry.insert(0, values[3])
    email_entry.insert(0, values[4])
    print(values)


# Update record
def update_record():
    # Create a database or connect to one that exists
    conn = sqlite3.connect('database.db')

    # Create a cursor instance
    c = conn.cursor()
    def getPatID():
        c.execute("SELECT patient_id from patients WHERE email_address='" + email_entry.get() + "'")
        patID = c.fetchone()[0]
        return patID

    # Grab the record number
    selected = my_tree.focus()
    # Update record

    my_tree.item(selected, text="", values=(getPatID(), fn_entry.get(), ln_entry.get(), phone_entry.get(), email_entry.get(),))

    # Update the database

    query = "UPDATE patients SET first_name=?, last_name=?, tel_num=?, email_address=? WHERE email_address=?"
    c.execute(query, (fn_entry.get(), ln_entry.get(), phone_entry.get(), email_entry.get(), email_entry.get(),))



    # Commit changes
    conn.commit()
    messagebox.showinfo("Success","Patient Updated!")

    # Close our connection
    conn.close()

    # Clear entry boxes
    fn_entry.delete(0, END)
    ln_entry.delete(0, END)
    phone_entry.delete(0, END)
    email_entry.delete(0, END)


# add new record to database
def add_record():
    # Create a database or connect to one that exists
    conn = sqlite3.connect('database.db')

    # Create a cursor instance
    c = conn.cursor()
    c.execute(
        "SELECT COUNT(*) from patients WHERE email_address='" + email_entry.get() + "' OR tel_num='" + phone_entry.get() + "' ")
    result = c.fetchone()
    if fn_entry.get() == "" or ln_entry.get() == "" or phone_entry.get() == "" or email_entry.get() == "":
        messagebox.showwarning("Fields Empty", "Warning: No Fields Should Be Empty.")
    elif not (re.fullmatch(regexEmail, email_entry.get())):
        messagebox.showwarning("Invalid Email", "Invalid Email Address")
    elif not (re.fullmatch(regexName, fn_entry.get())) or not (re.fullmatch(regexName, ln_entry.get())):
        messagebox.showwarning("Invalid Name", "Name cannot include special characters or numbers.")
    elif int(result[0]) > 0:
        messagebox.showwarning("Invalid", "This Patient Has Already Been Added")
    else:
        messagebox.showinfo("Success", "Patient Successfully Added!")
        c.execute("INSERT INTO patients(first_name,last_name,tel_num,email_address)VALUES(?,?,?,?)",
                  (fn_entry.get(), ln_entry.get(), phone_entry.get(), email_entry.get()))

        # Commit changes
        conn.commit()

    # Close our connection
    conn.close()

    # Clear entry boxes
    fn_entry.delete(0, END)
    ln_entry.delete(0, END)
    phone_entry.delete(0, END)
    email_entry.delete(0, END)

    # Clear The Treeview Table
    my_tree.delete(*my_tree.get_children())

    # Run to pull data from database on start
    query_database()


def create_table_again():
    # Create a database or connect to one that exists
    conn = sqlite3.connect('database.db')

    # Create a cursor instance
    c = conn.cursor()

    # Create Table
    c.execute("""CREATE TABLE IF NOT EXISTS patients(patient_id integer PRIMARY KEY AUTOINCREMENT, first_name text 
NOT NULL, last_name text NOT NULL, tel_num text NOT NULL, email_address text NOT NULL);""")

    # Commit changes
    conn.commit()

    # Close our connection
    conn.close()


# Add Buttons
button_frame = LabelFrame(patient_frame, text="Commands")
button_frame.pack(fill="x", expand="yes", padx=20)

update_button = Button(button_frame, text="Update Record", command=update_record)
update_button.grid(row=0, column=1, padx=10, pady=10)

add_button = Button(button_frame, text="Add Record", command=add_record)
add_button.grid(row=0, column=0, padx=10, pady=10)

remove_one_button = Button(button_frame, text="Remove One Selected", command=remove_one)
remove_one_button.grid(row=0, column=3, padx=10, pady=10)

remove_many_button = Button(button_frame, text="Remove Many Selected", command=remove_many)
remove_many_button.grid(row=0, column=4, padx=10, pady=10)

select_record_button = Button(button_frame, text="Generate PDF", command=generate_pdf)
select_record_button.grid(row=0, column=7, padx=10, pady=10)

# Bind the treeview
my_tree.bind("<ButtonRelease-1>", select_record)

# Run to pull data from database on start
query_database()
#----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------
# Create a Treeview Scrollbar
ap_tree_scroll = Scrollbar(appointment_tree_frame)
ap_tree_scroll.pack(side=RIGHT, fill=Y)

# Create The Treeview
my_ap_tree = ttk.Treeview(appointment_tree_frame, yscrollcommand=ap_tree_scroll.set, selectmode="extended")
my_ap_tree.pack()

# Configure the Scrollbar
ap_tree_scroll.config(command=my_ap_tree.yview)

# Define Our Columns
my_ap_tree['columns'] = ("Appt ID","Date", "Time", "Status", "Patient ID", "First Name", "Last Name","Email", "Phone")

# Format Our Columns
my_ap_tree.column("#0", width=0, stretch=NO)
my_ap_tree.column("Appt ID", anchor=W, width=60)
my_ap_tree.column("Date", anchor=W, width=90)
my_ap_tree.column("Time", anchor=W, width=90)
my_ap_tree.column("Status", anchor=W, width=90)
my_ap_tree.column("Patient ID", anchor=W, width=60)
my_ap_tree.column("First Name", anchor=W, width=100)
my_ap_tree.column("Last Name", anchor=W, width=100)
my_ap_tree.column("Email", anchor=W, width=200)
my_ap_tree.column("Phone", anchor=W, width=200)

# Create Headings
my_ap_tree.heading("#0", text="", anchor=W)
my_ap_tree.heading("Appt ID", text="Appt ID", anchor=W)
my_ap_tree.heading("Date", text="Date", anchor=W)
my_ap_tree.heading("Time", text="Time", anchor=W)
my_ap_tree.heading("Status", text="Status", anchor=W)
my_ap_tree.heading("Patient ID", text="Patient ID", anchor=W)
my_ap_tree.heading("First Name", text="First Name", anchor=W)
my_ap_tree.heading("Last Name", text="Last Name", anchor=W)
my_ap_tree.heading("Email", text="Email", anchor=W)
my_ap_tree.heading("Phone", text="Phone", anchor=W)


# Create Striped Row Tags
my_ap_tree.tag_configure('oddrow', background=saved_secondary_color)
my_ap_tree.tag_configure('evenrow', background=saved_primary_color)

# Add Record Entry Boxes
data_ap_frame = LabelFrame(appointment_frame, text="Record")
data_ap_frame.pack(fill="x", expand="yes", padx=20)

date_label = Label(data_ap_frame, text="Date:")
date_label.grid(row=0, column=0, padx=10, pady=10)
date_entry = DateEntry(data_ap_frame, width=12, background='white', foreground='darkblue',
                                      borderwidth=2, mindate=date.today())
date_entry.grid(row=0, column=1, padx=10, pady=10)

# Time Entry-----------------------------------------------------------------------
timeOptions = ["9:00 AM", "9:30 AM", "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM", "12:00 PM", "12:30 PM",
                               "1:00 PM", "1:30 PM", "2:00 PM", "2:30 PM", "3:00 PM", "3:30 PM", "4:00 PM", "4:30 PM"]

time_label = Label(data_ap_frame, text="Time:")
time_label.grid(row=0, column=2, padx=10, pady=10)

def callbackFunc(event):
    time_entry = event.widget.get()
    print(time_entry)

time_entry = ttk.Combobox(data_ap_frame, value=timeOptions, width=25)
time_entry.bind("<<ComboboxSelected>>", callbackFunc)
time_entry.grid(row=0, column=3, padx=10, pady=10)
#----------------------------------------------------------------------------------
#Status Entry
statusOptions = ["Upcoming", "Completed","Missed"]

status_label = Label(data_ap_frame, text="Status:")
status_label.grid(row=0, column=4, padx=10, pady=10)


def callbackFunc(event):
    status_entry = event.widget.get()
    print(status_entry)

status_entry = ttk.Combobox(data_ap_frame, value=statusOptions)
status_entry.bind("<<ComboboxSelected>>", callbackFunc)
status_entry.grid(row=0, column=5, padx=10, pady=10)



# Remove one record
def remove_one():
    x = my_ap_tree.selection()[0]
    my_ap_tree.delete(x)

    # Create a database or connect to one that exists
    conn = sqlite3.connect('database.db')

    # Create a cursor instance
    c = conn.cursor()

    # Delete From Database
    if messagebox.askokcancel("Confirm","Are You Sure You Want To Delete This Record?"):
        c.execute("DELETE from appointments WHERE appt_date='" + date_entry.get() + "' AND appt_time='" + time_entry.get() + "'")

        # Commit changes
        conn.commit()

    # Close our connection
    conn.close()

    # Clear The Entry Boxes
    clear_entries()

    # Add a little message box for fun
    messagebox.showinfo("Deleted!", "Your Record Has Been Deleted!")

# Clear entry boxes
def clear_entries():
    # Clear entry boxes
    date_entry.delete(0, END)
    time_entry.delete(0, END)
    status_entry.delete(0, END)

'''
# Update record
def update_record():
    # Create a database or connect to one that exists
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    sql = "SELECT * FROM appointments"
    res = c.execute(sql)
    for row in res:
        appt_id1 = row[0]
        appt_date1 = row[1]
        appt_time1 = row[2]
    # Create a cursor instance

    def getapptID():
        c.execute("SELECT appt_id from appointments WHERE appt_date='" + appt_date1 + "' AND appt_time='" + appt_time1 + "'")
        apptID = c.fetchone()[0]
        print(apptID)
        return apptID

    # Grab the record number
    selected = my_ap_tree.focus()
    # Update record

    my_ap_tree.item(selected, text="", values=(getapptID(), date_entry.get(), time_entry.get(), status_entry.get(),patient_id))

    # Update the database

    query = "UPDATE appointments SET appt_date=?, appt_time=?, appt_status=? WHERE appt_id=?"
    c.execute(query, (date_entry.get(), time_entry.get(), status_entry.get(),getapptID()))



    # Commit changes
    conn.commit()
    messagebox.showinfo("Success","Appointment Updated!")

    # Close our connection
    conn.close()

    # Clear entry boxes
    date_entry.delete(0, END)
    time_entry.delete(0, END)
    status_entry.delete(0, END)



# Remove Many records
def remove_many():
    # Add a little message box for fun
    response = messagebox.askyesno("Warning", "This Will Delete EVERYTHING SELECTED From The Table\nAre You Sure?!")

    # Add logic for message box
    if response == 1:
        # Designate selections
        x = my_ap_tree.selection()

        # Create List of ID's
        ids_to_delete = []

        # Add selections to ids_to_delete list
        for record in x:
            ids_to_delete.append(my_ap_tree.item(record, 'values')[0])

        # Delete From Treeview
        for record in x:
            my_ap_tree.delete(record)

        # Create a database or connect to one that exists
        conn = sqlite3.connect('database.db')

        # Create a cursor instance
        c = conn.cursor()

        # Delete Everything From The Table
        c.executemany("DELETE FROM patients WHERE patient_id = ?", [(a,) for a in ids_to_delete])

        # Reset List
        ids_to_delete = []

        # Commit changes
        conn.commit()

        # Close our connection
        conn.close()

        # Clear entry boxes if filled
        clear_entries()


# add new record to database
def add_record():
    # Create a database or connect to one that exists
    conn = sqlite3.connect('database.db')

    # Create a cursor instance
    c = conn.cursor()
    c.execute(
        "SELECT COUNT(*) from patients WHERE email_address='" + email_entry.get() + "' OR tel_num='" + phone_entry.get() + "' ")
    result = c.fetchone()
    if fn_entry.get() == "" or ln_entry.get() == "" or phone_entry.get() == "" or email_entry.get() == "":
        messagebox.showwarning("Fields Empty", "Warning: No Fields Should Be Empty.")
    elif not (re.fullmatch(regexEmail, email_entry.get())):
        messagebox.showwarning("Invalid Email", "Invalid Email Address")
    elif not (re.fullmatch(regexName, fn_entry.get())) or not (re.fullmatch(regexName, ln_entry.get())):
        messagebox.showwarning("Invalid Name", "Name cannot include special characters or numbers.")
    elif int(result[0]) > 0:
        messagebox.showwarning("Invalid", "This Patient Has Already Been Added")
    else:
        messagebox.showinfo("Success", "Patient Successfully Added!")
        c.execute("INSERT INTO patients(first_name,last_name,tel_num,email_address)VALUES(?,?,?,?)",
                  (fn_entry.get(), ln_entry.get(), phone_entry.get(), email_entry.get()))

        # Commit changes
        conn.commit()

    # Close our connection
    conn.close()

    # Clear entry boxes
    fn_entry.delete(0, END)
    ln_entry.delete(0, END)
    phone_entry.delete(0, END)
    email_entry.delete(0, END)

    # Clear The Treeview Table
    my_ap_tree.delete(*my_ap_tree.get_children())

    # Run to pull data from database on start
    query_ap_database()


def create_table_again():
    # Create a database or connect to one that exists
    conn = sqlite3.connect('database.db')

    # Create a cursor instance
    c = conn.cursor()

    # Create Table
    c.execute("""CREATE TABLE IF NOT EXISTS patients(patient_id integer PRIMARY KEY AUTOINCREMENT, first_name text 
NOT NULL, last_name text NOT NULL, tel_num text NOT NULL, email_address text NOT NULL);""")

    # Commit changes
    conn.commit()

    # Close our connection
    conn.close()

'''
# Select Record
def select_ap_record(e):
    # Clear entry boxes
    date_entry.delete(0, END)
    time_entry.delete(0, END)
    status_entry.delete(0, END)

    # Grab record Number
    selected = my_ap_tree.focus()
    # Grab record values
    values = my_ap_tree.item(selected, 'values')

    # outputs to entry boxes

    date_entry.insert(0, values[1])
    time_entry.insert(0, values[2])
    status_entry.insert(0, values[3])

    print(values)


# Add Buttons
button_frame = LabelFrame(appointment_frame, text="Commands")
button_frame.pack(fill="x", expand="yes", padx=20)

#update_button = Button(button_frame, text="Update Record", command=update_record)
#update_button.grid(row=0, column=1, padx=10, pady=10)

#add_button = Button(button_frame, text="Add Record", command="add_record")
#add_button.grid(row=0, column=0, padx=10, pady=10)

remove_one_button = Button(button_frame, text="Remove One Selected", command=remove_one)
remove_one_button.grid(row=0, column=3, padx=10, pady=10)

#remove_many_button = Button(button_frame, text="Remove Many Selected", command="remove_many")
#remove_many_button.grid(row=0, column=4, padx=10, pady=10)

select_record_button = Button(button_frame, text="Generate PDF", command=generate_ap_pdf)
select_record_button.grid(row=0, column=7, padx=10, pady=10)


# Bind the treeview
my_ap_tree.bind("<ButtonRelease-1>", select_ap_record)

# Run to pull data from database on start
query_ap_database()
#----------------------------------------------------------------------------------------------------------
masterwindow.mainloop()