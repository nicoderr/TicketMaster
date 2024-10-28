GROUP 29: DELIVERABLE - 4
Ticket Management System

###### Members and Contributions #####
Nitesha Paatil, npaatil@hawk.iit.edu,  A20544932, 33.33%
Yash Kulkarni, ykulkarni@hawk.iit.edu, A20541839, 33.33%
Smitkumar Panchal, spanchal4@hawk.iit.edu, A20527904, 33.33%

##### Project Overview: #####
This projects implements an Online Ticketing System which is a desktop based application. This system is developed using Python using Tkinter for GUI and MySQL for the backend database. This project illustrates an extensive role-based system consisiting of three distinct roles:
    a. Admin: Manages users and events
    b. Organizer: Can organize events and manage events.
    c. Customer: Can view and book the events.
The system follows best practices to provide seamless interface with SQL databases for data validation, error handling, and CRUD (Create, Read, Update, and Delete) operations. It also demonstrates strong functionality, clear code structure, thorough error management, and role-based access control, all of which aligns with the rubrics.

##### Requirements: #####

1. Progrmamming Language: Python versions 3.x versions
2. Database: MySQL Server
3. Libraries:
    - mysql-connector-python (interaction with database)
    - tkinter (this comes pre-installed with python for GUI)

##### Setup #####

1. Cloning the Repository:
    - git clone <repository_url>
    - cd <your-folder-name>
2. Installing Dependencies:
    - pip install mysql-connector-python

3. Setting up MySQL Database:

    a. Set up MySQL Database:
    - Install MySQL server from the MySQL's official website: https://dev.mysql.com/downloads/. Make sure to set a root password and note down.
    - Open MySQL Workbench for accessing the environment.

    b. Create Database:
    - Open MySQL Workbench and login with root credentials.
    - Create a database named as 'ticketmanagementsystem' by running this command: CREATE DATABASE ticketmanagementsystem;
    
    c. Import Schema- Import the tables using MySQL Workbench or the CLI.
    - Open SQL script by clicking on file.
    - Import the tables by clicking on Server -> Data Import. The tables will be imported.

    d. Verify Setup:
    - Run the following to command to verify tables are imported: SHOW TABLES;

4. Configure the Credentials of Database in ConnectingDatabase.py
    - Open the file in any code editor (we have used PyCharm)
    - Edit the credentials found in the below and save changes:
        db_connection = mysql.connector.connect(
            host='localhost',      # Your MySQL host (if different)
            user='root',            # Your MySQL username
            password='your_password',  # Your MySQL password
            database='ticketmanagementsystem',  # created database name 
            port=3306               # Default MySQL port, change if different
        )

5. Run the Application:
    - In the root directory of the project, open a terminal or command prompt.
    - Ensure whether the Python libraries are installed: pip install mysql-connector-python
    - Under UserPanel, execute the following command or click on the run button: python RegistrationPage.py

##### File Structure #####

1. EventInfo.py: This code file depicts the Admin panel to manage the events.
2. Navigator.py: Navigates between the roles (RegistrationPage.py calls this function) 
3. RegistrationPage.py: Manages role-based login and user registration (main entry point)
4. tab2.py: Shows a secondary tab containing the ticket list.
5. tab3.py: tab3.py is an empty placeholder, for later use.
6. user_profile.py: User profile information is displayed.
7. ConnectingDatabase.py: Manages SQL connection.

##### Usage and CRUD Operations #####

a. Customer can:
Create:
    - Register on the registration page as a new customer.
    - After the customer successfully registers, their information is added to the USER table.
Read:
    - Customers can view the available events from the EventInfo tab. (events retreived from the EVENTS table)
Update:
    - Number of tickets available in the EVENT table is reduced by one when a ticket is booked.
    - Booking information is updated in the TICKET and BOOKING tables.
Delete:
    - Admins can delete client data if needed, but customers do not have the ability to do so.

b. Organizer can:
Create:
    - Create, manage new events and assign performers to events.
Read:
    - Organizations can view events assigned to them as well as the performer information related to those events.
Update:
    - Change the details such as dates, venues, and performers of the event.
Delete:
    - Only Admins can delete the events
Events can be deleted by Admin, however organizers can remove performers from the events.

c. Admin:
Create:
    - Add new events on the Admin Panel.
Read:
    - View users, events, and bookings in the system.
Update:
    - Modify event details or user roles as needed.
Delete:
    - Delete users, events using the Admin Panel.

##### Error Handling #####

1. Users have to login with correct role:
  Error: You cannot log in as an Admin.
2. Prevention of duplicate user registration:
  Error: User with the same details already exists.
3. Incomplete submission of form:
  Error: All fields are required.

##### Function Definitions #####

1. submit_data() in RegistrationPage.py: Uses the information from the registration form to register new users.
2. bookingProcedure() in BookingProcedure.py: Updates bookings and tickets in the database and manages the booking logic.
3. open_navigator() in Navigator.py: Navigates the user to relevant pages based on their roles.

##### Conclusion #####

This Online Ticketing Management System or Ticketmaster provides the ability for Admins to manage events and users, Organizers to manage events and performers and Customers to view and book the events. Through well-integrated CRUD operations, the system guarantees error handling, data integrity, and role-based access control for smooth operation. The application is simple to maintain and expand for future use because to its modular design and clear code.
