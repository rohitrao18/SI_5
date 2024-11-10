import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

# Database setup
conn = sqlite3.connect("employee_attendance.db")
cursor = conn.cursor()

# Create tables if not exist
cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id INTEGER,
                    date TEXT,
                    time_in TEXT,
                    time_out TEXT,
                    FOREIGN KEY (employee_id) REFERENCES employees(id)
                )''')

# Function to add an employee
def add_employee():
    name = entry_name.get()
    if name:
        cursor.execute("INSERT INTO employees (name) VALUES (?)", (name,))
        conn.commit()
        messagebox.showinfo("Success", f"Employee '{name}' added successfully.")
        entry_name.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter the employee name.")

# Function to mark attendance (check-in)
def check_in():
    employee_id = entry_employee_id.get()
    date = datetime.now().date().isoformat()
    time_in = datetime.now().time().strftime('%H:%M:%S')

    cursor.execute("INSERT INTO attendance (employee_id, date, time_in) VALUES (?, ?, ?)",
                   (employee_id, date, time_in))
    conn.commit()
    messagebox.showinfo("Check-in", f"Checked in for Employee ID {employee_id} at {time_in}.")

# Function to mark attendance (check-out)
def check_out():
    employee_id = entry_employee_id.get()
    date = datetime.now().date().isoformat()
    time_out = datetime.now().time().strftime('%H:%M:%S')

    cursor.execute("UPDATE attendance SET time_out = ? WHERE employee_id = ? AND date = ? AND time_out IS NULL",
                   (time_out, employee_id, date))
    conn.commit()
    messagebox.showinfo("Check-out", f"Checked out for Employee ID {employee_id} at {time_out}.")

# Function to view all employees
def view_employees():
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    display_text = "Employee List:\n" + "\n".join([f"ID: {emp[0]}, Name: {emp[1]}" for emp in employees])
    text_display.delete("1.0", tk.END)
    text_display.insert(tk.END, display_text)

# Function to view attendance logs
def view_attendance():
    cursor.execute('''SELECT e.id, e.name, a.date, a.time_in, a.time_out
                      FROM attendance a
                      JOIN employees e ON a.employee_id = e.id
                      ORDER BY a.date DESC, a.time_in DESC''')
    attendance_logs = cursor.fetchall()
    display_text = "Attendance Logs:\n" + "\n".join(
        [f"ID: {log[0]}, Name: {log[1]}, Date: {log[2]}, Time In: {log[3]}, Time Out: {log[4]}"
         for log in attendance_logs])
    text_display.delete("1.0", tk.END)
    text_display.insert(tk.END, display_text)

# Function to generate attendance report
def generate_report():
    cursor.execute('''SELECT e.id, e.name, COUNT(a.id) AS attendance_days
                      FROM employees e
                      LEFT JOIN attendance a ON e.id = a.employee_id
                      GROUP BY e.id''')
    report = cursor.fetchall()
    display_text = "Attendance Report:\n" + "\n".join(
        [f"Employee ID: {emp[0]}, Name: {emp[1]}, Attendance Days: {emp[2]}" for emp in report])
    text_display.delete("1.0", tk.END)
    text_display.insert(tk.END, display_text)

# Create main window
root = tk.Tk()
root.title("Employee Attendance System")

# Name entry for adding employee
frame_add_employee = tk.Frame(root)
frame_add_employee.pack(pady=10)
label_name = tk.Label(frame_add_employee, text="Employee Name:")
label_name.pack(side=tk.LEFT)
entry_name = tk.Entry(frame_add_employee)
entry_name.pack(side=tk.LEFT)
button_add_employee = tk.Button(frame_add_employee, text="Add Employee", command=add_employee)
button_add_employee.pack(side=tk.LEFT)

# Employee ID entry for check-in/check-out
frame_employee_id = tk.Frame(root)
frame_employee_id.pack(pady=10)
label_employee_id = tk.Label(frame_employee_id, text="Employee ID:")
label_employee_id.pack(side=tk.LEFT)
entry_employee_id = tk.Entry(frame_employee_id)
entry_employee_id.pack(side=tk.LEFT)

# Buttons for Check-in, Check-out, View Employees, View Attendance, and Generate Report
button_check_in = tk.Button(root, text="Check-in", command=check_in)
button_check_in.pack(pady=5)

button_check_out = tk.Button(root, text="Check-out", command=check_out)
button_check_out.pack(pady=5)

button_view_employees = tk.Button(root, text="View Employees", command=view_employees)
button_view_employees.pack(pady=5)

button_view_attendance = tk.Button(root, text="View Attendance Logs", command=view_attendance)
button_view_attendance.pack(pady=5)

button_generate_report = tk.Button(root, text="Generate Attendance Report", command=generate_report)
button_generate_report.pack(pady=5)

# Text box for displaying information
text_display = tk.Text(root, height=15, width=50)
text_display.pack(pady=10)

# Start the Tkinter main loop
root.mainloop()

# Close the connection when done
conn.close()
