import os
import pip
import cv2
import qrcode
from PIL import Image
import mysql.connector
from datetime import date

today = date.today()

class QR():
    
    # make qr code for the newly added participant
    def maker(self,convert):
        
        qr = qrcode.QRCode(version = 1,
                    error_correction = qrcode.constants.ERROR_CORRECT_H,
                    box_size = 25, border = 4)
        
        qr.add_data(convert)
        qr.make(fit = True)

        image = qr.make_image(fill_color = "black", back_color = 'white')
        for_name = convert.split(',')
        name = for_name[2]
        image.save("Created QR-Codes\\" + name + ".png")

    # scanner to scan qr code for admin work
    def scanner(self,):
        print("Please wait while we open scanner to scan code.")

        cap = cv2.VideoCapture(0)
        detector = cv2.QRCodeDetector()
        a = None

        while True:
            
            _, img = cap.read()
            data, one, _ = detector.detectAndDecode(img)

            if data:
                a = data
                break

            cv2.imshow("Show your QR-Code to mark attendance.", img)

            if cv2.waitKey(1) == ord('q'):
                break


        try:
            cap.release(a)
        except Exception:
            cv2.destroyAllWindows()
        
        return a

class need():

    # download modules absent in the device.
    def collect(self,name):

        if hasattr(pip, 'main'):
            pip.main(['install', name])
            print(f"\nInstallation complete for {name}.")
        else:
            pip._internal.main(['install', name])
            print(f"\nInstallation complete for {name}.")
        os.system('cls')
        return

    # create database if file is running for the first time.
    def database(self):
        
        os.system('cls')
        
        try:
            print('''We could not connect to the localhost.
This is because you are running this file for the first time on this device.
Please provide localhost user and password for that user.
we will re-create sample database for you on your localhost.\n''')
        
            user = input("Please enter user for localhost:")
            password = input("Please enter password for the user:")
            
            line = user+','+password
            with open("localhostdetails.txt",'w') as f:
                f.write(str(line))
                f.close()
            
            mydb=mysql.connector.connect(host='localhost',
                                    user= user,
                                    password= password)
            print("Creating sample database now, please wait....\n\n")
            
            queries=[
                "create database mark_your_attendance;",

                '''use mark_your_attendance;''',
                
                '''create table members(
Name varchar(30),
Designation varchar(15) unique,
Department_ELab varchar(10),
course varchar(10),
Year varchar(5),
Strikes int,
ID int unique not null,
Email varchar(100) unique not null,
Organisation varchar(100) not null);''',

                '''create table login(
organisation_name varchar(60) unique not null,
password varchar(50) unique not null,
email varchar(100) unique not null);''',

                '''create table attendance(
Name varchar(30),
Designation varchar(15) unique,
Date date,
Mark varchar(3),
ID int unique not null);''',

'''insert into login values('ELab','demopassword','elab.demo@markyourattendance.com');''',

'''insert into members values('Shivansh',' ','Tech','PMCs','1st',0,82181,'shivansh.samplemail@markyourattendance.com','ELab');''',
'''insert into members values('Ashwarit','Tech-Manager','Tech','PME','2nd',0,73036,'ashwarit.samplemail@markyourattendance.com','ELab');''',

f'''insert into attendance values('Shivansh',' ','{today}','Yes',82181);''',
f'''insert into attendance values('Ashwarit','Tech-Manager','{today}','No',73036);'''
                ]

            mycursor=mydb.cursor()
            for query in queries:
                mycursor.execute(query)
                mydb.commit()

            QR().maker("'Shivansh',' ',82181")
            QR().maker("'Ashwarit','Tech-Manager',73036")

            os.system('cls')
            
            print("""Sample database has been created successfully.\n\n
There are two members in the sample database and their IDs are as follows:\n
ID number for Ashwarit is 73036.
ID number for Shivansh is 82181.\n\n
We are now closing program. Please start it again.
\n\nAnd before starting the program please make sure that the below path is added into your path folder
of environment variables before restarting the application else we won't be able read the created the database.
\n-----> C:\\\Program Files\\\MySQL\\\MySQL Server 8.1\\\\bin <-----\n\n""")
            exit()
        
        except Exception as e:
            os.remove("C:\\Users\\hp\\OneDrive\\Desktop\\All Codes\\Attedance Project\\localhostdetails.txt")
            return e
