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

        # Search donation records in PostgreSQL
        donation_records_postgres = view_donation(donor_id)

        # Search donation records in Firebase
        donation_records_firebase = view_donation_in_firebase(donor_id)

        if not donor_id:
            messagebox.showinfo("Error", "Please enter a donor ID to search for donation records.")
            return

        if not donation_records_postgres and not donation_records_firebase:
            messagebox.showinfo("No Records", "No records found for donor ID: " + donor_id)
            return

        # Clear any existing labels or treeviews
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        # Display PostgreSQL data
        if donation_records_postgres:
            postgres_label = ttk.Label(self.input_frame, text="PostgreSQL Data")
            postgres_label.pack(pady=5)

            tree_postgres = ttk.Treeview(self.input_frame)
            tree_postgres["columns"] = ("Donor ID", "Blood Bank ID", "Quantity Donated (ml)", "Blood Type", "Health Check Information", "Donation ID")

            for col in tree_postgres["columns"]:
                tree_postgres.heading(col, text=col)

            for record in donation_records_postgres:
                tree_postgres.insert("", "end", values=record)

            tree_postgres.pack(padx=10, pady=10, fill="both", expand=True)

            # Adjust column spacing
            for col in tree_postgres["columns"]:
                tree_postgres.column(col, width=140, anchor="center")  # Adjust width as needed

            # Add scrollbar
            scrollbar_postgres = ttk.Scrollbar(self.input_frame, orient="vertical", command=tree_postgres.yview)
            scrollbar_postgres.pack(side="right", fill="y")
            tree_postgres.configure(yscrollcommand=scrollbar_postgres.set)
        else:
            messagebox.showinfo("No Records", "No records found for donor ID: " + donor_id)

        # Display Firebase data
        if donation_records_firebase:
            firebase_label = ttk.Label(self.input_frame, text="Firebase Data")
            firebase_label.pack(pady=5)

            tree_firebase = ttk.Treeview(self.input_frame)
            tree_firebase["columns"] = tuple(donation_records_firebase[0].keys())

            for col in tree_firebase["columns"]:
                tree_firebase.heading(col, text=col)

            for record in donation_records_firebase:
                values = [str(record[key]) for key in record]
                tree_firebase.insert("", "end", values=values)

            tree_firebase.pack(padx=10, pady=10, fill="both", expand=True)

            # Adjust column spacing
            for col in tree_firebase["columns"]:
                tree_firebase.column(col, width=120, anchor="center")  # Adjust width as needed

            # Add scrollbar
            scrollbar_firebase = ttk.Scrollbar(self.input_frame, orient="vertical", command=tree_firebase.yview)
            scrollbar_firebase.pack(side="right", fill="y")
            tree_firebase.configure(yscrollcommand=scrollbar_firebase.set)
        else:
            messagebox.showinfo("No Records", "No records found for donor ID in Firebase: " + donor_id)


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