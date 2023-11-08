import sqlite3
import csv
import random

conn = sqlite3.connect('C:/Users/Owner/DataGripProjects/CPSC408/identifier.sqlite')  # establish connection to db
mycursor = conn.cursor()  # the cursor allows python to execute SQL statements

# Write a python function to import the students.csv file into your newly created Students table
advisors = ['Rene German', 'Micheal Fahy', 'Erik Linstead', 'Elizabeth Stevens']
state_names = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut",
               "District of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois",
               "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan",
               "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska",
               "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon",
               "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas",
               "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]


def import_students():
    with open('C:/Users/Owner/Downloads/students.csv') as csvfile:
        reader = csv.DictReader(csvfile)  # DictReader takes first line as header
        for row in reader:
            index = random.randint(0,
                                   3)  # create random number (to randomly chose an advisor of the list provided above)
            advisor = advisors[index]
            print('importing data...')
            mycursor.execute(
                "INSERT INTO Student(FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber, isDeleted)"
                "VALUES (?,?,?,?,?,?,?,?,?,?,?);", (row['FirstName'], row['LastName'], row['GPA'],
                                                    row['Major'], advisor, row['Address'],
                                                    row['City'], row['State'], row['ZipCode'],
                                                    row['MobilePhoneNumber'], False))
            conn.commit()
    print('data import complete')


# DISPLAY ALL STUDENTS
def display_all_students():
    mycursor.execute("SELECT * FROM Student WHERE isDeleted = False;")
    output = mycursor.fetchall()  # fetch information from query
    for row in output:
        print(row)  # print information by row


def fetch_student():
    while True:
        student_id = input("Student ID of the student you are requesting: ")  # prompt user for student ID
        # check if student exists in database
        mycursor.execute("SELECT StudentID FROM Student WHERE StudentID = ?", (student_id,))
        fetched_id = mycursor.fetchone()

        if fetched_id:  # if student is in database
            mycursor.execute("SELECT FirstName, LastName FROM Student WHERE StudentID = ?",
                             (student_id,))  # get student's first and last name
            student_fn, student_ln = mycursor.fetchone()
            print("The student you are requesting is", student_fn, student_ln,
                  "correct? (answer with yes or no)")  # ask if user is asking for the correct student
        else:  # student does not exist, ask user if they want to try again
            print("Student does not exist")
            if not try_again():  # user does not want to continue (leave function)
                return
            continue

        correct_student = input()
        if correct_student == "yes":  # correct student found
            break

    return student_id  # return student ID knowing it exists and is the right ID


def is_deleted_student(student_id):  # takes in student_id, returns true or false depending on whether student is deleted or not
    mycursor.execute("SELECT * FROM Student WHERE StudentID = ?", (student_id,))
    output = mycursor.fetchone()
    if output[11] == 1:  # student isDeleted = true
        return True
    elif output[11] == 0:  # student isDeleted = false
        return False


def in_database(attribute, look_up):  # check if input is existing in the database, takes in column to look at and what to find in column
    count = 0
    mycursor.execute("SELECT * FROM Student WHERE %s = ?" % attribute, (look_up,))
    output = mycursor.fetchall()  # returns none if not in database
    if output:
        for row in output:
            if row[11] == 0:  # make sure all of these students aren't deleted
                count = count + 1
            if count == 0:
                return False
        return True  # exists in database
    else:
        return False  # does not exist in database


def try_again():
    while True:
        user_decision = input(
            "Would you like to try again (answer with yes or no)? ")  # asks user if they want to try again
        if user_decision == "no":  # user foes not want to try again
            return False
        elif user_decision == "yes":  # user wants to try again
            return True
        print("Invalid input")  # user did not say yes or no, automatically asked again if they want to try again


symbols = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", ",", "?", "/", "=", "+", ":", ";", "[", "]", "{", "}"]
def valid_input(user_input, attribute):
    if attribute == "string": # first name, last name, major, faculty advisor, city
        if any(chr1.isdigit() for chr1 in user_input): # make sure it does not include a number
            return False
        for chr2 in user_input:
            if chr2 in symbols: # make sure it does not include a symbol
                return False
    elif attribute == "state": # state
        if not (user_input in state_names):
            return False
    elif attribute == "number":
        if not any(chr3.isdigit() for chr3 in user_input): # input can only be a number
            return False
    elif attribute == "gpa":
        if not any(chr4.isdigit() for chr4 in user_input): # input must be a number
            if user_input != ".": # if it is not a number than it has to be decimal
                return False
    elif attribute == "phone":
        if not any(chr5.isdigit() for chr5 in user_input): # input must be a number
            if user_input != "-": # if it is not a number than it has to be a dash
                return False
    elif attribute == "address":
        for chr6 in user_input:
            if chr6 in symbols: # input must not include a symbol
                return False
    return True

