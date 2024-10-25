import os
import random
import support_classes
from datetime import date

need = support_classes.need()
qr = support_classes.QR()
today = date.today()

# try importing the required modules
try:
    from prettytable import PrettyTable
    
except Exception:
    
    print('''Required modules missing
Now manually installing modules from pip.....''')
    
    print('Installing prettytable')
    need.collect('prettytable')
    
    # importing module again after installing
    from prettytable import PrettyTable

try:
    import mysql.connector

except Exception as e:
    
    print("Installing mysql connector for python")

    need.collect('mysql-connector-python')
    # importing module again after installling
    import mysql.connector

# connect to the host
try:   
    mydb=mysql.connector.connect(host='localhost',
                            user='root',
                            password='bf387bnc25ncxn23d2',
                            database = 'mark_your_attendance')

except Exception as e: 
    
     # if failed to connect to the local host
    try:

        # if we are not running it for the first time
        with open('localhostdetails.txt','r') as f:
            readed = f.readline()
            details = readed.split(',')
            user, password= details[0], details[1]
            f.close()
        
        mydb=mysql.connector.connect(host='localhost',
                            user=user,
                            password=password,
                            database = 'mark_your_attendance')
    
    except FileNotFoundError as e:
            
        try:

            # if we are running it for the first time
            need.database()
            
        except Exception as e:
            print("\nDatabase could not be created.")
            print(e)

mycursor = mydb.cursor()

class Base():

    def add_to_table(self, values):
        
        try:
            id_ = self.new_id()
            query=f"insert into members values('{values[0]}', '{values[1]}', '{values[2]}', '{values[3]}', '{values[4]}', {values[5]}, {id_}, '{values[6]}', '{values[7]}');"
            mycursor.execute(query)
            mydb.commit()
            qr.maker(values[0]+","+values[1]+","+str(id_))
            print(f'Member added successfully. And the ID is {id_}')
            
            return True

        except Exception as e:
            print(f"Member could not be added because of the reason:{e}")
            return True

    def login(self):

            for i in range(5):
                password=input('Enter Password:')
                query=f'select password from login where organisation_name="{self.organisation_name}" and email="{self.email}";'
                mycursor.execute(query)
                pswd=mycursor.fetchone()
                
                if pswd[0] == password:
                    return True
                else:
                    print('Wrong password entered.Try again...')
            
            return None

    def mark(self):
            verify = self.login()
            if verify == True:
                
                flag = True
                while flag == True:
                    
                    value = qr.scanner()
                    if value == None:
                        
                        verify = self.login()
                        if verify == True:
                            
                            print("\nMarking for the absenties...")
                            # [(id,),(id,)]
                            query = f"select ID,Name,Designation from members;"
                            mycursor.execute(query)
                            details = mycursor.fetchall()

                            query = f"select ID from attendance where date='{today}' and mark='Yes';"
                            mycursor.execute(query)
                            records = mycursor.fetchall()
                            present_people = []
                            
                            for i in records:
                                present_people.append(i[0])
                            
                            for detail in details:
                                if detail[0] not in present_people:
                                    query = f"insert into attendance values('{detail[1]}','{detail[2]}','{today}','No',{detail[0]});"
                                    mycursor.execute(query)
                                    mydb.commit()

                            # update about the absenties
                            print("Updating Strikes for the absenties...")
                            query = f"select ID from attendance where date='{today}' and mark='No';"
                            mycursor.execute(query)
                            absenties = mycursor.fetchall()
                            for i in range(len(absenties)):
                                query = f'update members set Strikes = Strikes+1 where ID="{absenties[i][0]}";'
                                mycursor.execute(query)
                                mydb.commit()
                            print("\nAll the absenties have been marked and their strikes have also been updated.")
                            flag = False
                            return True
                        
                        else:
                            return None
                        
                    else:
                        values = value.split(',')
                        query = f"insert into attendance values('{values[0]}','{values[1]}','{today}','Yes',{int(values[2])});"
                        mycursor.execute(query)
                        mydb.commit()
                        print("\nAttendance marked for",values[0])
                        
            return None

    def new_id(self):

        numbers = [1,2,3,4,5,6,7,8,9]
        id_ = ''

        for i in range(5):
              if i==0:
                id_ = id_ + str(random.choice(numbers))
                numbers.append(0)
              else:
                    id_ = id_ + str(random.choice(numbers))
        return int(id_)

    def rem_from_table(self):

        try:

            # delete particiapnt from table.
            id_ = input("Enter ID of the Member you want to remove:")
            query1=f"delete from members where ID='{id_}';"
            mycursor.execute(query1)
            mydb.commit()

            # delete qr-code from the database
            os.chdir("C:\\Users\\hp\\OneDrive\\Desktop\\All Codes\\Attedance Project\\Created QR-Codes")
            os.remove(id_+'.png')

            return True
        
        except Exception as e:

            print(f"Error occured while trying to remove Member & Error is:{e}")
            return True

    def sign_up(self,org_name,email,password):

        query = f"select organisation_name,email,password from login;"
        mycursor.execute(query)
        records = mycursor.fetchall()

        for record in records:

            if org_name in record:
                print("Organisation already registered.")
                print("Please sign-in using your registered Email.")
                return True
            
            if email in record:
                print("Email already in use.")
                print("Please sign-in using your email and password.")
                return True
            
            if password in record:
                print("Password was rejected for being weak. Choose different password.")
                return True
            
        query = f"insert into login values('{org_name}','{password}','{email}');"
        mycursor.execute(query)
        mydb.commit()
        os.system('cls')
        print("You have been registered successfully. Please sign-in using your credentials.")
        flag =False
        return True
                
