import os
import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

data_loaded = False  # Initialize the data_loaded variable

# Function to add a new employee to the database
def add_employee():
    name = name_entry.get()
    try:
        salary = float(salary_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid salary.")
        return
    
    current_time = datetime.now().strftime("%Y-%m-%d")
    employees.append({'name': name, 'salary': salary, 'date': current_time})
    update_display()
    # Clear entry fields
    name_entry.delete(0, tk.END)
    salary_entry.delete(0, tk.END)
    
    # Automatically save data after adding an employee
    save_data()


# Function to delete an employee from the database
def delete_employee():
    index = text.curselection()
    if index:
        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete this employee?")
        if confirm:
            del employees[index[0]]
            update_display()
            # Automatically save data after deleting an employee
            save_data()
    else:
        messagebox.showerror("Error", "Please select an employee to delete.")

# Function to update the salary of an existing employee
def update_salary():
    index = text.curselection()
    if index:
        try:
            new_salary = float(new_salary_entry.get())
            employees[index[0]]['salary'] = new_salary
            update_display()
            # Automatically save data after update a salary
            save_data()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid salary.")
    else:
        messagebox.showerror("Error", "Please select an employee to update.")

# Function to save employee data to a file
def save_data():
    global data_loaded  # Declare data_loaded as global
    if not os.path.exists("employee_data.txt") or (os.path.exists("employee_data.txt") and data_loaded):
        with open("employee_data.txt", "w") as file:
            for employee in employees:
                file.write(f"{employee['name']},{employee['salary']},{employee['date']}\n")
        messagebox.showinfo("Success", "Employee data saved successfully.")
    else:
        messagebox.showinfo("Info", "Employee data is not loaded. Save operation is not allowed.")


# Function to load employee data from a file
data_loaded = False  # Initialize the flag
def load_data():
    global data_loaded  # Declare data_loaded as global
    if not data_loaded:  # Check if data is not already loaded
        try:
            with open("employee_data.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    data = line.strip().split(',')
                    if len(data) == 3:  # Ensure all required fields are present
                        name, salary, date = data
                        employees.append({'name': name, 'salary': float(salary), 'date': date})
                    else:
                        messagebox.showwarning("Warning", "Some data in the file is invalid.")
            update_display()
            messagebox.showinfo("Success", "Employee data loaded successfully.")
            data_loaded = True  # Set the flag to True after loading data
        except FileNotFoundError:
            messagebox.showerror("Error", "No employee data found.")
            data_loaded = False  # Set the flag to False if no data file is found
    else:
        messagebox.showinfo("Info", "Employee data is already loaded.")


# Function to sort employees by name or salary
def sort_employees(sort_key):
    employees.sort(key=lambda x: x[sort_key])
    update_display()

# Function to search for employees by name or date
def search_employee():
    query = search_entry.get().lower()

    # Search by name
    name_results = [employee for employee in employees if query in employee['name'].lower()]
    date_results = []

    # If not found in name, check if it's a valid date
    if not name_results:
        try:
            query_date = datetime.strptime(query, '%d-%m-%Y').strftime('%Y-%m-%d')
            date_results = [employee for employee in employees if query_date in employee['date']]
        except ValueError:
            try:
                query_date = datetime.strptime(query, '%d.%m.%Y').strftime('%Y-%m-%d')
                date_results = [employee for employee in employees if query_date in employee['date']]
            except ValueError:
                pass

    results = name_results + date_results

    if results:
        text.delete(0, tk.END)
        for employee in results:
            text.insert(tk.END, f"Name: {employee['name']}, Salary: {employee['salary']}, Date: {employee.get('date', 'N/A')}\n")
    else:
        messagebox.showinfo("Search", "No matching employees found.")

# Function to export filtered employee data to Excel and text file in a folder named "output"
def export_data():
    search_query = search_entry.get().lower()
    search_results = []

    # Search for matching employees
    if search_query:
        # Search by name
        name_results = [employee for employee in employees if search_query in employee['name'].lower()]
        date_results = []

        # If not found in name, check if it's a valid date
        if not name_results:
            try:
                query_date = datetime.strptime(search_query, '%d-%m-%Y').strftime('%Y-%m-%d')
                date_results = [employee for employee in employees if query_date in employee['date']]
            except ValueError:
                try:
                    query_date = datetime.strptime(search_query, '%d.%m.%Y').strftime('%Y-%m-%d')
                    date_results = [employee for employee in employees if query_date in employee['date']]
                except ValueError:
                    pass

        search_results = name_results + date_results
    else:
        search_results = employees

    if search_results:
        # Create the output folder if it doesn't exist
        if not os.path.exists("output"):
            os.makedirs("output")
        
        # Export data to Excel file
        excel_file_path = os.path.join("output", "employee_data.xlsx")
        df = pd.DataFrame(search_results)
        df.to_excel(excel_file_path, index=False)
        
        # Export data to text file
        txt_file_path = os.path.join("output", "employee_data.txt")
        with open(txt_file_path, "w") as file:
            for employee in search_results:
                # Format salary without decimal point and trailing zeros
                formatted_salary = f"{employee['salary']:.0f}"
                file.write(f"{employee['name']},{formatted_salary},{employee['date']}\n")
                
        messagebox.showinfo("Export", "Filtered employee data exported to Excel and text file in 'output' folder successfully.")
    else:
        messagebox.showinfo("Export", "No matching employee data available to export.")

# Function to export filtered employee data to a text file by a specific date
def export_data_by_date():
    today_date = datetime.now().strftime('%Y-%m-%d')
    user_choice = messagebox.askyesno("Export by Date", f"Do you want to export data for today's date ({today_date})?")

    if user_choice:
        search_results = [employee for employee in employees if employee['date'] == today_date]
        specific_date = today_date  # Set specific_date to today_date
    else:
        specific_date = simpledialog.askstring("Export by Date", "Enter the date (YYYY-MM-DD):")
        if specific_date is None:  # If user cancels the operation, return early
            return
        
        search_results = [employee for employee in employees if employee['date'] == specific_date]

    if search_results:
        # Calculate total salary
        total_salary = sum(employee['salary'] for employee in search_results)

        # Create the output folder if it doesn't exist
        if not os.path.exists("output"):
            os.makedirs("output")
        
        # Export data to text file
        txt_file_path = os.path.join("output", f"employee_data_{specific_date}.txt")
        with open(txt_file_path, "w") as file:
            # Header
            file.write(" شركه ابناء عرفات \n")
            file.write(" رواتب الموظفين \n")
            file.write(f" {specific_date} \n\n")
            
            # Employee data
            for employee in search_results:
                formatted_salary = f"{employee['salary']} شيكل"
                file.write(f"{employee['name'].ljust(10)}{formatted_salary.rjust(20)}\n")
            
            # Separate line
            file.write("\n*************************\n")
            
            # Total amount
            total_line = f"المجموع الكلي: {total_salary} شيكل"
            file.write(total_line.center(40) + "\n")
            
            # Separate line
            file.write("*************************\n")
                
        messagebox.showinfo("Export by Date", "Employee data for the specified date exported to text file in 'output' folder successfully.")
    else:
        messagebox.showinfo("Export by Date", "No employee data available for the specified date.")

# Function to visualize employee data
def visualize_data():
    if employees:
        df = pd.DataFrame(employees)
        df.plot(kind='bar', x='name', y='salary', rot=45)
        plt.xlabel('Employee')
        plt.ylabel('Salary')
        plt.title('Employee Salary Distribution')
        plt.tight_layout()
        plt.show()
    else:
        messagebox.showinfo("Data Visualization", "No employee data available to visualize.")

# Function to update the display with current employee data
def update_display():
    text.delete(0, tk.END)
    for employee in employees:
        text.insert(tk.END, f"Name: {employee['name']}, Salary: {employee['salary']}, Date: {employee.get('date', 'N/A')}\n")

# Function to export filtered employee data to a text file by a specific month and year
def export_data_by_month():
    month_year = simpledialog.askstring("Export by Month", "Enter the month and year (MM/YYYY):")
    if month_year is None:  # If user cancels the operation, return early
        return

    try:
        month, year = map(int, month_year.split('/'))
        if not (1 <= month <= 12 and year >= 1900):
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid month and year (MM/YYYY).")
        return

    # Filter employees by month and year
    search_results = [employee for employee in employees if datetime.strptime(employee['date'], '%Y-%m-%d').month == month and datetime.strptime(employee['date'], '%Y-%m-%d').year == year]

    if search_results:
        # Calculate total salary
        total_salary = sum(employee['salary'] for employee in search_results)

        # Create the output folder if it doesn't exist
        if not os.path.exists("output"):
            os.makedirs("output")

        # Export data to text file
        txt_file_path = os.path.join("output", f"employee_data_{month:02d}_{year}.txt")
        with open(txt_file_path, "w") as file:
            # Header
            file.write(" شركه ابناء عرفات \n")
            file.write(" رواتب الموظفين \n")
            file.write(f" {month:02d}/{year} \n\n")

            # Employee data
            for employee in search_results:
                formatted_salary = f"{employee['salary']} شيكل"
                file.write(f"{employee['name'].ljust(10)}{formatted_salary.rjust(20)}\n")

            # Separate line
            file.write("\n*************************\n")

            # Total amount
            total_line = f"المجموع الكلي: {total_salary} شيكل"
            file.write(total_line.center(40) + "\n")

            # Separate line
            file.write("*************************\n")

        messagebox.showinfo("Export by Month", f"Employee data for {month:02d}/{year} exported to text file in 'output' folder successfully.")
    else:
        messagebox.showinfo("Export by Month", f"No employee data available for {month:02d}/{year}.")




employees = []

root = tk.Tk()
root.title("Employee Salary Management")

# Label and entry for adding new employees
name_label = tk.Label(root, text="Name:")
name_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)

name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=5)