def check_valid(user_input, attribute, ask_string):
    new_input = ""
    while not valid_input(user_input, attribute):
        print("Invalid input")
        if not try_again():
            return "invalid"
        new_input = input(ask_string)
        user_input = new_input
    return new_input

# ADD NEW STUDENT
# All attributes are required when creating a new student.
# Please make sure to validate user input appropriately.
def add_new_student():
    #FIRST NAME
    first_name = input("First name: ")
    first_name = check_valid(first_name, "string", "First name: ")
    if first_name == "invalid":
        print("Returning to main menu...")
        return
    #LAST NAME
    last_name = input("Last name: ")
    last_name = check_valid(last_name, "string", "Last name: ")
    if last_name == "invalid":
        print("Returning to main menu...")
        return
    #GPA
    gpa = input("GPA: ")
    gpa = check_valid(gpa, "gpa", "GPA: ")
    if gpa == "invalid":
        print("Returning to main menu...")
        return
    #MAJOR
    major = input("Major: ")
    major = check_valid(major, "string", "Major: ")
    if major == "invalid":
        print("Returning to main menu...")
        return
    #FACULTY ADVISOR
    faculty_advisor = input("Faculty Advisor: ")
    faculty_advisor = check_valid(faculty_advisor, "string", "Faculty Advisor: ")
    if faculty_advisor == "invalid":
        print("Returning to main menu...")
        return
    #ADDRESS
    address = input("Address: ")
    address = check_valid(address, "address", "Address: ")
    if address == "invalid":
        print("Returning to main menu...")
        return
    #CITY
    city = input("City: ")
    city = check_valid(city, "string", "City: ")
    if city == "invalid":
        print("Returning to main menu...")
        return
    #STATE
    state = input("State: ")
    state = check_valid(state, "state", "State: ")
    if state == "invalid":
        print("Returning to main menu...")
        return
    #ZIP CODE
    zip_code = input("Zip Code: ")
    zip_code = check_valid(zip_code, "number", "Zip Code: ")
    if zip_code == "invalid":
        print("Returning to main menu...")
        return
    #MOBILE PHONE NUMBER
    mobile_number = input("Mobile Phone Number (format xxx-xxx-xxxx): ")
    mobile_number = check_valid(mobile_number, "phone", "Mobile Phone Number (format xxx-xxx-xxxx): ")
    if mobile_number == "invalid":
        print("Returning to main menu...")
        return

    mycursor.execute(
        "INSERT INTO Student(FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber, isDeleted)"
        "VALUES (?,?,?,?,?,?,?,?,?,?,?);", (first_name, last_name, gpa,
                                            major, faculty_advisor, address,
                                            city, state, zip_code,
                                            mobile_number, False))
    conn.commit()
    print("New student successfully added!")


# UPDATE STUDENT
# Only the following fields can be updated: Major, Advisor, MobilePhoneNumber
def update_info(attribute):
    if attribute == "major":  # user wants to update major
        update_major()
    elif attribute == "advisor":  # user wants to update advisor
        update_advisor()
    elif attribute == "phone number":  # user wants to update phone number
        update_phone_number()
    else:
        print("I'm sorry that is an attribute that cannot be updated.")  # user input invalid
        if not try_again():
            return
        else:
            attribute = input(
                "What would like to update? ").lower()  # if user decides to continue, re-prompt for what they want to update
            update_info(attribute)


def update_major():
    student_to_update = fetch_student()  # ask user what student they want to update
    new_major = input("New major: ")
    mycursor.execute("UPDATE Student SET Major = ? WHERE StudentID = ?", (new_major, student_to_update))
    conn.commit()
    print("Major successfully updated!")


