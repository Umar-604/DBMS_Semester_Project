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
