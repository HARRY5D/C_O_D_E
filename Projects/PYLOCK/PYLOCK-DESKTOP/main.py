
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class MainWindow:
    def setup_passwords_tab(self):
        # ...existing code...
        
        # Password actions frame
        password_actions_frame = ttk.Frame(self.passwords_tab)
        password_actions_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add button
        add_button = ttk.Button(password_actions_frame, text="Add", command=self.add_password)
        add_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Edit button
        edit_button = ttk.Button(password_actions_frame, text="Edit", command=self.edit_password)
        edit_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Delete button
        delete_button = ttk.Button(password_actions_frame, text="Delete", command=self.delete_password)
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # ...existing code...
    
    def edit_password(self):
        # Get the selected item from password treeview
        selected_item = self.passwords_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a password entry to edit.")
            return
            
        # Get the password ID and current data from the item
        password_id = self.passwords_tree.item(selected_item, "values")[0]
        website = self.passwords_tree.item(selected_item, "values")[1]
        username = self.passwords_tree.item(selected_item, "values")[2]
        
        # Get encrypted password from database
        password_data = None
        for pwd in self.passwords:
            if str(pwd['id']) == str(password_id):
                password_data = pwd
                break
        
        if not password_data:
            messagebox.showerror("Error", "Could not retrieve password data.")
            return
            
        # Create edit window
        edit_window = tk.Toplevel(self.master)
        edit_window.title("Edit Password")
        edit_window.geometry("400x300")
        edit_window.resizable(False, False)
        
        # Set window to be modal
        edit_window.transient(self.master)
        edit_window.grab_set()
        
        # Add fields
        ttk.Label(edit_window, text="Website:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        website_entry = ttk.Entry(edit_window, width=30)
        website_entry.grid(row=0, column=1, padx=10, pady=10)
        website_entry.insert(0, website)
        
        ttk.Label(edit_window, text="Username:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        username_entry = ttk.Entry(edit_window, width=30)
        username_entry.grid(row=1, column=1, padx=10, pady=10)
        username_entry.insert(0, username)
        
        ttk.Label(edit_window, text="Password:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        password_entry = ttk.Entry(edit_window, width=30, show="•")
        password_entry.grid(row=2, column=1, padx=10, pady=10)
        
        # Decrypt the password for editing
        decrypted_password = self.encryption_manager.decrypt(password_data['password'].encode())
        password_entry.insert(0, decrypted_password)
        
        # Save and cancel buttons
        button_frame = ttk.Frame(edit_window)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        def save_edited_password():
            # Get the values from entry fields
            website = website_entry.get().strip()
            username = username_entry.get().strip()
            password = password_entry.get()
            
            # Validate inputs
            if not website or not username or not password:
                messagebox.showwarning("Validation Error", "All fields are required!")
                return
                
            # Encrypt the password
            encrypted_password = self.encryption_manager.encrypt(password).decode()
            
            # Update the database
            success = self.db_manager.update_password(
                password_id, 
                self.user['id'], 
                website, 
                username, 
                encrypted_password
            )
            
            if success:
                messagebox.showinfo("Success", "Password updated successfully!")
                edit_window.destroy()
                # Refresh the password list
                self.load_passwords()
            else:
                messagebox.showerror("Error", "Failed to update password.")
        
        save_btn = ttk.Button(button_frame, text="Save", command=save_edited_password)
        save_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=edit_window.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=10)
        
        # Center the window
        edit_window.update_idletasks()
        width = edit_window.winfo_width()
        height = edit_window.winfo_height()
        x = (edit_window.winfo_screenwidth() // 2) - (width // 2)
        y = (edit_window.winfo_screenheight() // 2) - (height // 2)
        edit_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Focus on the first field
        website_entry.focus_set()
    
    # ...existing code...
    def delete_password(self):
        # Get the selected item from password treeview
        selected_item = self.passwords_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a password entry to delete.")
            return
        
        # Get the password ID from the item
        password_id = self.passwords_tree.item(selected_item, "values")[0]
        
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this password?")
        if confirm:
            success = self.db_manager.delete_password(password_id)
            if success:
                messagebox.showinfo("Success", "Password deleted successfully!")
                self.load_passwords()
            else:
                messagebox.showerror("Error", "Failed to delete password.")

