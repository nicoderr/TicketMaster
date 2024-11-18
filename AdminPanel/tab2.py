import tkinter as tk
from tkinter import ttk
import mysql.connector
from mysql.connector import Error

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


def load_events_and_revenue_by_category(tab2_frame, selected_category=None):
    # Clear existing content
    for widget in tab2_frame.winfo_children():
        widget.destroy()

    # Aggregate Function: Query to retrieve event details and total revenue by category
    # This query calculates the total revenue (SUM(E.total_price)) for each event and groups the results by category_name
    # and event_name.

    query = """
        SELECT 
            EC.category_name, 
            E.event_name, 
            SUM(E.total_price) AS total_revenue
        FROM 
            EVENT E
        JOIN 
            EVENTCATEGORY EC ON E.event_category = EC.category_id
        LEFT JOIN 
            TICKET T ON E.event_id = T.event_id
    """
    conditions = []
    params = []

    if selected_category and selected_category != "All Categories":
        # Set Operation: This dynamic filtering introduces a set comparison where the selected category is matched with
        # category_name. It ensures that only events belonging to the selected category are retrieved.
        conditions.append("EC.category_name = %s")
        params.append(selected_category)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += """
        GROUP BY EC.category_name, E.event_name
        ORDER BY EC.category_name, total_revenue DESC;
    """

    cursor.execute(query, tuple(params))
    event_data = cursor.fetchall()

    if event_data:
        current_category = None
        category_total_revenue = 0

        # Display each event with its revenue
        for category, event_name, total_revenue in event_data:
            if current_category != category:
                # If a new category starts, display the total revenue of the previous category
                if current_category is not None:
                    tk.Label(tab2_frame, text=f"Total Revenue for {current_category}: ${category_total_revenue:.2f}",
                             font=("Arial", 12, "italic"), fg="blue").pack(pady=5)
                # Add a header for the new category
                tk.Label(tab2_frame, text=f"Category: {category}",
                         font=("Arial", 14, "bold")).pack(pady=10)
                current_category = category
                category_total_revenue = 0  # Reset for the new category

            # Add the event's revenue to the category's total revenue
            category_total_revenue += total_revenue

            # Create a frame for each event
            event_frame = ttk.Frame(tab2_frame, borderwidth=2, relief="ridge", padding=10)
            event_frame.pack(fill=tk.X, padx=10, pady=5)

            # Display event name and total revenue
            event_details = f"Event Name: {event_name}\nEvent Revenue: ${total_revenue:.2f}"
            label = tk.Label(event_frame, text=event_details, justify="left")
            label.pack(side="left", padx=10)

        # Display the total revenue for the last category
        tk.Label(tab2_frame, text=f"Total Revenue for {current_category}: ${category_total_revenue:.2f}",
                 font=("Arial", 12, "italic"), fg="blue").pack(pady=5)
    else:
        tk.Label(tab2_frame, text="No events or revenue data available.", font=("Arial", 12), fg="red").pack(pady=20)


    # OLAP Query - Running total revenue by category
    # This is an OLAP query because it uses a window function (OVER) to calculate a running total of revenue for each
    # category (PARTITION BY EC.category_name). It orders events within each category by event_name.
    olap_query = """
        SELECT 
            EC.category_name,
            E.event_name,
            SUM(E.total_price) AS total_revenue,
            SUM(SUM(E.total_price)) OVER (PARTITION BY EC.category_name ORDER BY E.event_name) AS running_total
        FROM 
            EVENT E
        JOIN 
            EVENTCATEGORY EC ON E.event_category = EC.category_id
        LEFT JOIN 
            TICKET T ON E.event_id = T.event_id
        GROUP BY 
            EC.category_name, E.event_name
        ORDER BY 
            EC.category_name, total_revenue DESC;
    """

    cursor.execute(olap_query)
    olap_data = cursor.fetchall()


def create_tab2(notebook):
    tab2_frame = tk.Frame(notebook)
    notebook.add(tab2_frame, text="Events and Revenue by Category")

    # Create a filter section at the top
    filter_frame = ttk.Frame(tab2_frame)
    filter_frame.pack(fill=tk.X, pady=10)

    tk.Label(filter_frame, text="Filter by Category:").pack(side="left", padx=10)

    # Subquery + WITH Clause: Dropdown for category selection using WITH clause.
    # This query defines a CTE (CategoryEvents) to extract distinct categories by joining EVENTCATEGORY and EVENT. The
    # outer query simply retrieves category_name. While it’s not an OLAP query, it’s a subquery-based operation using
    # a WITH clause.
    cursor.execute("""
        WITH CategoryEvents AS (
            SELECT DISTINCT EC.category_name
            FROM EVENTCATEGORY EC
            JOIN EVENT E ON E.event_category = EC.category_id
        )
        SELECT category_name
        FROM CategoryEvents
    """)

    categories = [row[0] for row in cursor.fetchall()]
    category_var = tk.StringVar(value="All Categories")

    category_dropdown = ttk.Combobox(filter_frame, textvariable=category_var, values=["All Categories"] + categories)
    category_dropdown.pack(side="left", padx=10)

    def apply_filter():
        selected_category = category_var.get() if category_var.get() != "All Categories" else None
        load_events_and_revenue_by_category(content_frame, selected_category)

    # Apply button for filter
    apply_button = ttk.Button(filter_frame, text="Apply Filter", command=apply_filter)
    apply_button.pack(side="left", padx=10)

    # Create a canvas to hold the content and a vertical scrollbar
    canvas = tk.Canvas(tab2_frame)
    scrollbar = ttk.Scrollbar(tab2_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas that will hold all the widgets
    content_frame = tk.Frame(canvas)

    # Create a window in the canvas to hold the content_frame
    canvas.create_window((0, 0), window=content_frame, anchor="nw")
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Load and display the events with revenue
    load_events_and_revenue_by_category(content_frame)

    # Update scroll region to match the size of content
    content_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


# Main Application Window
def main():
    root = tk.Tk()
    root.title("Ticket Booking System")

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    # Add Tab2
    create_tab2(notebook)

    root.mainloop()