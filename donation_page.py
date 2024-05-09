from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from database import *

class DonationGUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x500")
        self.root.title("Make a Donation")
        self.create_input_frame()

    def create_input_frame(self):
        self.input_frame = Frame(self.root, bg="white")
        self.input_frame.pack(expand=True, padx=50, pady=50)

        # Search bar
        search_label = Label(self.input_frame, text="Search Donor ID:")
        search_label.grid(row=0, column=0, padx=10, pady=10)
        self.search_entry = Entry(self.input_frame)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10)
        search_button = Button(self.input_frame, text="Search", command=self.search_donation_info)
        search_button.grid(row=0, column=2, padx=10, pady=10)

        # Example input widgets
        title_label = Label(self.input_frame, text="Enter Donation Information", font=("Helvetica", 14, "bold"))
        title_label.grid(row=1, column=0, columnspan=3, pady=10)

        label1 = Label(self.input_frame, text="Donor ID:")
        label1.grid(row=2, column=0, padx=10, pady=10)
        self.donor_id_entry = Entry(self.input_frame)
        self.donor_id_entry.grid(row=2, column=1, padx=10, pady=10)

        label2 = Label(self.input_frame, text="Blood Bank ID:")
        label2.grid(row=3, column=0, padx=10, pady=10)
        self.blood_bank_id_entry = Entry(self.input_frame)
        self.blood_bank_id_entry.grid(row=3, column=1, padx=10, pady=10)

        label3 = Label(self.input_frame, text="Quantity Donated:")
        label3.grid(row=4, column=0, padx=10, pady=10)
        self.quantity_donated_entry = Entry(self.input_frame)
        self.quantity_donated_entry.grid(row=4, column=1, padx=10, pady=10)

        blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

        label4 = Label(self.input_frame, text="Blood Type:")
        label4.grid(row=5, column=0, padx=10, pady=10)
        self.blood_type_combobox = ttk.Combobox(self.input_frame, values=blood_types, state="readonly")  # Create combobox
        self.blood_type_combobox.current(0)  # Set default value
        self.blood_type_combobox.grid(row=5, column=1, padx=10, pady=10)

        label5 = Label(self.input_frame, text="Health Check Info:")
        label5.grid(row=6, column=0, padx=10, pady=10)
        self.health_check_information_entry = Entry(self.input_frame)
        self.health_check_information_entry.grid(row=6, column=1, padx=10, pady=10)

        submit_button = Button(self.input_frame, text="Submit", width="15", command=self.submit_donation_info)
        submit_button.grid(row=7, columnspan=2, pady=10)

        # Label to display donation records
        self.donation_records_label = Label(self.input_frame, text="", wraplength=400, justify="left")
        self.donation_records_label.grid(row=8, columnspan=3, padx=10, pady=10)

    def search_donation_info(self):
        donor_id = self.search_entry.get()
        if donor_id:
            donation_records = view_donation(donor_id)
            if donation_records:
                records_text = "\n".join([", ".join(map(str, record)) for record in donation_records])
                self.donation_records_label.config(text="Donation Records:\n" + records_text)
            else:
                self.donation_records_label.config(text="No records found for donor ID: " + donor_id)
        else:
            self.donation_records_label.config(text="Please enter a donor ID to search for donation records.")

    def submit_donation_info(self):
        donor_id = self.donor_id_entry.get()
        blood_bank_id = self.blood_bank_id_entry.get()
        quantity_donated = self.quantity_donated_entry.get()
        blood_type = self.blood_type_combobox.get()
        health_check_info = self.health_check_information_entry.get()

        # Call the function from the practice module to submit the donation info
        insert_donations(donor_id, blood_bank_id, quantity_donated, blood_type, health_check_info)
        messagebox.showinfo("Success", "Donation information submitted successfully.")

def open_donation_gui():
    root = Tk()
    donation_gui = DonationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    open_donation_gui()