import re

def validate_password(password):
    if 6 <= len(password) <= 12:
        if re.search("[a-z]", password) and \
           re.search("[0-9]", password) and \
           re.search("[A-Z]", password) and \
           re.search("[$#@]", password):
            return True
    return False

passwords = input("Enter passwords separated by commas: ").split(",")
valid_passwords = [p.strip() for p in passwords if validate_password(p.strip())]
print(",".join(valid_passwords))