class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
    
    def get_employee_details(self):
        return f"Name: {self.name}, Salary: {self.salary}$"

class Customer:
    def __init__(self, customer_id, account_balance):
        self.customer_id = customer_id
        self.account_balance = account_balance
    
    def get_customer_details(self):
        return f"Customer ID: {self.customer_id}, Account Balance: {self.account_balance}$"

class EmployeeCustomer(Employee, Customer):
    def __init__(self, name, salary, customer_id, account_balance):
        Employee.__init__(self, name, salary)
        Customer.__init__(self, customer_id, account_balance)
    
    def show_details(self):
        print("Employee-Customer Details:")
        print(self.get_employee_details())
        print(self.get_customer_details())

ec1 = EmployeeCustomer("Will Smith", 75000, "CUS123", 15000)
ec1.show_details()