class admin(Base):

    def __init__(self,org_name,email):
            
            query = f"select organisation_name from login;"
            mycursor.execute(query)
            record = mycursor.fetchall()
            for i in record:
                if i[0] == org_name:
                    self.organisation_name = org_name
                    query = f"select email from login where organisation_name='{self.organisation_name}';"
                    mycursor.execute(query)
                    record = mycursor.fetchall()

                    for i in record:
                        if i[0] == email:
                            self.email = email
                            rv = self.login()

                            if rv == True:
                                os.system('cls')
                                print(f"Dashboard for organisation {self.organisation_name}.")
                                return self.ask()
                            else:
                                return None
                        
                        else:
                            print("Wrong email entered.Please Try Again...")
                            return None

            print("No Organisation with this name is registered with us.")
            return None

    def ask(self):

        print("\n----------------------------------------------------------------\n")
        print(f''' \tHello, Your options as Admin of {self.organisation_name} are:
        \tEnter 1 to add a new Member into the attendance list.
        \tEnter 2 to remove a Member from the attendance list.
        \tEnter 3 to display information of a particular Member.
        \tEnter 4 to display attendance for a particular date.
        \tEnter 5 to display attendance of a particular Member.
        \tEnter 6 to display attendance of a particular Member for a particular date.
        \tEnter 7 to mark attendance for {today}.
        \tEnter 8 to Log-out.''')
        ch= int(input(':'))

        if ch==1:
            name = input("Enter name:")
            designation = input("Enter Designation:")
            department = input("Enter Department:")
            course = input("Enter course:")
            year = input("Enter Year:")
            strikes = 0
            email = input("Enter Email:")
            org = self.organisation_name
            if self.add_to_table([name,designation,department,course,year,strikes,email,org]):
                return self.ask()
        
        elif ch==2:
            
            if self.rem_from_table():
                return self.ask()

        elif ch==3:
            
            try:
                id_ = input("Enter ID of Member:")
                query=f'select Name,Designation,Department,Course,Year,Strikes,ID,Email from members where ID="{id_}";'
                mycursor.execute(query)
                t=PrettyTable(['Name','Designation','Department @ ELab','Course','Year','Strikes','ID','Email'])
                data=mycursor.fetchall()
                for i in data:
                    row = [i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]]
                    t.add_row(row)
                print(t)
                return self.ask()
            
            except Exception as e:
                print(f"Could not process the command. The reason being:{e}")
                return None

        elif ch==4:
            
            try:
                dte=input('Enter date:')
                query=f'select * from attendance where date="{dte}";'
                mycursor.execute(query)
                t=PrettyTable(['Name','Designation','Date','Mark'])
                data=mycursor.fetchall()

                for i in data:
                    row = [i[0],i[1],i[2],i[3]]
                    t.add_row(row)
                print(t)
                return self.ask()
            
            except Exception as e:
                print(f"Could not process the command. The reason being:{e}")
                return None
            
        elif ch==5:

            try:
                id_ = input("Enter ID of Member:")
                query=f'select * from attendance where ID="{id_}";'
                mycursor.execute(query)
                t=PrettyTable(['Name','Designation','Date','Mark'])
                data=mycursor.fetchall()
                for i in data:
                    row = [i[0],i[1],i[2],i[3]]
                    t.add_row(row)
                print(t)
                return self.ask()
            
            except Exception as e:
                print(f"Could not process the command. The reason being:{e}")
                return None

        elif ch==6:

            try:
                dte= input('Enter date:')
                id_=input('Enter ID of Member:')
                query=f'select * from attendance where Date="{dte}" and ID="{id_}";'
                mycursor.execute(query)
                t=PrettyTable(['Name','Designation','Date','Mark'])
                data=mycursor.fetchall()
                for i in data:
                    row = [i[0],i[1],i[2],i[3]]
                    t.add_row(row)
                print(t)
                return self.ask()
            
            except Exception as e:
                print(f"Could not process the command. The reason being:{e}")
                return None
            
        elif ch==7:

            rv = self.mark()
            if rv == True:
                return self.ask()
            else:
                return None

        elif ch==8:
            
            for i in range(5):
                password=input('Enter Password:')
                query=f'select password from login where organisation_name="{self.organisation_name}" and email="{self.email}";'
                mycursor.execute(query)
                pswd=mycursor.fetchone()
                
                if pswd[0] == password:
                    os.system('cls')
                    print("Log-out successfull")
                    return None
                else:
                    print('Wrong password entered.Try again...')
            os.system('cls')
            print("Log-out failed because of wrong password.")
            return self.ask()
            
        else:
            print("Wrong choice entered. Please try again...")
            return self.ask()
