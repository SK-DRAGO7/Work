import tkinter as tk
from tkinter import messagebox
import random
import string
import csv
import os

# Define constants
PASSWORD_FILE = "password.csv"

class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager App")
        
        # Create main menu
        self.main_menu = tk.Frame(self.root)
        self.main_menu.pack()
        
        self.label = tk.Label(self.main_menu, text="Password Manager App", font=('Helvetica', 18, 'bold'))
        self.label.pack(pady=20)
        
        self.create_btn = tk.Button(self.main_menu, text="Create Password", command=self.create_password_screen, width=25)
        self.create_btn.pack(pady=5)
        
        self.check_btn = tk.Button(self.main_menu, text="Check Password", command=self.check_password_screen, width=25)
        self.check_btn.pack(pady=5)
        
        self.edit_btn = tk.Button(self.main_menu, text="Edit Password", command=self.edit_password_screen, width=25)
        self.edit_btn.pack(pady=5)
        
        self.del_btn = tk.Button(self.main_menu, text="Delete Password", command=self.delete_password_screen, width=25)
        self.del_btn.pack(pady=5)
        
        self.exit_btn = tk.Button(self.main_menu, text="Exit", command=self.exit_app, width=25)
        self.exit_btn.pack(pady=20)

    def generate_password(self, length, include_uppercase=True, include_digits=True, include_special_chars=True):
        """Generate a random password with customizable options."""
        char_sets = [
            string.ascii_lowercase,
            string.ascii_uppercase if include_uppercase else "",
            string.digits if include_digits else "",
            string.punctuation if include_special_chars else "",
        ]
        # Filter out empty strings from char_sets
        char_sets = [chars for chars in char_sets if chars]
        
        # Ensure at least one character type is selected
        if not char_sets:
            raise ValueError("At least one character set must be selected.")
        
        password = []
        
        # Sample one character from each selected set
        for char_set in char_sets:
            password.append(random.choice(char_set))
        
        # Fill remaining password length with random characters from all selected sets
        password.extend(random.choice("".join(char_sets)) for _ in range(length - len(password)))
        
        # Shuffle the password to ensure randomness
        random.shuffle(password)
        
        # Join password list into string and return
        return "".join(password)

    def create_password_screen(self):
        self.clear_screen()
        self.label = tk.Label(self.root, text="Create Password", font=('Helvetica', 18, 'bold'))
        self.label.pack(pady=20)
        
        self.aim_label = tk.Label(self.root, text="Program/Website:")
        self.aim_label.pack(pady=5)
        self.aim_entry = tk.Entry(self.root, width=50)
        self.aim_entry.pack(pady=5)

        # New UI elements for customization
        self.length_label = tk.Label(self.root, text="Password Length:")
        self.length_label.pack(pady=5)
        self.length_entry = tk.Entry(self.root, width=10)
        self.length_entry.pack(pady=5)

        self.uppercase_var = tk.IntVar()
        self.uppercase_check = tk.Checkbutton(self.root, text="Include Uppercase Letters", variable=self.uppercase_var)
        self.uppercase_check.pack(pady=5)

        self.digits_var = tk.IntVar()
        self.digits_check = tk.Checkbutton(self.root, text="Include Digits", variable=self.digits_var)
        self.digits_check.pack(pady=5)

        self.special_var = tk.IntVar()
        self.special_check = tk.Checkbutton(self.root, text="Include Special Characters", variable=self.special_var)
        self.special_check.pack(pady=5)
        
        self.create_btn = tk.Button(self.root, text="Generate Password", command=self.create_password)
        self.create_btn.pack(pady=10)
        
        self.back_btn = tk.Button(self.root, text="Back to Main Menu", command=self.back_to_main)
        self.back_btn.pack(pady=10)

    def create_password(self):
        aim = self.aim_entry.get().strip()
        length = int(self.length_entry.get().strip())
        include_uppercase = bool(self.uppercase_var.get())
        include_digits = bool(self.digits_var.get())
        include_special_chars = bool(self.special_var.get())

        try:
            # Generate password with specified options
            password = self.generate_password(length, include_uppercase, include_digits, include_special_chars)
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return

        if aim:
            # Check if the password file exists and create it if not
            if not os.path.isfile(PASSWORD_FILE):
                with open(PASSWORD_FILE, "w", newline="") as csvfile:
                    fieldnames = ["aim", "password"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
            
            # Read the existing aims from the CSV file
            existing_aims = []
            with open(PASSWORD_FILE, "r") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    existing_aims.append(row["aim"])
            
            # Check if the aim is already used and reject it if so
            if aim in existing_aims:
                messagebox.showerror("Error", f"'{aim}' is unavailable. Please use a different aim.")
            else:
                # Append the aim and password to the CSV file
                with open(PASSWORD_FILE, "a", newline="") as csvfile:
                    fieldnames = ["aim", "password"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writerow({"aim": aim, "password": password})
                
                # Display a success message and the new password
                messagebox.showinfo("Success", f"Password created successfully.\n\n{aim} password is: {password}")
        else:
            messagebox.showerror("Error", "Aim unspecified or empty. Please specify an 'aim' value.")

    def check_password_screen(self):
        self.clear_screen()
        self.label = tk.Label(self.root, text="Check Password", font=('Helvetica', 18, 'bold'))
        self.label.pack(pady=20)
        
        self.aim_label = tk.Label(self.root, text="Program/Website:")
        self.aim_label.pack(pady=5)
        self.aim_entry = tk.Entry(self.root, width=50)
        self.aim_entry.pack(pady=5)
        
        self.check_btn = tk.Button(self.root, text="Check Password", command=self.check_password)
        self.check_btn.pack(pady=10)
        
        self.back_btn = tk.Button(self.root, text="Back to Main Menu", command=self.back_to_main)
        self.back_btn.pack(pady=10)

    def check_password(self):
        aim = self.aim_entry.get().strip()
        if aim:
            if not os.path.isfile(PASSWORD_FILE):
                messagebox.showerror("Error", "Password file does not exist. Please create a password first.")
                return

            with open(PASSWORD_FILE, "r") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if aim == row["aim"]:
                        messagebox.showinfo("Password Found", f"Password for '{aim}' is: {row['password']}")
                        return
            messagebox.showerror("Error", "No password found for the specified aim.")
        else:
            messagebox.showerror("Error", "Aim unspecified or empty. Please specify an 'aim' value.")
    
    def edit_password_screen(self):
        self.clear_screen()
        self.label = tk.Label(self.root, text="Edit Password", font=('Helvetica', 18, 'bold'))
        self.label.pack(pady=20)
        
        self.aim_label = tk.Label(self.root, text="Program/Website:")
        self.aim_label.pack(pady=5)
        self.aim_entry = tk.Entry(self.root, width=50)
        self.aim_entry.pack(pady=5)
        
        self.new_pass_label = tk.Label(self.root, text="New Password:")
        self.new_pass_label.pack(pady=5)
        self.new_pass_entry = tk.Entry(self.root, width=50)
        self.new_pass_entry.pack(pady=5)
        
        self.confirm_pass_label = tk.Label(self.root, text="Confirm New Password:")
        self.confirm_pass_label.pack(pady=5)
        self.confirm_pass_entry = tk.Entry(self.root, width=50)
        self.confirm_pass_entry.pack(pady=5)
        
        self.edit_btn = tk.Button(self.root, text="Edit Password", command=self.edit_password)
        self.edit_btn.pack(pady=10)
        
        self.back_btn = tk.Button(self.root, text="Back to Main Menu", command=self.back_to_main)
        self.back_btn.pack(pady=10)

    def edit_password(self):
        aim = self.aim_entry.get().strip()
        new_password = self.new_pass_entry.get().strip()
        confirm_password = self.confirm_pass_entry.get().strip()

        if aim and new_password and confirm_password:
            if new_password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match. Please try again.")
                return

            data = []
            found = False
            with open(PASSWORD_FILE, "r") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    data.append(row)
                    if aim == row["aim"]:
                        found = True

            if found:
                for row in data:
                    if row["aim"] == aim:
                        row["password"] = new_password

                with open(PASSWORD_FILE, "w", newline="") as csvfile:
                    fieldnames = ["aim", "password"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(data)

                messagebox.showinfo("Success", f"Password updated successfully.\n\nNew password for '{aim}' is: {new_password}")
            else:
                messagebox.showerror("Error", "No password found for the specified aim.")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")
    
    def delete_password_screen(self):
        self.clear_screen()
        self.label = tk.Label(self.root, text="Delete Password", font=('Helvetica', 18, 'bold'))
        self.label.pack(pady=20)
        
        self.aim_label = tk.Label(self.root, text="Program/Website:")
        self.aim_label.pack(pady=5)
        self.aim_entry = tk.Entry(self.root, width=50)
        self.aim_entry.pack(pady=5)
        
        self.del_btn = tk.Button(self.root, text="Delete Password", command=self.del_password)
        self.del_btn.pack(pady=10)
        
        self.back_btn = tk.Button(self.root, text="Back to Main Menu", command=self.back_to_main)
        self.back_btn.pack(pady=10)

    def del_password(self):
        aim = self.aim_entry.get().strip()
        if aim:
            data = []
            found = False
            with open(PASSWORD_FILE, "r") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if aim == row["aim"]:
                        found = True
                    else:
                        data.append(row)

            if found:
                with open(PASSWORD_FILE, "w", newline="") as csvfile:
                    fieldnames = ["aim", "password"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(data)

                messagebox.showinfo("Success", f"Password deleted successfully for aim: {aim}")
            else:
                messagebox.showerror("Error", "No password found for the specified aim.")
        else:
            messagebox.showerror("Error", "Aim unspecified or empty. Please specify an 'aim' value.")
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def back_to_main(self):
        self.clear_screen()
        self.__init__(self.root)
    
    def exit_app(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()
