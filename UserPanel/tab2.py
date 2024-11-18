import tkinter as tk
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
from UserPanel import Registration
import datetime  # For working with dates

# Database connection
try:
    db_connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='nitu24',
        database='ticket_management_system'
    )
    if db_connection.is_connected():
        cursor = db_connection.cursor()
        print("Database connection successful")
except Error as err:
    print(f"Error: {err}")
    exit(1)  # Exit if connection fails

def load_ticket_list(tab2_frame):
    global cursor, db_connection

    # Ensure the database connection is valid
    if not db_connection.is_connected():
        db_connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='nitu24',
            database='ticket_management_system'
        )
        cursor = db_connection.cursor()

    # Clear existing content from the UI
    for widget in tab2_frame.winfo_children():
        widget.destroy()

    # Retrieve user details
    email = Registration.get_email()
    if not email:
        tk.Label(tab2_frame, text="User email not found. Please log in again.", font=("Arial", 12), fg="red").pack(pady=20)
        return

    # Fetch user_id using email
    cursor.execute("SELECT user_id FROM USER WHERE email = %s LIMIT 1", (email,))
    result = cursor.fetchone()
    user_id = result[0] if result else None

    if user_id:
        # Aggregate Function query: Fetch booked events for the user.
        # Explanation: This query uses the COUNT aggregate function to count the number of bookings (booking_id) for each
        # event that the user has booked. The GROUP BY clause is used to group results by event_name, event_date, start_time,
        # and end_time.
        cursor.execute("""
            SELECT EVENT.event_name, EVENT.event_date, EVENT.start_time, EVENT.end_time, COUNT(BOOKING.booking_id) AS user_bookings
            FROM EVENT
            JOIN TICKET ON EVENT.event_id = TICKET.event_id
            LEFT JOIN BOOKING ON TICKET.ticket_id = BOOKING.ticket_id
            WHERE BOOKING.user_id = %s
            GROUP BY EVENT.event_name, EVENT.event_date, EVENT.start_time, EVENT.end_time;
        """, (user_id,))

        booked_events = cursor.fetchall()

        if booked_events:
            # Display booked events in the UI
            for event in booked_events:
                event_name, event_date, start_time, end_time, user_bookings = event

                # Create a frame for each event
                event_frame = ttk.Frame(tab2_frame, borderwidth=2, relief="ridge", padding=10)
                event_frame.pack(fill=tk.X, padx=10, pady=5)

                # Add event details to the frame
                event_details = (
                    f"Event Name: {event_name}\n"
                    f"Event Date: {event_date}\n"
                    f"Start Time: {start_time}\n"
                    f"End Time: {end_time}\n"
                    f"Bookings by User: {user_bookings}"
                )
                label = tk.Label(event_frame, text=event_details, justify="left")
                label.pack(side="left", padx=10)
        else:
            tk.Label(tab2_frame, text="No booked events found for this user.", font=("Arial", 12), fg="red").pack(pady=20)
    else:
        # If user does not exist, show a message
        tk.Label(tab2_frame, text="User does not exist or has not booked any events.", font=("Arial", 12), fg="red").pack(pady=20)

    # Add the refresh button again to reload the list
    # refresh_button = ttk.Button(tab2_frame, text="Refresh Booked Events", command=lambda: load_ticket_list(tab2_frame))
    # refresh_button.pack(side="bottom", pady=5)

    # Optionally, add a button for booking new events
    book_button = ttk.Button(tab2_frame, text="Upcoming Event", command=lambda: book_new_event(tab2_frame))
    book_button.pack(side="bottom", pady=5)


def book_new_event(tab2_frame):
    # Get today's date and calculate the date 10 days from now
    today = datetime.date.today()
    end_date = today + datetime.timedelta(days=10)

    # Generate a list of dates from today to 10 days from now
    date_list = [(today + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(11)]

    # Convert the list of dates into a comma-separated string for the IN query
    date_string = ', '.join(f"'{date}'" for date in date_list)

    # Set Membership: Query to get events within the next 10 days using IN for membership query

    # Explanation: This query checks if event_date is in a set of dates (generated as a string). The IN operator is a
    # set membership operation that verifies if a value exists within a specified set.
    cursor.execute(f"""
        SELECT event_name, event_date, start_time, end_time
        FROM EVENT
        WHERE event_date IN ({date_string})
        ORDER BY event_date;
    """)

    upcoming_events = cursor.fetchall()

    # Clear existing content in the tab before displaying new events
    for widget in tab2_frame.winfo_children():
        widget.destroy()

    if upcoming_events:
        # Display each upcoming event in a block UI
        for event in upcoming_events:
            event_name, event_date, start_time, end_time = event

            # Create a frame for each event
            event_frame = ttk.Frame(tab2_frame, borderwidth=2, relief="ridge", padding=10)
            event_frame.pack(fill=tk.X, padx=10, pady=5)

            # Display event details
            event_details = (
                f"Event Name: {event_name}\n"
                f"Event Date: {event_date}\n"
                f"Start Time: {start_time}\n"
                f"End Time: {end_time}"
            )
            label = tk.Label(event_frame, text=event_details, justify="left")
            label.pack(side="left", padx=10)
    else:
        tk.Label(tab2_frame, text="No upcoming events in the next 10 days.", font=("Arial", 12), fg="red").pack(pady=20)

def TicketList(notebook):
    tab2_frame = tk.Frame(notebook)
    notebook.add(tab2_frame, text="Booked Event")

    # Bind event for tab switching
    def on_tab_changed(event):
        selected_tab = event.widget.index("current")
        if selected_tab == notebook.index(tab2_frame):  # Check if "Booked Events" tab is selected
            load_ticket_list(tab2_frame)

    notebook.bind("<<NotebookTabChanged>>", on_tab_changed)
