import os
import main_classes as main

os.system('cls')

base = main.Base()
flag = True

while flag!=False:

    print("\n---------------- Welcome to 'MARK YOUR ATTENDANCE' ----------------\n")
    print("You want to sign-in or sign-up?")
    print("Enter 1 for sign-in and 2 for sign-up or 3 to end the programme...")
    choice = int(input(":"))

    if choice == 1:
        org_name = input("Enter Name of your Organisation:")
        email=input("Enter Email:")
        flag = main.admin(org_name,email)

    elif choice == 2:
        org_name = input("Enter Name of your Organisation:")
        email = input("Enter Email:")
        password = input("Enter Password:")
        flag = base.sign_up(org_name=org_name,email=email,password=password)
    
    elif choice == 3:
        os.system('cls')
        print('\n\n---------------- Thanks for using our product ----------------\n\n')
        flag=False
        
    else:
        print("Wrong choice is entered. Please try again...")