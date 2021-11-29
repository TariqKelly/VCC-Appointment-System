#import win10toast library to create desktop notifications
from win10toast import ToastNotifier

def notifyStaff(patientName, appointmentTime):
    #set icon path for notification icon
    ICON_PATH = "C:/Users/tariq/OneDrive/Documents/vcc_icon.ico"

    #instatiate notification object
    n = ToastNotifier()

    #generate and display notification with relevant patient's name and appointment time
    n.show_toast("PATIENT ALERT", f"{patientName} will be arriving at {appointmentTime}", duration=25, icon_path=ICON_PATH)
