from tkinter import *
from tkinter import messagebox
from tkinter import ttk  # Import ttk module for themed widgets
from database import *

class Inventory:
    def __init__(self, root):
        self.inventory = root
        self.inventory.geometry("500x500")
        self.inventory.title("Inventory Record")
        self.blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        self.tree = None  # Initialize Treeview widget

        # Button to view all data in inventory
        view_all_button = Button(self.inventory, text="View All Inventory", command=self.view_all_records_inventory)
        view_all_button.pack(pady=10)

        # Input bar to enter blood type
        self.blood_type_combobox = ttk.Combobox(self.inventory, values=self.blood_types, state="readonly")  # Create combobox
        self.blood_type_combobox.pack(pady=5)

        # Button to display inventory records based on blood type
        search_button = Button(self.inventory, text="Search by Blood Type", command=self.search_inventory_by_blood_type)
        search_button.pack(pady=5)

    def view_all_records_inventory(self):
        # Clear previous records
        if self.tree:
            self.tree.destroy()

        # Get all inventory records
        inventory_records = view_all_inventory()
        if inventory_records:
            self.tree = ttk.Treeview(self.inventory, show="headings", selectmode="browse")
            
            # Define columns
            self.tree["columns"] = ("Blood Bank ID", "Blood Type", "Quantity Available", "Expiry date", "Donor ID", "Serial No")
            
            # Column headings
            for column in self.tree["columns"]:
                self.tree.heading(column, text=column)
                self.tree.column(column, width=120, anchor="center")  # Adjust width as needed
            
            # Insert data
            for record in inventory_records:
                self.tree.insert("", "end", values=record)
            
            # Display Treeview
            self.tree.pack(fill="both", expand=True)
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(self.inventory, orient="vertical", command=self.tree.yview)
            scrollbar.pack(side="right", fill="y")
            self.tree.configure(yscrollcommand=scrollbar.set)
        else:
            messagebox.showinfo("No Records", "No records found ")

    def search_inventory_by_blood_type(self):
        # Clear previous records
        if self.tree:
            self.tree.destroy()

        blood_type = self.blood_type_combobox.get()
        inventory_records = view_inventory(blood_type)
        if inventory_records:
            self.tree = ttk.Treeview(self.inventory, show="headings", selectmode="browse")
            
            # Define columns
            self.tree["columns"] = ("Blood Bank ID", "Blood Type", "Quantity Available", "Expiry date", "Donor ID", "Serial No")
            
            # Column headings
            for column in self.tree["columns"]:
                self.tree.heading(column, text=column)
                self.tree.column(column, width=120, anchor="center")  # Adjust width as needed
            
            # Insert data
            for record in inventory_records:
                self.tree.insert("", "end", values=record)
            
            # Display Treeview
            self.tree.pack(fill="both", expand=True)
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(self.inventory, orient="vertical", command=self.tree.yview)
            scrollbar.pack(side="right", fill="y")
            self.tree.configure(yscrollcommand=scrollbar.set)
        else:
            messagebox.showinfo("No Records", "No records found for blood type: " + blood_type)