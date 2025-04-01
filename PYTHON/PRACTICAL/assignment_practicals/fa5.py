# Global variable for university information
university_name = "Example University"

class User:
    # Class variable for predefined roles and privileges
    role_privileges = {
        "student": ["view_grades", "submit_assignments", "access_library"],
        "teacher": ["view_grades", "modify_grades", "create_assignments", "access_library"],
        "admin": ["view_all_data", "modify_user_roles", "access_system_settings", "access_library"]
    }
    
    def __init__(self, name, user_id, role):
        # Instance variables for individual user details
        self.name = name
        self.user_id = user_id
        self.role = role
    
    def get_privileges(self):
        """Retrieve and display user's privileges based on their role"""
        if self.role in User.role_privileges:
            print(f"\nUser: {self.name} (ID: {self.user_id})")
            print(f"Role: {self.role} at {university_name}")
            print("Privileges:")
            for privilege in User.role_privileges[self.role]:
                print(f"- {privilege}")
            return User.role_privileges[self.role]
        else:
            print(f"Role '{self.role}' not defined in the system.")
            return []

# Example usage
student1 = User("John Smith", "ST12345", "student")
teacher1 = User("Dr.John", "TC54321", "teacher")
admin1 = User("Admin User", "AD99999", "admin")

student1.get_privileges()
teacher1.get_privileges()
admin1.get_privileges()