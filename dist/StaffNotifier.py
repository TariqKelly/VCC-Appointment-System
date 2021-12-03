#import win10toast library to create desktop notifications
from win10toast import ToastNotifier
import datetime
import sqlite3


def notifyStaff():
    
    currentDateTime = datetime.datetime.now()
    currentDate = currentDateTime.strftime("%x")
    currentDate = currentDate.replace("0","")
    #print(currentDate)
    currentTime = currentDateTime.strftime("%I:%M %p")
    print(currentTime)
    
    conn = sqlite3.connect('database.db')

    # Create a cursor instance
    c = conn.cursor()

    c.execute("SELECT appointments.appt_date, appointments.appt_time, patients.first_name, patients.last_name"
              + " FROM appointments INNER JOIN patients ON appointments.patient_id=patients.patient_id")
    records = c.fetchall()
    
    for row in records:
        data = [row[0], row[1], row[2], row[3]]
        appointmentDate = row[0]
        #print(appointmentDate)
        appointmentTime = row[1]
        print(appointmentTime)
        patientName = f"{row[2]} {row[3]}"

    #instatiate notification object
        n = ToastNotifier()
    #m/d/yyyy H:MM 

    #generate and display notification with relevant patient's name and appointment time
        if (appointmentDate == currentDate and appointmentTime == currentTime):
            n.show_toast("PATIENT ALERT", f"{patientName} will be arriving at {appointmentTime}", duration=10)
    
