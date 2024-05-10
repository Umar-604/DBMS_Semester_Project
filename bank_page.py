from tkinter import *
from tkinter import messagebox
from tkinter import ttk  # Import ttk module for themed widgets
from database import *

class BankGUI:
    def __init__(self, root):
        self.bank_options_window = root
        
        # Create the donation options window
        self.bank_options_window.title("Bank Options")
        self.bank_options_window.geometry("500x500")

        # New Donor button
        new_bank_button = Button(self.bank_options_window, text="New Bank", command=lambda: self.on_option_click("New Donor"))
        new_bank_button.pack(pady=10)

        # Existing Donor button
        view_bank_button = Button(self.bank_options_window, text="View Bank", command=lambda: self.on_option_click("Existing Donor"))
        view_bank_button.pack(pady=10)

    
    def on_option_click(self, option):
        if option == "New Bank":
            self.new_bank_window()
        elif option == "View Bank":
            self.view_bank_window()

    