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

