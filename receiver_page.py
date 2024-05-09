from tkinter import *
from tkinter import messagebox
from tkinter import ttk  # Import ttk module for themed widgets
from database import *

class ReceiverGUI:
    def __init__(self, root):
        self.receiver_options_window = root
        
    def on_option_click(self, option):
        if option == "New Receiver":
            self.new_receiver_window()
        elif option == "Existing Receiver":
            self.existing_receiver_window()

    def new_receiver_window(self):
        new_receiver_window = Toplevel()
        new_receiver_window.title("New receiver Information")
        new_receiver_window.geometry("400x400")

        # Rest of the code for the new receiver window...
        def submit_reciever_info(reciever_id_entry, name_entry, contact_entry, blood_type_combobox, dob_entry, gender_combobox, health_history_entry, last_donation_date_entry):
            receiver_id = reciever_id_entry.get()
            name = name_entry.get()
            contact = contact_entry.get()
            blood_type = blood_type_combobox.get()  # Getting the selected blood type from the combobox
            dob = dob_entry.get()
            gender = gender_combobox.get()
            health_history = health_history_entry.get()
            last_donation_date = last_donation_date_entry.get()

            insert_receiver(receiver_id, name, contact, blood_type, dob, gender, health_history, last_donation_date)
            messagebox.showinfo("receiver Information", f"receiver ID: {receiver_id}\nName: {name}\nContact: {contact}\nBlood Type: {blood_type}\nDate of Birth: {dob}\nGender: {gender}\nHealth History: {health_history}\nLast Donation Date: {last_donation_date}")

        # receiver ID
        receiver_id_label = Label(new_receiver_window, text="receiver ID:")
        receiver_id_label.grid(row=0, column=0, padx=10, pady=10)
        receiver_id_entry = Entry(new_receiver_window)
        receiver_id_entry.grid(row=0, column=1, padx=10, pady=10)

        # Name
        name_label = Label(new_receiver_window, text="Name:")
        name_label.grid(row=1, column=0, padx=10, pady=10)
        name_entry = Entry(new_receiver_window)
        name_entry.grid(row=1, column=1, padx=10, pady=10)

        # Contact
        contact_label = Label(new_receiver_window, text="Contact:")
        contact_label.grid(row=2, column=0, padx=10, pady=10)
        contact_entry = Entry(new_receiver_window)
        contact_entry.grid(row=2, column=1, padx=10, pady=10)

         # Blood Type
        blood_type_label = Label(new_receiver_window, text="Blood Type:")
        blood_type_label.grid(row=3, column=0, padx=10, pady=10)
        blood_type_combobox = ttk.Combobox(new_receiver_window, values=self.blood_types, state="readonly")  # Create combobox
        blood_type_combobox.current(0)  # Set default value
        blood_type_combobox.grid(row=3, column=1, padx=10, pady=10)

         # Gender
        gender_label = Label(new_receiver_window, text="Gender:")
        gender_label.grid(row=4, column=0, padx=10, pady=10)
        gender_combobox = ttk.Combobox(new_receiver_window, values=self.gender_types, state="readonly")  # Create combobox
        gender_combobox.current(0)  # Set default value
        gender_combobox.grid(row=4, column=1, padx=10, pady=10)

        # Date of Birth
        dob_label = Label(new_receiver_window, text="Date of Birth:")
        dob_label.grid(row=5, column=0, padx=10, pady=10)
        dob_entry = Entry(new_receiver_window)
        dob_entry.grid(row=5, column=1, padx=10, pady=10)

         # Health History
        health_history_label = Label(new_receiver_window, text="Health History:")
        health_history_label.grid(row=6, column=0, padx=10, pady=10)
        health_history_entry = Entry(new_receiver_window)
        health_history_entry.grid(row=6, column=1, padx=10, pady=10)

        # Hospital/Healthcare Facility
        healthcare_facility_label = Label(new_receiver_window, text="Hospital/Healthcare Facility:")
        healthcare_facility_label.grid(row=8, column=0, padx=10, pady=10)
        healthcare_facility_entry = Entry(new_receiver_window)
        healthcare_facility_entry.grid(row=8, column=1, padx=10, pady=10)

         # Submit Button
        submit_button = Button(new_receiver_window, text="Submit", command=lambda: submit_receiver_info(receiver_id_entry, name_entry, contact_entry, blood_type_combobox, dob_entry, gender_combobox, health_history_entry, last_donation_date_entry))
        submit_button.grid(row=8, columnspan=2, padx=10, pady=10)


        # Create the donation options window
        self.receiver_options_window.title("Receiver Options")
        self.receiver_options_window.geometry("500x500")

        # New Receiver button
        new_receiver_button = Button(self.receiver_options_window, text="New Receiver", command=lambda: self.on_option_click("New Receiver"))
        new_receiver_button.pack(pady=10)

        # Existing Receiver button
        existing_receiver_button = Button(self.receiver_options_window, text="Existing Receiver", command=lambda: self.on_option_click("Existing Receiver"))
        existing_receiver_button.pack(pady=10)

        self.blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        self.gender_types = ["Male", "Female", "None"]
        
def existing_receiver_window(self):
        existing_receiver_window = Toplevel()
        existing_receiver_window.title("Existing  receiver Information")
        existing_receiver_window.geometry("300x200")

        # Rest of the code for the existing  receiver window...
        receiver_records_label = Label(existing_receiver_window, text="", wraplength=280, justify=LEFT)
        receiver_records_label.grid(row=2, columnspan=2, padx=10, pady=10)

        # Function to handle the submission of  receiver ID
        def submit_receiver_id():
            receiver_id = receiver_id_entry.get()
            receiver_records = view_receiver(receiver_id)
            if receiver_records:
                # Convert  receiver records to a string
                records_text = ""
                for record in receiver_records:
                    records_text += ", ".join(str(field) for field in record) + "\n"
                receiver_records_label.config(text=records_text)
            else:
                receiver_records_label.config(text="No records found for  receiver ID: " + receiver_id)

        #  receiver ID
        receiver_id_label = Label(existing_receiver_window, text="Donor ID:")
        receiver_id_label.grid(row=0, column=0, padx=10, pady=10)
        receiver_id_entry = Entry(existing_receiver_window)
        receiver_id_entry.grid(row=0, column=1, padx=10, pady=10)

        # Submit Button
        submit_button = Button(existing_receiver_window, text="Submit", command=submit_receiver_id)
        submit_button.grid(row=1, columnspan=2, padx=10, pady=10)
