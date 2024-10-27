import tkinter as tk
from tkinter import ttk, messagebox
from ConnectingDatabase import cursor, db_connection  # Ensure the correct import for database connection
import Navigator
import re

# Function to handle form submission
def submit_data():
    first_name = first_name_entry.get().strip()
    last_name = last_name_entry.get().strip()
    email = email_entry.get().strip()
    role = role_combobox.get()

    # Validate that all fields are filled
    if not first_name or not last_name or not email:
        messagebox.showwarning("Input Error", "First name, last name, and email are required!")
        return

    # Validate email format
    if not is_valid_email(email):
        messagebox.showwarning("Input Error", "Please enter a valid email address!")
        return

    # Check if the user exists with the matching details
    check_query = "SELECT * FROM USER WHERE first_name = %s AND last_name = %s AND email = %s AND role = %s"
    cursor.execute(check_query, (first_name, last_name, email, role))
    result = cursor.fetchone()

    if result:
        # User exists, proceed to open navigator
        root.destroy()
        Navigator.open_navigator(first_name, last_name, email, role)
    else:
        # User does not exist, check if they exist with all the same details
        check_user_existence(first_name, last_name, email, role)

# Function to check if the user exists with the same details
def check_user_existence(first_name, last_name, email, role):
    check_query = "SELECT * FROM USER WHERE first_name = %s AND last_name = %s AND email = %s"
    cursor.execute(check_query, (first_name, last_name, email))
    existing_user = cursor.fetchone()

    if existing_user:
        messagebox.showerror("Registration Failed", "User with the same details already exists.")
    else:
        # Prevent insertion for Admin and Organization roles
        if role in ["Admin", "Organization"]:
            messagebox.showerror("Registration Failed", f"Users cannot be registered with the role '{role}'.")
        else:
            insert_user(first_name, last_name, email, role)

# Function to insert user data into the database
def insert_user(first_name, last_name, email, role):
    insert_query = "INSERT INTO USER (first_name, last_name, email, role) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(insert_query, (first_name, last_name, email, role))
        db_connection.commit()  # Commit the transaction to save changes
        messagebox.showinfo("Success", "User registered successfully!")
        root.destroy()
        Navigator.open_navigator(first_name, last_name, email, role)
    except Exception as e:
        # Print the error message for debugging
        print(f"Failed to register user: {str(e)}")
        messagebox.showerror("Error", f"Failed to register user: {str(e)}")

# Function to validate email format
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

# Function to create the form
def create_form():
    global frame, first_name_entry, last_name_entry, email_entry, role_combobox

    frame = tk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="First Name").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    first_name_entry = tk.Entry(frame)
    first_name_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(frame, text="Last Name").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    last_name_entry = tk.Entry(frame)
    last_name_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(frame, text="Email").grid(row=2, column=0, padx=10, pady=10, sticky="e")
    email_entry = tk.Entry(frame)
    email_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(frame, text="Role").grid(row=3, column=0, padx=10, pady=10, sticky="e")
    role_combobox = ttk.Combobox(frame, values=["Admin", "Organization", "Customer"], state="readonly")
    role_combobox.grid(row=3, column=1, padx=10, pady=10)

    submit_button = tk.Button(frame, text="Submit", command=submit_data)
    submit_button.grid(row=4, column=0, columnspan=2, pady=20)


# Create and start the main application window
root = tk.Tk()
root.title("User Information Form")
root.geometry("400x300")
create_form()
root.mainloop()
