from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from database import *

def submit_inventory_info(inventory_id_entry, blood_bank_id_entry, donor_id_entry):
    inventory_id = inventory_id_entry.get()
    blood_bank_id = blood_bank_id_entry.get()
    donor_id = donor_id_entry.get()
    insert_blood_inventory(inventory_id, blood_bank_id, donor_id)
    messagebox.showinfo( "Inventory table", "Information Inserted into Blood Inventory Table")


            