salary_label = tk.Label(root, text="Salary:")
salary_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)

salary_entry = tk.Entry(root)
salary_entry.grid(row=1, column=1, padx=10, pady=5)

add_button = tk.Button(root, text="Add Employee", command=add_employee)
add_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

# Text widget to display employee data
text = tk.Listbox(root, width=60, height=15)
text.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W+tk.E+tk.N+tk.S)

# Button to delete selected employee
delete_button = tk.Button(root, text="Delete Employee", command=delete_employee)
delete_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

# Label and entry for updating salary
new_salary_label = tk.Label(root, text="New Salary:")
new_salary_label.grid(row=5, column=0, padx=10, pady=5, sticky=tk.E)

new_salary_entry = tk.Entry(root)
new_salary_entry.grid(row=5, column=1, padx=10, pady=5)

update_salary_button = tk.Button(root, text="Update Salary", command=update_salary)
update_salary_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

# Button to save and load data
save_button = tk.Button(root, text="Save Data", command=save_data)
save_button.grid(row=7, column=0, padx=10, pady=5)

load_button = tk.Button(root, text="Load Data", command=load_data)
load_button.grid(row=7, column=1, padx=10, pady=5)

# Buttons for sorting employees
sort_name_button = tk.Button(root, text="Sort by Name", command=lambda: sort_employees('name'))
sort_name_button.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

