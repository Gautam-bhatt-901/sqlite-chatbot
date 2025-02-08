import sqlite3

#  Connect to SQLite database (creates file if not exists)
conn = sqlite3.connect("company.db")
cursor = conn.cursor()

#  Create Employees table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Employees (
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Department TEXT NOT NULL,
    Salary INTEGER NOT NULL,
    Hire_Date TEXT NOT NULL
)
""")

#  Create Departments table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Departments (
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Manager TEXT NOT NULL
)
""")

#  Insert sample data into Employees table
employees_data = [
    (1, "Alice", "Sales", 50000, "2021-01-15"),
    (2, "Bob", "Engineering", 70000, "2020-06-10"),
    (3, "Charlie", "Marketing", 60000, "2022-03-20"),
    (4, "Roman", "HR", 55000, "2020-01-10"),
    (5, "Kate", "Engineering", 60000, "2023-02-11")
]

cursor.executemany("INSERT INTO Employees VALUES (?, ?, ?, ?, ?)", employees_data)

#  Insert sample data into Departments table
departments_data = [
    (1, "Sales", "Alice"),
    (2, "Engineering", "Bob"),
    (3, "Marketing", "Charlie"),
    (4, "HR", "Roman")
]

cursor.executemany("INSERT INTO Departments VALUES (?, ?, ?)", departments_data)

#  Commit changes and close connection
conn.commit()
conn.close()

print("Database and tables created successfully!")