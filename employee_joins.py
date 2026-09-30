import sqlite3

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

# Departments table
cursor.execute("""
    CREATE TABLE departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT NOT NULL
    )
""")

# Employees table
cursor.execute("""
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        salary REAL NOT NULL,
        department_id INTEGER,
        FOREIGN KEY (department_id) REFERENCES departments(id)
    )
""")

# Projects table
cursor.execute("""
    CREATE TABLE projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        employee_id INTEGER,
        FOREIGN KEY (employee_id) REFERENCES employees(id)
    )
""")


# --------------------------------------------------
# 2. INSERT SAMPLE DATA
# --------------------------------------------------

# Departments
departments = [
    ("Engineering", "St. Louis"),
    ("Human Resources", "Chicago"),
    ("Marketing", "Kansas City"),
    ("Finance", "Dallas")
]

cursor.executemany("""
    INSERT INTO departments (name, location)
    VALUES (?, ?)
""", departments)


# Employees
employees = [
    ("Alice Johnson", "Software Engineer", 85000, 1),
    ("Bob Smith", "Data Analyst", 72000, 1),
    ("Charlie Brown", "Senior Developer", 95000, 1),
    ("Diana Williams", "HR Manager", 78000, 2),
    ("Ethan Davis", "HR Specialist", 62000, 2),
    ("Frank Miller", "Marketing Manager", 81000, 3),
    ("Grace Wilson", "Marketing Specialist", 65000, 3),
    ("Henry Moore", "Financial Analyst", 74000, 4)
]

cursor.executemany("""
    INSERT INTO employees (name, role, salary, department_id)
    VALUES (?, ?, ?, ?)
""", employees)


# Projects
projects = [
    ("Website Redesign", 1),
    ("Data Migration", 3),
    ("Employee Training Program", 4),
    ("Marketing Campaign", 6)
]

cursor.executemany("""
    INSERT INTO projects (title, employee_id)
    VALUES (?, ?)
""", projects)


connection.commit()


# --------------------------------------------------
# QUERY 1
# List all employees with their department name
# INNER JOIN
# --------------------------------------------------

print("\n--- Query 1: Employees and Departments ---")

cursor.execute("""
    SELECT
        employees.name,
        employees.role,
        departments.name AS department
    FROM employees
    INNER JOIN departments
        ON employees.department_id = departments.id
    ORDER BY employees.id
""")

for row in cursor.fetchall():
    print(row)

# --------------------------------------------------
# QUERY 2
# List all departments, even those with no employees
# LEFT JOIN
# --------------------------------------------------

print("\n--- Query 2: All Departments and Employees ---")

cursor.execute("""
    SELECT
        departments.name AS department,
        employees.name AS employee
    FROM departments
    LEFT JOIN employees
        ON departments.id = employees.department_id
    ORDER BY departments.id, employees.name
""")

for row in cursor.fetchall():
    print(row)


# --------------------------------------------------
# QUERY 3
# List all employees and projects they lead
# Include employees who don't lead a project
# LEFT JOIN
# --------------------------------------------------

print("\n--- Query 3: Employees and Projects ---")

cursor.execute("""
    SELECT
        employees.name AS employee,
        projects.title AS project
    FROM employees
    LEFT JOIN projects
        ON employees.id = projects.employee_id
    ORDER BY employees.id
""")

for row in cursor.fetchall():
    print(row)


# --------------------------------------------------
# QUERY 4
# Find employees who don't lead any project
# LEFT JOIN + IS NULL
# --------------------------------------------------

print("\n--- Query 4: Employees Without Projects ---")

cursor.execute("""
    SELECT
        employees.name
    FROM employees
    LEFT JOIN projects
        ON employees.id = projects.employee_id
    WHERE projects.employee_id IS NULL
    ORDER BY employees.id
""")

for row in cursor.fetchall():
    print(row)


# --------------------------------------------------
# QUERY 5
# List all projects with project lead and department
# JOIN THREE TABLES
# --------------------------------------------------

print("\n--- Query 5: Projects, Leads, and Departments ---")

cursor.execute("""
    SELECT
        projects.title AS project,
        employees.name AS project_lead,
        departments.name AS department
    FROM projects
    INNER JOIN employees
        ON projects.employee_id = employees.id
    INNER JOIN departments
        ON employees.department_id = departments.id
    ORDER BY projects.id
""")

for row in cursor.fetchall():
    print(row)


# Close the database connection
connection.close()