def update_advisor():
    student_to_update = fetch_student()  # ask user what student they want to update
    new_advisor = input("New advisor: ")
    mycursor.execute("UPDATE Student SET FacultyAdvisor = ? WHERE StudentID = ?", (new_advisor, student_to_update))
    conn.commit()
    print("Advisor successfully updated!")


def update_phone_number():
    student_to_update = fetch_student()  # ask user what student they want to update
    new_num = input("New mobile phone number: ")
    mycursor.execute("UPDATE Student SET MobilePhoneNumber = ? WHERE StudentID = ?", (new_num, student_to_update))
    conn.commit()
    print("Mobile phone number successfully updated!")


# Delete Students by StudentId
# Perform a “soft” delete on students that is, set isDeleted to true (1)
def delete_student():
    student_to_delete = fetch_student()  # ask user what student they want to delete
    while is_deleted_student(student_to_delete):  # if student is already deleted try another student
        print("Student already deleted")
        if not try_again():
            return
        student_to_delete = fetch_student()
    mycursor.execute("UPDATE Student SET isDeleted = ? WHERE StudentID = ?", (True, student_to_delete))
    conn.commit()
    print("Student successfully deleted!")


# DISPLAY STUDENT
# Options: by Major, GPA, City, State and Advisor.
def display_info(attribute, display_by):  # display info of given attribute and user input option
    mycursor.execute("SELECT * FROM Student WHERE %s = ?" % attribute, (display_by,))
    output = mycursor.fetchall()
    for row in output:
        if row[11] != 1:  # if student is deleted, do not display student
            print(row)


def display_by_major():
    major = input("Major: ")
    while not in_database("Major", major):  # check if major exists
        print("Major does not exist")
        if not try_again():
            return
        major = input("Major: ")
    display_info("Major", major)  # display those of the major


def display_by_gpa():
    gpa = input("GPA: ")
    while not in_database("GPA", gpa):  # check if students with requested gpa exist
        print("There are no students with that GPA")
        if not try_again():
            return
        gpa = input("GPA: ")
    display_info("GPA", gpa)  # display those of requesting gpa


def display_by_city():
    city = input("City: ")
    while not in_database("City", city):  # check if students from requested city exist
        print("There are no students from that city")
        if not try_again():
            return
        city = input("City: ")
    display_info("City", city)  # display those of requested city


def display_by_state():
    state = input("State: ")
    while not in_database("State", state):  # check if students from requested state exist
        print("There are no students from that state")
        if not try_again():
            return
        state = input("State: ")
    display_info("State", state)  # display those of requested state


def display_by_advisor():
    advisor = input("Faculty advisor: ")
    while not in_database("FacultyAdvisor", advisor):  # check if students under requested advisor exist
        print("There are no students under that advisor")
        if not try_again():
            return
        advisor = input("Faculty advisor: ")
    display_info("FacultyAdvisor", advisor)  # display those under requested advisor


def what_to_display(display_option):
    if display_option == "major":
        display_by_major()
    elif display_option == "gpa":
        display_by_gpa()
    elif display_option == "city":
        display_by_city()
    elif display_option == "state":
        display_by_state()
    elif display_option == "advisor":
        display_by_advisor()
    else:
        print("Invalid input")
        if not try_again():
            return
        display_option = input("What would you like to search by? (Major, GPA, City, State, Advisor) ").lower()
        what_to_display(display_option)


def options():
    print("1. Add new student")
    print("2. Update student information")
    print("3. Delete student from database")
    print("4. Search for student")


def main():
    print("Welcome!")
    while True:
        options()
        decision = input("What would you like to do today (type corresponding number)? ")
        if decision == "1":
            print("Please provide the following information to add student to database")
            add_new_student()
        elif decision == "2":
            attribute_to_update = input(
                "What would like to update? (choose one of the following: major, advisor, phone number) ").lower()
            update_info(attribute_to_update)
        elif decision == "3":
            delete_student()
        elif decision == "4":
            display_option = input("What would you like to search by? (Major, GPA, City, State, Advisor) ").lower()
            what_to_display(display_option)
        else:
            print("Invalid option")
            # try again option, display options

        again = input("Would you like to choose another option? (please answer with yes or no) ") # would user like to pick another option
        if again == "yes":
            continue
        elif again == "no":
            break
        else:
            print("Invalid input")
            if not try_again():
                break

    print("Goodbye!")
    mycursor.close()


if __name__ == "__main__":
    main()
