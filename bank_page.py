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
        new_bank_button = Button(self.bank_options_window, text="New Bank", command=lambda: self.on_option_click("New Donor"))
        new_bank_button.pack(pady=10)

        # Existing Donor button
        view_bank_button = Button(self.bank_options_window, text="View Bank", command=lambda: self.on_option_click("Existing Donor"))
        view_bank_button.pack(pady=10)

    
    def on_option_click(self, option):
        if option == "New Bank":
            self.new_bank_window()
        elif option == "View Bank":
            self.view_bank_window()

    def new_bank_window(self):
        new_bank_window = Toplevel()
        new_bank_window.title("New Donor Information")
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

        # Donor ID
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
        contact_label.grid(row=2, column=0, padx=10, pady=10)
        contact_entry = Entry(new_bank_window)
        contact_entry.grid(row=2, column=1, padx=10, pady=10)

        # Services provided
        services_provided_label = Label(new_bank_window, text="Blood Type:")
        services_provided_label.grid(row=3, column=0, padx=10, pady=10)
        services_provided_combobox = ttk.Combobox(new_bank_window, values=self.blood_types, state="readonly")  # Create combobox
        services_provided_combobox.current(0)  # Set default value
        services_provided_combobox.grid(row=3, column=1, padx=10, pady=10)


        # Operating hours
        operating_hours_label = Label(new_bank_window, text="Gender:")
        operating_hours_label.grid(row=4, column=0, padx=10, pady=10)
        operating_hours_entry = Entry(new_bank_window)
        operating_hours_entry.grid(row=5, column=1, padx=10, pady=10)

        # Submit Button
        submit_button = Button(new_bank_window, text="Submit", command=lambda: submit_bank_info(blood_bank_id_entry, name_entry, location_entry, contact_entry, services_provided_combobox, operating_hours_entry))
        submit_button.grid(row=8, columnspan=2, padx=10, pady=10)