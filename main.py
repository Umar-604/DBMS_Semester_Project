from tkinter import *
from tkinter import messagebox
from tkinter import ttk  # Import ttk module for themed widgets
from PIL import Image, ImageTk
from database import *

def open_donation_options():
    def on_option_click(option):
        if option == "New Donor":
            new_donor_window()
        elif option == "Existing Donor":
            existing_donor_window()

    def new_donor_window():
        new_donor_window = Toplevel(root)
        new_donor_window.title("New Donor Information")
        new_donor_window.geometry("400x400")


root = Tk()
root.title("Donation Page")
root.geometry("500x500")

# Styling
root.configure(bg="#f9efbe")
font_style = ("Arial", 12, "bold")

# Container Frame
container_frame = Frame(root, bg="#f9efbe")
container_frame.pack(fill="both", expand=True)

# Left Side Frame
left_frame = Frame(container_frame, bg="red")
left_frame.pack(side="left", fill="both", expand=True)
left_frame.pack_propagate(0)  # Prevent the frame from resizing

# Image
image_path = "front.jpeg"
image = Image.open(image_path)
image = image.resize((600, 750), Image.BICUBIC)  # Increase the size of the image
image = ImageTk.PhotoImage(image)
image_label = Label(left_frame, image=image, bg="red")
image_label.image = image
image_label.pack(fill="both", expand=True)

# Right Side Frame
right_frame = Frame(container_frame, bg="#f9efbe")
right_frame.pack(side="right", fill="both", expand=True)
right_frame.pack_propagate(0)  # Prevent the frame from resizing

# Heading
heading_label = Label(right_frame, text="Welcome to Blood Donation System", font=font_style, bg="#f9efbe")
heading_label.pack(pady=20)

# Option Frame
option_frame = Frame(right_frame, bg="#f9efbe")
option_frame.pack(pady=20)

# Buttons
button1 = Button(option_frame, text="Make Your Donation", command=open_donation_options)
button1.pack(pady=10)

button2 = Button(option_frame, text="Receiver")
button2.pack(pady=10)

# List of blood types and genders
blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
gender_types = ["Male", "Female", "None"]

root.mainloop()