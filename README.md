GROUP 29: DELIVERABLE - 4
Ticket Management System

###### Members and Contributions #####
Nitesha Paatil, npaatil@hawk.iit.edu,  A20544932, 33.33%
Yash Kulkarni, ykulkarni@hawk.iit.edu, A20541839, 33.33%
Smitkumar Panchal, spanchal4@hawk.iit.edu, A20527904, 33.33%

##### Project Overview: #####
This projects implements an Online Ticketing System which is a desktop based application. This system is developed using Python using Tkinter for GUI and MySQL for the backend database. This project illustrates an extensive role-based system consisiting of three distinct roles:
    a. Admin: Manages events.
    b. Organizer: Can organize events.
    c. Customer: Can view and book the events.
The system follows best practices to provide seamless interface with SQL databases for data validation, error handling, and CRUD (Create, Read, Update, and Delete) operations. It also demonstrates strong functionality, clear code structure, thorough error management, and role-based access control, all of which aligns with the rubrics.

##### Requirements: #####

1. Progrmamming Language: Python versions 3.x versions
2. Database: MySQL Server
3. Libraries:
    - mysql-connector-python (connecting to the MySQL database)
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

TicketManagementSystem ontains two main panels: AdminPanel and UserPanel

* Includes a ConnectingDatabase.py file for database operations

AdminPanel Directory:
* EventInfo.py - The EventInfo.py file in the AdminPanel manages event-related data by connecting to a MySQL database, displaying booked events, handling upcoming event listings, and providing a user interface for ticket management through tkinter-based GUI components.
* Navigator.py - Navigator.py creates a tabbed GUI interface that displays user profile information and manages navigation between different sections of the admin panel, featuring a main window with user details and additional tabs for event information and other functionalities.
* RegistrationPage.py - RegistrationPage.py creates a user registration form with input fields for first name, last name, email, and role selection (Admin/Organization/Customer). It validates user credentials against a database and directs users to appropriate navigation panels based on their role, using tkinter for the GUI interface.
* tab2.py - Handles displaying and calculating event revenues, with filtering capabilities and detailed revenue summaries for administrative oversight.
* user_profile.py - It creates a GUI window in the Admin Panel to display a user's profile information, including their first name, last name, email, and role, using the Tkinter library.

UserPanel Directory:
* BookingProcedure.py - The BookingProcedure.py handles event booking by creating or validating user records, generating tickets, updating event availability, and confirming bookings in the ticketbookingsystem database.
* Registration.py - User registration
* RegistrationPage.py - User registration interface
* tab2.py and tab3.py - Additional tab functionalities
* user_profile.py - User profile management
* UserEventInfo.py - Event information display for users
* UserNavigator.py - Navigation for user interface


##### Usage and CRUD Operations #####

a. Customer can:
Create:
    - Register on the registration page as a new customer.
    - After the customer successfully registers, their information is added to the USER table.
Read:
    - Customers can view the available events from the EventInfo tab. (events retreived from the EVENTS table)
Update:
    - Number of tickets available in the EVENT table is reduced by one when a ticket is booked.

b. Organizer can:
Create:
    - Create new events and assign performers to events.
Read:
    - Organizations can view events.

c. Admin:
Create:
    - Add new events.
Read:
    - View events in the system.
Delete:
    - Only Admins can delete the events.

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
