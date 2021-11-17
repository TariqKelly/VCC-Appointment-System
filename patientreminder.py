import smtplib
from datetime import datetime

def patientreminder():

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login("comp2140project2021@gmail.com", "softwareengineering")
mess = input("Enter patient's email address: ")
name = input("Enter patient's name: ")
appoint= input("Enter the patient's appointment date: ")
time= input("Enter the time of the patient's appointment: ")
server.sendmail(
  
  "comp2140project2021@gmail.com", 
  
  mess, 
  
  "Hello " + name + "! " "Your upcoming appointment at Vision Care Centre on " + appoint + " at " + time + " is coming up. If there are any changes or concerns, please contact our office. Have a great day!")
print("Email sent to " + name)
server.quit()
