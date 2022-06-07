# Modules

import sqlite3
import getpass
import sys
import os
import time
import random
import string
import win32com.client as win32

# Variables

user = os.getlogin()
clear = lambda: os.system("cls")

# Database

db = fr"C:\Users\{user}\Dropbox\Dev\Python\Projects\User Management Console\db\users.db.db"
connection = sqlite3.connect(db)
cursor = connection.cursor()
table = "credentials"
print("Successfully Connected to SQLite3!")

def login():
    username = input("\nEnter Username: ")
    passwd = getpass.getpass("Enter Password: ")

    cursor.execute(f"SELECT loginid, password FROM {table} WHERE loginid=(?) and password=(?);", (username, passwd,))

    result = cursor.fetchone()
    if result != (username, passwd):
        clear()
        print("Login failed. Please try again.")
        login()
    else:
        clear()
        print(f"Success! Logged in as: {username}")
        time.sleep(1)
        clear()

login()

def view_users():
    print("--- View UID ---")
    print("\nThese users are currently active: \n")

    viewusers = cursor.execute("SELECT * FROM CREDENTIALS order by accountcreation DESC;")

    for i in viewusers:
        print(i[2], "- " + i[0], i[1])

def add_user():
    print("--- Add Users ---")

    value1 = input("\nEnter First Name: ").title()
    value2 = input("Enter Last Name: ").title()
    value3 = (value2[0:5].lower() + value1[0:3].lower())
    value4 = "".join(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=20))

    try:
        cursor.execute(f"INSERT INTO {table} VALUES (?,?,?,?,CURRENT_TIMESTAMP, NULL)", (value1, value2, value3, value4))
        connection.commit()
        clear()
        print("Account has been created. The password for this UID will only be shown once:\n")
        print(f"Name: {value1} {value2}")
        print(f"UID: {value3}")
        print(f"Password: {value4}")

        # Send Mail 1

        outlook = win32.Dispatch("outlook.application")
        mail = outlook.CreateItem(0)
        mail.To = "kelvingooding@msn.com"
        mail.Subject = f"{value1} {value2} - UMC Username"
        mail.Body = "Hi,\n\n" \
                    f"Your username is: {value3}\n\n" \
                    f"Password will be send in a seperate email."
        mail.Send()

        # Send Mail 2

        outlook = win32.Dispatch("outlook.application")
        mail = outlook.CreateItem(0)
        mail.To = "kelvingooding@msn.com"
        mail.Subject = f"{value1} {value2} - UMC Password"
        mail.Body = "Hi,\n\n" \
                    f"Your password is: {value4}\n\n"
        mail.Send()

    except sqlite3.IntegrityError:
        clear()
        print(f"The UID {value4} already exists. Please try again.")
        add_user()

def delete_user():
    print("--- Delete User ---")

    main1 = input("\nEnter a UID: ")

    result = cursor.execute(f"SELECT loginid FROM {table} WHERE loginid=(?);", (main1,))

    for i in result:
        if i[0] == main1:
            cursor.execute(f"DELETE FROM {table} WHERE loginid=(?)", (main1,))
            connection.commit()
            print("\nThe below user has been deleted:\n\n" + main1)
            submenu()
    else:
        clear()
        print("This user does not exists. Please try again.")
        time.sleep(3)
        clear()
        delete_user()

def password_reset():
    print("--- Password Reset ---")

    main2 = input("\nEnter UID: ")
    passwd1 = getpass.getpass("\nEnter New Password: ")
    passwd2 = getpass.getpass("Re-enter Password: ")

    if passwd1 == passwd2:
        cursor.execute(f"UPDATE {table} SET password=(?), lastpasschange=(CURRENT_TIMESTAMP) WHERE loginid=(?)", (passwd1, main2,))
        connection.commit()
        print("\nPassword has been changed!")

        # Send Mail 1

        outlook = win32.Dispatch("outlook.application")
        mail = outlook.CreateItem(0)
        mail.To = "kelvingooding@msn.com"
        mail.Subject = f"{main2} - UMC Password Reset"
        mail.Body = "Hi,\n\n" \
                    f"Your new password is: {passwd2}\n\n"
        mail.Send()

    else:
        clear()
        print("Password's do not match. Please try again.")
        time.sleep(3)
        clear()
        password_reset()

def submenu():
    Q1 = input("\nReturn to Main Menu? (Y or N): ")

    if (Q1 == "Y") or (Q1 == "y"):
        clear()
        main_menu()
    elif (Q1 == "N") or (Q1 == "n"):
        input("\nPress any key to exit..")
        sys.exit()
    else:
        clear()
        print("Incorrect answer. Please try again.")
        submenu()

def main_menu():
    print("--- User Console Main Menu ---")
    print("""
    1. View Users
    2. Add User
    3. Delete User
    4. Password Reset
    5. Exit""")

    Q1 = input("\nSelect an option: ")

    if Q1 == "1":
        clear()
        view_users()
        submenu()
    elif Q1 == "2":
        clear()
        add_user()
        submenu()
    elif Q1 == "3":
        clear()
        view_users()
        print()
        delete_user()
        submenu()
    elif Q1 == "4":
        clear()
        view_users()
        print()
        password_reset()
        submenu()
    elif Q1 == "5":
        sys.exit()
    else:
        clear()
        print("Incorrect option. please try again.")
        time.sleep(3)
        clear()
        main_menu()
main_menu()
