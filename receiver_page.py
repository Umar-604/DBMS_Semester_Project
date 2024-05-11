from tkinter import *
from tkinter import messagebox
from tkinter import ttk  # Import ttk module for themed widgets
from database import *

class ReceiverGUI:
    def __init__(self, root):
        self.receiver_options_window = root
        receiver_id_entry = None  # Define receiver_id_entry as a class attribute
        
        # Create the receiver options window
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
        
    def on_option_click(self, option):
        if option == "New Receiver":
            self.new_receiver_window()
        elif option == "Existing Receiver":
            self.existing_receiver_window()

    def new_receiver_window(self):
        new_receiver_window = Toplevel()
        new_receiver_window.title("New Receiver Information")
        new_receiver_window.geometry("400x400")

        # Rest of the code for the new receiver window...
        def submit_receiver_info(receiver_id_entry, name_entry, contact_entry, blood_type_combobox, dob_entry, gender_combobox, health_condition_entry, healthcare_facility_entry):
            receiver_id = receiver_id_entry.get()
            name = name_entry.get()
            contact = contact_entry.get()
            blood_type = blood_type_combobox.get()  # Getting the selected blood type from the combobox
            dob = dob_entry.get()
            gender = gender_combobox.get()
            health_condition = health_condition_entry.get()
            healthcare_facility = healthcare_facility_entry.get()

            insert_receiver(receiver_id, name, contact, blood_type, dob, gender, health_condition, healthcare_facility)
            messagebox.showinfo("Receiver Information", f"Receiver ID: {receiver_id}\nName: {name}\nContact: {contact}\nBlood Type: {blood_type}\nDate of Birth: {dob}\nGender: {gender}\nHealth Condition: {health_condition}\nHealthcare Facility: {healthcare_facility}")

        # Receiver ID
        receiver_id_label = Label(new_receiver_window, text="Receiver ID:")
        receiver_id_label.grid(row=0, column=0, padx=10, pady=10)
        receiver_id_entry = Entry(new_receiver_window)  # Assign to class attribute
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

        # Date of Birth
        dob_label = Label(new_receiver_window, text="Date of Birth:")
        dob_label.grid(row=5, column=0, padx=10, pady=10)
        dob_entry = Entry(new_receiver_window)
        dob_entry.grid(row=5, column=1, padx=10, pady=10)

         # Gender
        gender_label = Label(new_receiver_window, text="Gender:")
        gender_label.grid(row=4, column=0, padx=10, pady=10)
        gender_combobox = ttk.Combobox(new_receiver_window, values=self.gender_types, state="readonly")  # Create combobox
        gender_combobox.current(0)  # Set default value
        gender_combobox.grid(row=4, column=1, padx=10, pady=10)

         # Health History
        health_condition_label = Label(new_receiver_window, text="Health Condition:")
        health_condition_label.grid(row=6, column=0, padx=10, pady=10)
        health_condition_entry = Entry(new_receiver_window)
        health_condition_entry.grid(row=6, column=1, padx=10, pady=10)

        # Hospital/Healthcare Facility
        healthcare_facility_label = Label(new_receiver_window, text="Hospital/Healthcare Facility:")
        healthcare_facility_label.grid(row=8, column=0, padx=10, pady=10)
        healthcare_facility_entry = Entry(new_receiver_window)
        healthcare_facility_entry.grid(row=8, column=1, padx=10, pady=10)

         # Submit Button
        submit_button = Button(new_receiver_window, text="Submit", command=lambda: submit_receiver_info(receiver_id_entry, name_entry, contact_entry, blood_type_combobox, dob_entry, gender_combobox, health_condition_entry, healthcare_facility_entry))
        submit_button.grid(row=9, columnspan=2, padx=10, pady=10)

    def existing_receiver_window(self):
        existing_receiver_window = Toplevel()
        existing_receiver_window.title("Existing Receiver Information")
        existing_receiver_window.geometry("300x200")

        # Rest of the code for the existing receiver window...
        receiver_records_label = Label(existing_receiver_window, text="", wraplength=280, justify=LEFT)
        receiver_records_label.grid(row=2, columnspan=2, padx=10, pady=10)

        # Function to handle the submission of receiver ID
        def submit_receiver_id():
            recipient_id = receiver_id_entry.get()  # Access class attribute
            receiver_records = view_receiver(recipient_id)
            receiver_records_firebase = view_receiver_firebase(recipient_id)

            if receiver_records:
                # Add label for PostgreSQL table
                postgres_label = ttk.Label(existing_receiver_window, text="PostgreSQL Data")
                postgres_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

                # Create Treeview widget for PostgreSQL data
                tree_postgres = ttk.Treeview(existing_receiver_window)

                # Define columns
                tree_postgres["columns"] = ("Recipient ID", "Name", "Contact Information", "Blood Type", "Date of Birth", "Gender", "Health Condition", "Hospital")

                # Column headings
                for column in tree_postgres["columns"]:
                    tree_postgres.heading(column, text=column)

                # Insert data
                for record in receiver_records:
                    tree_postgres.insert("", "end", values=record)

                # Display Treeview
                tree_postgres.grid(row=6, columnspan=2, padx=10, pady=10, sticky="nsew")

                # Adjust column spacing
                for col in tree_postgres["columns"]:
                    tree_postgres.column(col, width=120, anchor="center")  # Adjust width as needed

                # Add scrollbar
                scrollbar_postgres = ttk.Scrollbar(existing_receiver_window, orient="vertical", command=tree_postgres.yview)
                scrollbar_postgres.grid(row=6, column=2, sticky="ns")
                tree_postgres.configure(yscrollcommand=scrollbar_postgres.set)
            else:
                messagebox.showinfo("No Records", "No records found for recipient ID: " + recipient_id)

            if receiver_records_firebase:
                # Add label for Firebase table
                firebase_label = ttk.Label(existing_receiver_window, text="Firebase Data")
                firebase_label.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

                # Create Treeview widget for Firebase data
                tree_firebase = ttk.Treeview(existing_receiver_window)

                # Define columns
                tree_firebase["columns"] = tuple(receiver_records_firebase[0].keys())

                # Column headings
                for column in tree_firebase["columns"]:
                    tree_firebase.heading(column, text=column)

                # Insert data
                for record in receiver_records_firebase:
                    values = [str(record[key]) for key in record]
                    tree_firebase.insert("", "end", values=values)

                # Display Treeview
                tree_firebase.grid(row=8, columnspan=2, padx=10, pady=10, sticky="nsew")

                # Adjust column spacing
                for col in tree_firebase["columns"]:
                    tree_firebase.column(col, width=120, anchor="center")  # Adjust width as needed

                # Add scrollbar
                scrollbar_firebase = ttk.Scrollbar(existing_receiver_window, orient="vertical", command=tree_firebase.yview)
                scrollbar_firebase.grid(row=8, column=2, sticky="ns")
                tree_firebase.configure(yscrollcommand=scrollbar_firebase.set)
            else:
                messagebox.showinfo("No Records", "No records found for recipient ID in Firebase: " + recipient_id)

        def delete_selected_donor():
            recipient_id = r_search_entry.get()  # Get the recipient ID from the entry
            receiver_records = view_receiver(recipient_id)

            if receiver_records:
                delete_receiver(recipient_id)
                messagebox.showinfo("Deletion", "The record is deleted ")
            else:  
                messagebox.showinfo("No Records", "No records found for recipient ID: " + recipient_id)

        # Receiver ID
        receiver_id_label = Label(existing_receiver_window, text="Receiver ID:")
        receiver_id_label.grid(row=0, column=0, padx=10, pady=10)
        receiver_id_entry = Entry(existing_receiver_window)  # Assign to class attribute
        receiver_id_entry.grid(row=0, column=1, padx=10, pady=10)

        # Submit Button
        submit_button = Button(existing_receiver_window, text="Submit", command=submit_receiver_id)
        submit_button.grid(row=1, columnspan=2, padx=10, pady=10)

        r_search_label = Label(existing_receiver_window, text="Enter Recipient ID:")
        r_search_label.grid(row=2, column=0, padx=10, pady=10)
        r_search_entry = Entry(existing_receiver_window)
        r_search_entry.grid(row=2, column=1, padx=10, pady=10)
        delete_button = Button(existing_receiver_window, text="Delete", command=lambda: delete_selected_donor())
        delete_button.grid(row=3, columnspan=2, padx=10, pady=10)

        # Adjust spacing for input bar labels
        existing_receiver_window.grid_rowconfigure(4, minsize=20)

# Main Tkinter window
def open_receiver_gui():
    root = Tk()
    donation_gui = ReceiverGUI(root)
    root.mainloop()

if __name__ == "__main__":
    open_receiver_gui()
