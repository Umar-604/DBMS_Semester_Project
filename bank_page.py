from tkinter import *
from tkinter import messagebox
from tkinter import ttk  # Import ttk module for themed widgets
from database import *

class BankGUI:
    def __init__(self, root):
        self.bank_options_window = root
        
        # Create the donation options window
        self.bank_options_window.title("Bank Options")
        self.bank_options_window.geometry("500x500")

        # New Donor button
        new_bank_button = Button(self.bank_options_window, text="New Bank", command=lambda: self.on_option_click("New Bank"))
        new_bank_button.pack(pady=10)

        # Existing Donor button
        view_bank_button = Button(self.bank_options_window, text="View Bank", command=lambda: self.on_option_click("View Bank"))
        view_bank_button.pack(pady=10)

        self.services_provided = ["Blood Storage", "Blood Donation", "Blood Testing"]

    def on_option_click(self, option):
        if option == "New Bank":
            self.new_bank_window()
        elif option == "View Bank":
            self.view_bank_window()

    def new_bank_window(self):
        new_bank_window = Toplevel()
        new_bank_window.title("New Bank Information")
        new_bank_window.geometry("400x400")

        # Rest of the code for the new donor window...
        def submit_bank_info(blood_bank_id_entry, name_entry, location_entry, contact_entry, services_provided_combobox, operating_hours_entry):
            blood_bank_id = blood_bank_id_entry.get()
            name = name_entry.get()
            location = location_entry.get()
            contact = contact_entry.get()
            services_provided = services_provided_combobox.get()
            operating_hours = operating_hours_entry.get()

            insert_blood_bank(blood_bank_id, name, location, contact, services_provided, operating_hours)
            messagebox.showinfo("Blood Bank Information", "Data inserted successfully")

        # Blood Bank ID
        blood_bank_id_label = Label(new_bank_window, text="Blood Bank ID:")
        blood_bank_id_label.grid(row=0, column=0, padx=10, pady=10)
        blood_bank_id_entry = Entry(new_bank_window)
        blood_bank_id_entry.grid(row=0, column=1, padx=10, pady=10)

        # Name
        name_label = Label(new_bank_window, text="Name:")
        name_label.grid(row=1, column=0, padx=10, pady=10)
        name_entry = Entry(new_bank_window)
        name_entry.grid(row=1, column=1, padx=10, pady=10)

        location_label = Label(new_bank_window, text="Location:")
        location_label.grid(row=2, column=0, padx=10, pady=10)
        location_entry = Entry(new_bank_window)
        location_entry.grid(row=2, column=1, padx=10, pady=10)

        # Contact
        contact_label = Label(new_bank_window, text="Contact:")
        contact_label.grid(row=3, column=0, padx=10, pady=10)
        contact_entry = Entry(new_bank_window)
        contact_entry.grid(row=3, column=1, padx=10, pady=10)

        # Services provided
        services_provided_label = Label(new_bank_window, text="Services Type:")
        services_provided_label.grid(row=4, column=0, padx=10, pady=10)
        services_provided_combobox = ttk.Combobox(new_bank_window, values=self.services_provided, state="readonly")  # Create combobox
        services_provided_combobox.current(0)  # Set default value
        services_provided_combobox.grid(row=4, column=1, padx=10, pady=10)

        # Operating hours
        operating_hours_label = Label(new_bank_window, text="Operating hours:")
        operating_hours_label.grid(row=5, column=0, padx=10, pady=10)
        operating_hours_entry = Entry(new_bank_window)
        operating_hours_entry.grid(row=5, column=1, padx=10, pady=10)

        # Submit Button
        submit_button = Button(new_bank_window, text="Submit", command=lambda: submit_bank_info(blood_bank_id_entry, name_entry, location_entry, contact_entry, services_provided_combobox, operating_hours_entry))
        submit_button.grid(row=6, columnspan=2, padx=10, pady=10)

    def view_bank_window(self):
        view_bank_window = Toplevel()
        view_bank_window.title("Banks Information")
        view_bank_window.geometry("500x500")

        # Rest of the code for the existing donor window...
        bank_records_label = Label(view_bank_window, text="", wraplength=280, justify=LEFT)
        bank_records_label.grid(row=5, columnspan=2, padx=10, pady=10)

        # Function to handle the submission of donor ID
        def submit_bank_id():
            blood_bank_id = blood_bank_id_entry.get()
            bank_records = view_bank(blood_bank_id)
            if bank_records:
                # Create Treeview widget
                tree = ttk.Treeview(view_bank_window)
                
                # Define columns
                tree["columns"] = ("Blood Bank ID", "Name", "Location", "Contact Information", "Services Provided", "Operating Hours")
                
                # Column headings
                for column in tree["columns"]:
                    tree.heading(column, text=column)
                
                # Insert data
                for record in bank_records:
                    tree.insert("", "end", values=record)
                
                # Display Treeview
                tree.grid(row=6, columnspan=2, padx=10, pady=10, sticky="nsew")
                
                # Adjust column spacing
                for col in tree["columns"]:
                    tree.column(col, width=120, anchor="center")  # Adjust width as needed
                
                # Add scrollbar
                scrollbar = ttk.Scrollbar(view_bank_window, orient="vertical", command=tree.yview)
                scrollbar.grid(row=6, column=2, sticky="ns")
                tree.configure(yscrollcommand=scrollbar.set)
            else:
                messagebox.showinfo("No Records", "No records found for Blood Bank ID: " + blood_bank_id)

        def delete_selected_bank():
            blood_bank_id = b_search_entry.get()  # Get the donor ID from the entry
            bank_records = view_bank(blood_bank_id)

            if bank_records:
                delete_bank(blood_bank_id)
                messagebox.showinfo("Deletion", "The record is deleted ")
            else:  
                messagebox.showinfo("No Records", "No records found for Blood Bank ID: " + blood_bank_id)

        # Donor ID
        blood_bank_id_label = Label(view_bank_window, text="Blood Bank ID:")
        blood_bank_id_label.grid(row=0, column=0, padx=10, pady=10)
        blood_bank_id_entry = Entry(view_bank_window)
        blood_bank_id_entry.grid(row=0, column=1, padx=10, pady=10)

        # Submit Button
        submit_button = Button(view_bank_window, text="Submit", command=submit_bank_id)
        submit_button.grid(row=1, columnspan=2, padx=10, pady=10)

        b_search_label = Label(view_bank_window, text="Enter Blood Bank ID:")
        b_search_label.grid(row=2, column=0, padx=10, pady=10)
        b_search_entry = Entry(view_bank_window)
        b_search_entry.grid(row=2, column=1, padx=10, pady=10)
        delete_button = Button(view_bank_window, text="Delete", command=delete_selected_bank)
        delete_button.grid(row=3, columnspan=2, padx=10, pady=10)


        # Adjust spacing for input bar labels
        view_bank_window.grid_rowconfigure(4, minsize=20)

        def view_all_records_bank():
            blood_bank_id = blood_bank_id_entry.get()
            bank_records = view_all_banks()
            if bank_records:
                # Create Treeview widget
                tree = ttk.Treeview(view_bank_window)
                
                # Define columns
                tree["columns"] = ("Blood Bank ID", "Name", "Location", "Contact Information", "Services Provided", "Operating Hours")
                
                # Column headings
                for column in tree["columns"]:
                    tree.heading(column, text=column)
                
                # Insert data
                for record in bank_records:
                    tree.insert("", "end", values=record)
                
                # Display Treeview
                tree.grid(row=6, columnspan=2, padx=10, pady=10, sticky="nsew")
                
                # Adjust column spacing
                for col in tree["columns"]:
                    tree.column(col, width=120, anchor="center")  # Adjust width as needed
                
                # Add scrollbar
                scrollbar = ttk.Scrollbar(view_bank_window, orient="vertical", command=tree.yview)
                scrollbar.grid(row=6, column=2, sticky="ns")
                tree.configure(yscrollcommand=scrollbar.set)
            else:
                messagebox.showinfo("No Records", "No records found for Blood Bank ID: " + blood_bank_id)

        view_all_button = Button(view_bank_window, text="View All Banks", command=view_all_records_bank)
        view_all_button.grid(row=4, columnspan=2, padx=10, pady=10)

        

def open_bank_gui():
    root = Tk()
    bank_gui = BankGUI(root)
    root.mainloop()

if __name__ == "__main__":
    open_bank_gui()
