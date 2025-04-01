import sqlite3
import pandas as pd
import numpy as np

def create_database():
    # Create a connection to SQLite database
    conn = sqlite3.connect('employee_salaries.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        EmployeeName TEXT,
        JobTitle TEXT,
        BasePay REAL,
        OvertimePay REAL,
        OtherPay REAL,
        Benefits REAL,
        TotalPay REAL,
        TotalPayBenefits REAL,
        Year INTEGER,
        Notes TEXT,
        Agency TEXT,
        Status TEXT
    )
    ''')

    
    df = pd.read_csv("C:/Users/dipes/Desktop/JAVA/CODE/PYTHON_ASSIGNMENT/Salaries.csv")
    
    
    numeric_columns = ['BasePay', 'OvertimePay', 'OtherPay', 'Benefits', 'TotalPay', 'TotalPayBenefits']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Insert data from CSV into the database
    df.to_sql('employees', conn, if_exists='replace', index=False)
    
    print("Database and table created successfully!")
    return conn

def analyze_employee_data(conn):
    cursor = conn.cursor()
    
    # 3. Find the highest-paid employee (including benefits)
    cursor.execute('''
    SELECT EmployeeName, JobTitle, TotalPayBenefits
    FROM employees
    WHERE TotalPayBenefits IS NOT NULL
    ORDER BY TotalPayBenefits DESC
    LIMIT 1
    ''')
    highest_paid = cursor.fetchone()
    print("\nHighest-paid employee:")
    print(f"Name: {highest_paid[0]}")
    print(f"Job Title: {highest_paid[1]}")
    print(f"Total Pay with Benefits: ${highest_paid[2]:,.2f}")

    # 4. Find the total salary expenditure for each year
    cursor.execute('''
    SELECT Year, SUM(TotalPayBenefits) as total_expenditure
    FROM employees
    WHERE TotalPayBenefits IS NOT NULL
    GROUP BY Year
    ORDER BY Year
    ''')
    yearly_expenditure = cursor.fetchall()
    print("\nTotal salary expenditure by year:")
    for year, total in yearly_expenditure:
        print(f"Year {year}: ${total:,.2f}")

    # 5. Retrieve employees with overtime pay > $50,000
    cursor.execute('''
    SELECT EmployeeName, JobTitle, OvertimePay
    FROM employees
    WHERE OvertimePay > 50000 AND OvertimePay IS NOT NULL
    ORDER BY OvertimePay DESC
    LIMIT 5
    ''')
    high_overtime = cursor.fetchall()
    print("\nTop 5 employees with overtime pay > $50,000:")
    for emp in high_overtime:
        print(f"Name: {emp[0]}")
        print(f"Job Title: {emp[1]}")
        print(f"Overtime Pay: ${emp[2]:,.2f}")

    # 6. Find the most common job title
    cursor.execute('''
    SELECT JobTitle, COUNT(*) as count
    FROM employees
    GROUP BY JobTitle
    ORDER BY count DESC
    LIMIT 1
    ''')
    most_common = cursor.fetchone()
    print(f"\nMost common job title: {most_common[0]} ({most_common[1]} employees)")

    # 7. Sort employees by BasePay in descending order
    cursor.execute('''
    SELECT EmployeeName, JobTitle, BasePay
    FROM employees
    WHERE BasePay IS NOT NULL
    ORDER BY BasePay DESC
    LIMIT 5
    ''')
    top_base_pay = cursor.fetchall()
    print("\nTop 5 employees by Base Pay:")
    for emp in top_base_pay:
        print(f"Name: {emp[0]}")
        print(f"Job Title: {emp[1]}")
        print(f"Base Pay: ${emp[2]:,.2f}")

    # 8. Update BasePay for John Doe
    cursor.execute('''
    UPDATE employees
    SET BasePay = 120000
    WHERE EmployeeName = 'John Doe'
    ''')
    print("\nUpdated BasePay for John Doe to $120,000")

    # 9. Delete employees with TotalPayBenefits < 40,000
    cursor.execute('''
    DELETE FROM employees
    WHERE TotalPayBenefits < 40000 AND TotalPayBenefits IS NOT NULL
    ''')
    deleted_count = cursor.rowcount
    print(f"\nDeleted {deleted_count} employees with TotalPayBenefits < $40,000")

    # Commit the changes
    conn.commit()

def main():
    # Create database and table
    conn = create_database()
    
    # Analyze employee data
    analyze_employee_data(conn)
    
    # Close the connection
    conn.close()

if __name__ == "__main__":
    main()
