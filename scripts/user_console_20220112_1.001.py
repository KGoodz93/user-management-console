# Release Notes

"""
Version 1.000 Release Notes

- Fixed security exploit.
"""

# Modules

import sqlite3
import getpass
import sys
import os

# Variables

user = os.getlogin()
clear = lambda: os.system("cls")

# Database

db = fr"C:\Users\{user}\Dropbox\Coding\Python\Projects\User Management Console\db\users.db"
connection = sqlite3.connect(db)
cursor = connection.cursor()
table = "credentials"
print("Successfully Connected to SQLite3!")

def login():
    username = input("\nEnter Username: ")
    passwd = getpass.getpass("Enter Password: ")

    cursor.execute("SELECT loginid, password FROM " + table + " WHERE loginid=(?) and password=(?);", (username, passwd,))

    result = cursor.fetchone()
    if result != (username, passwd):
        clear()
        print("Login failed. Please try again.")
        login()
    else:
        clear()
        print(f"Success! Logged in as: {username}")

login()


def view_users():
    print("--- View UID ---")
    print("\nThese users are currently active: \n")

    viewusers = cursor.execute("SELECT * FROM CREDENTIALS order by accountcreation DESC;")

    for i in viewusers:
        print(i[2], "- " + i[0], i[1])

def add_user():
    print("--- Add Users ---")

    value1 = input("\nEnter First Name: ")
    value2 = input("Enter Last Name: ")
    value3 = (value2[0:5].lower() + value1[0:3].lower())
    value4 = "summer2020!"

    try:
        cursor.execute("INSERT INTO " + table + " VALUES (?,?,?,?,CURRENT_TIMESTAMP, NULL)", (value1, value2, value3, value4))
        connection.commit()
    except:
        print("\nThis user already exists! Please try again")
        add_user()
    else:
        print("\nAccount has been created: ")
        print("\nName: " + value1 + " " + value2)
        print("UID: " + value3)
        print("Password: " + value4)
        print("\n(The password for this UID will only be shown once.)")

def delete_user():
    print("--- Delete User ---")

    main1 = input("\nEnter a UID: ")

    cursor.execute("DELETE FROM " + table + " WHERE loginid=(?)", (main1,))
    connection.commit()

    print("\nThe below user has been deleted:\n\n" + main1)

def password_reset():
    print("--- Password Reset ---")

    main2 = input("\nEnter UID: ")
    main3 = getpass.getpass("Enter New Password: ")

    cursor.execute("UPDATE " + table + " SET password=(?), lastpasschange=(CURRENT_TIMESTAMP) WHERE loginid=(?)", (main3, main2))
    connection.commit()

    print("\nPassword has been changed!")

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
    print("\n--- User Console Main Menu ---")
    print("\n1. View Users"
          "\n2. Add User"
          "\n3. Delete User"
          "\n4. Password Reset")

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
    else:
        clear()
        print("\nIncorrect option, please try again.")
        main_menu()
main_menu()

