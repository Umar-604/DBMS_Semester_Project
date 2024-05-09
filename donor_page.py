from tkinter import *
from tkinter import messagebox
from tkinter import ttk  
from database import *

class DonorGUI:
    def _init_(self, root):
        self.donation_options_window = root

        # Create the donation options window
        self.donation_options_window.title("Donation Options")
        self.donation_options_window.geometry("500x500")
        
        # New Donor button
        new_donor_button = Button(self.donation_options_window, text="New Donor", command=lambda: self.on_option_click("New Donor"))
        new_donor_button.pack(pady=10)

        # Existing Donor button
        existing_donor_button = Button(self.donation_options_window, text="Existing Donor", command=lambda: self.on_option_click("Existing Donor"))
        existing_donor_button.pack(pady=10)

        self.blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        self.gender_types = ["Male", "Female", "None"]


    def new_donor_window(self):
        new_donor_window = Toplevel()
        new_donor_window.title("New Donor Information")
        new_donor_window.geometry("400x400")

        # Rest of the code for the new donor window...
        def submit_donor_info(donor_id_entry, name_entry, contact_entry, blood_type_combobox, dob_entry, gender_combobox, health_history_entry, last_donation_date_entry):
            donor_id = donor_id_entry.get()
            name = name_entry.get()
            contact = contact_entry.get()
            blood_type = blood_type_combobox.get()  # Getting the selected blood type from the combobox
            dob = dob_entry.get()
            gender = gender_combobox.get()
            health_history = health_history_entry.get()
            last_donation_date = last_donation_date_entry.get()

            insert_donor(donor_id, name, contact, blood_type, dob, gender, health_history, last_donation_date)
            messagebox.showinfo("Donor Information", f"Donor ID: {donor_id}\nName: {name}\nContact: {contact}\nBlood Type: {blood_type}\nDate of Birth: {dob}\nGender: {gender}\nHealth History: {health_history}\nLast Donation Date: {last_donation_date}")

        # Donor ID
        donor_id_label = Label(new_donor_window, text="Donor ID:")
        donor_id_label.grid(row=0, column=0, padx=10, pady=10)
        donor_id_entry = Entry(new_donor_window)
        donor_id_entry.grid(row=0, column=1, padx=10, pady=10)

        # Name
        name_label = Label(new_donor_window, text="Name:")
        name_label.grid(row=1, column=0, padx=10, pady=10)
        name_entry = Entry(new_donor_window)
        name_entry.grid(row=1, column=1, padx=10, pady=10)

        # Contact
        contact_label = Label(new_donor_window, text="Contact:")
        contact_label.grid(row=2, column=0, padx=10, pady=10)
        contact_entry = Entry(new_donor_window)
        contact_entry.grid(row=2, column=1, padx=10, pady=10)

        # Blood Type
        blood_type_label = Label(new_donor_window, text="Blood Type:")
        blood_type_label.grid(row=3, column=0, padx=10, pady=10)
        blood_type_combobox = ttk.Combobox(new_donor_window, values=self.blood_types, state="readonly")  # Create combobox
        blood_type_combobox.current(0)  # Set default value
        blood_type_combobox.grid(row=3, column=1, padx=10, pady=10)

        # Gender
        gender_label = Label(new_donor_window, text="Gender:")
        gender_label.grid(row=4, column=0, padx=10, pady=10)
        gender_combobox = ttk.Combobox(new_donor_window, values=self.gender_types, state="readonly")  # Create combobox
        gender_combobox.current(0)  # Set default value
        gender_combobox.grid(row=4, column=1, padx=10, pady=10)

        # Date of Birth
        dob_label = Label(new_donor_window, text="Date of Birth:")
        dob_label.grid(row=5, column=0, padx=10, pady=10)
        dob_entry = Entry(new_donor_window)
        dob_entry.grid(row=5, column=1, padx=10, pady=10)

        # Health History
        health_history_label = Label(new_donor_window, text="Health History:")
        health_history_label.grid(row=6, column=0, padx=10, pady=10)
        health_history_entry = Entry(new_donor_window)
        health_history_entry.grid(row=6, column=1, padx=10, pady=10)

        # Last Donation Date
        last_donation_date_label = Label(new_donor_window, text="Last Donation Date:")
        last_donation_date_label.grid(row=7, column=0, padx=10, pady=10)
        last_donation_date_entry = Entry(new_donor_window)
        last_donation_date_entry.grid(row=7, column=1, padx=10, pady=10)

        # Submit Button
        submit_button = Button(new_donor_window, text="Submit", command=lambda: submit_donor_info(donor_id_entry, name_entry, contact_entry, blood_type_combobox, dob_entry, gender_combobox, health_history_entry, last_donation_date_entry))
        submit_button.grid(row=8, columnspan=2, padx=10, pady=10)

    
