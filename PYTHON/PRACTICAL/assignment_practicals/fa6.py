def atm_transaction():
    correct_pin = "1234"
    attempts = 0
    max_attempts = 3
    
    print("Welcome to the ATM System")
    
    while attempts < max_attempts:
        pin = input("Enter your PIN: ")
        
        if pin == correct_pin:
            print("PIN correct! Transaction Successful.")
            break
        else:
            attempts += 1
            remaining = max_attempts - attempts
            if remaining > 0:
                print(f"Incorrect PIN. {remaining} attempt(s) remaining.")
            continue
    else:
        print("Card Blocked. Too many incorrect attempts.")

atm_transaction()