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


