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
