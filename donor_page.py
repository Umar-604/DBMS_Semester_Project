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