# cie3.py

def mark_attendance(employee_id, name, status):
    with open("attendance.txt", "a") as file:
        file.write(f"{employee_id} {name} {status}\n")
    return "ATTENDANCE MARKED"

def view_attendance():
    try:
        with open("attendance.txt", "r") as file:
            records = file.readlines()
            if not records:
                return "NO ATTENDANCE RECORDS FOUND."
            
            result = "ATTENDANCE RECORDS:\n"
            for record in records:
                result += record.strip() + "\n"
            return result.strip()
    except FileNotFoundError:
        return "NO ATTENDANCE RECORDS FOUND."

def main():
    open("attendance.txt", "w").close()
    #print("Enter the number of records to add:")
    n = int(input().strip())
    
    #print("Enter the employee id, name and status to add:")
    for _ in range(n):
        record = input().strip()
        parts = record.split(' ', 2)

        if len(parts) == 3:
            employee_id, name, status = parts
            result = mark_attendance(employee_id, name, status)
            print(result)
        else:
            print("Invalid input format")
    
    
    command = input().strip()
    if command == "VIEW":
        print(view_attendance())

if __name__ == "__main__":
    main()