sort_salary_button = tk.Button(root, text="Sort by Salary", command=lambda: sort_employees('salary'))
sort_salary_button.grid(row=9, column=0, columnspan=2, padx=10, pady=5)

# Entry and button for searching employees
search_entry = tk.Entry(root)
search_entry.grid(row=10, column=0, padx=10, pady=5)

search_button = tk.Button(root, text="Search", command=search_employee)
search_button.grid(row=10, column=1, padx=10, pady=5)

# Button for data visualization
visualize_button = tk.Button(root, text="Visualize Data", command=visualize_data)
visualize_button.grid(row=11, column=0, columnspan=2, padx=10, pady=5)

# Button for exporting data to Excel and text file
export_excel_button = tk.Button(root, text="Export to Excel and Text", command=export_data)
export_excel_button.grid(row=12, column=0, columnspan=2, padx=10, pady=5)

# Button for exporting data to text file by specific date
export_by_date_button = tk.Button(root, text="Export by Date", command=export_data_by_date)
export_by_date_button.grid(row=13, column=0, columnspan=2, padx=10, pady=5)

# Button for exporting data to text file by specific month and year
export_by_month_button = tk.Button(root, text="Export by Month", command=export_data_by_month)
export_by_month_button.grid(row=14, column=0, columnspan=2, padx=10, pady=5)

root.update_idletasks()
root_width = root.winfo_width()
root_height = root.winfo_height()
x_offset = (root.winfo_screenwidth() - root_width) // 2
y_offset = (root.winfo_screenheight() - root_height) // 2
root.geometry(f"{root_width}x{root_height}+{x_offset}+{y_offset}")

root.mainloop()
