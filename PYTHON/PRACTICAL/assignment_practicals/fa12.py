import pandas as pd

def analyze_employee_salaries(df):

    # 1. Read the dataset
    df = pd.read_csv("C:/Users/dipes/Desktop/JAVA/CODE/PYTHON_ASSIGNMENT/Salaries.csv", header=0, sep=',', quotechar='"')
    
    # 2. Find employee with highest and lowest total pay
    highest_pay = df.loc[df['TotalPayBenefits'].idxmax()]
    lowest_pay = df.loc[df['TotalPayBenefits'].idxmin()]
    
    print("Employee with Highest Total Pay:")
    print(highest_pay[['EmployeeName', 'JobTitle', 'TotalPayBenefits']])
    
    print("\nEmployee with Lowest Total Pay:")
    print(lowest_pay[['EmployeeName', 'JobTitle', 'TotalPayBenefits']])
    
    # 3. Average base salary for each job title
    df['BasePay'] = pd.to_numeric(df['BasePay'], errors='coerce')
    avg_by_title = df.groupby('JobTitle')['BasePay'].mean().reset_index()
    
    # 4. Job title with highest average base salary
    highest_avg_title = avg_by_title.loc[avg_by_title['BasePay'].idxmax()]
    print("\nJob Title with Highest Average Base Salary:")
    print(highest_avg_title)
    
    # 5. Total salary expenditure for each year
    yearly_expenditure = df.groupby('Year')['TotalPayBenefits'].sum().reset_index()
    print("\nTotal Salary Expenditure by Year:")
    print(yearly_expenditure)
    
    # 6. Top 5 highest-paid employees
    top_5 = df.nlargest(5, 'TotalPayBenefits')[['EmployeeName', 'JobTitle', 'TotalPayBenefits']]
    print("\nTop 5 Highest-Paid Employees:")
    print(top_5)
    
    # 7. Sort by overtime pay
    df['OvertimePay'] = pd.to_numeric(df['OvertimePay'], errors='coerce')
    sorted_by_overtime = df.sort_values('OvertimePay', ascending=False)[['EmployeeName', 'JobTitle', 'OvertimePay']].head(10)
    print("\nEmployees with Highest Overtime Pay:")
    print(sorted_by_overtime)
    
    # 8. Add Salary Bracket column
    df['SalaryBracket'] = pd.cut(df['BasePay'], 
                                 bins=[-float('inf'), 50000, 100000, float('inf')],
                                 labels=['Low', 'Medium', 'High'])
    
    # 9. Count employees in each bracket
    bracket_counts = df['SalaryBracket'].value_counts()
    print("\nEmployees in Each Salary Bracket:")
    print(bracket_counts)
    
    # 10. Most common job title
    most_common_job = df['JobTitle'].value_counts().idxmax()
    job_count = df['JobTitle'].value_counts().max()
    print(f"\nMost Common Job Title: {most_common_job} ({job_count} employees)")

# Replace with the actual file path
analyze_employee_salaries("Salaries.csv")