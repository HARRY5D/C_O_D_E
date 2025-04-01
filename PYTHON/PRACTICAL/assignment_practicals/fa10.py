class BankAccount:
    def __init__(self, account_holder, initial_balance=0):
        self.account_holder = account_holder
        # Private attribute
        self._balance = 0  
        
        # Validation of  initial balance
        if initial_balance >= 0:
            self._balance = initial_balance
        else:
            raise ValueError("Initial balance cannot be negative")
    
    @property
    def balance(self):
        """Getter for balance"""
        return self._balance
    
    @balance.setter
    def balance(self, value):
        """Setter for balance with validation"""
        if value < 0:
            raise ValueError("Cannot set negative balance")
        self._balance = value
    
    def deposit(self, amount):
        """Add money to account"""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        return f"Deposited ${amount}. New balance: ${self.balance}"
    
    def withdraw(self, amount):
        """Remove money from account"""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        return f"Withdrew ${amount}. New balance: ${self.balance}"

# Example usage
account = BankAccount("HARRY", 1000)
print(f"Account created for {account.account_holder} with balance ${account.balance}")

print(account.deposit(500))
print(account.withdraw(200))

try:
    #raises error
    account.balance = -100  
except ValueError as e:
    print(f"Error: {e}")

try:
    account.withdraw(2000) #raises error
except ValueError as e:
    print(f"Error: {e}")