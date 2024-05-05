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

        # Donor ID
        donor_id_label = Label(new_donor_window, text="Donor ID:")
        donor_id_label.grid(row=0, column=0, padx=10, pady=10)
        donor_id_entry = Entry(new_donor_window)
        donor_id_entry.grid(row=0, column=1, padx=10, pady=10)

        # Name
        name_label = Label(new_donor_window, text="Name:")
        name_label.grid(row=1, column=0, padx=10, pady=10)
        name_entry = Entry(new_donor_window)
        name_entry.grid(row=1, column=1, padx=10, pady=10)

        # Contact
        contact_label = Label(new_donor_window, text="Contact:")
        contact_label.grid(row=2, column=0, padx=10, pady=10)
        contact_entry = Entry(new_donor_window)
        contact_entry.grid(row=2, column=1, padx=10, pady=10)

        # Blood Type
        blood_type_label = Label(new_donor_window, text="Blood Type:")
        blood_type_label.grid(row=3, column=0, padx=10, pady=10)
        blood_type_combobox = ttk.Combobox(new_donor_window, values=blood_types, state="readonly")  # Create combobox
        blood_type_combobox.current(0)  # Set default value
        blood_type_combobox.grid(row=3, column=1, padx=10, pady=10)

        # Gender
        gender_label = Label(new_donor_window, text="Gender:")
        gender_label.grid(row=4, column=0, padx=10, pady=10)
        gender_combobox = ttk.Combobox(new_donor_window, values=gender_types, state="readonly")  # Create combobox
        gender_combobox.current(0)  # Set default value
        gender_combobox.grid(row=4, column=1, padx=10, pady=10)

        # Date of Birth
        dob_label = Label(new_donor_window, text="Date of Birth:")
        dob_label.grid(row=5, column=0, padx=10, pady=10)
        dob_entry = Entry(new_donor_window)
        dob_entry.grid(row=5, column=1, padx=10, pady=10)

        # Health History
        health_history_label = Label(new_donor_window, text="Health History:")
        health_history_label.grid(row=6, column=0, padx=10, pady=10)
        health_history_entry = Entry(new_donor_window)
        health_history_entry.grid(row=6, column=1, padx=10, pady=10)

        # Last Donation Date
        last_donation_date_label = Label(new_donor_window, text="Last Donation Date:")
        last_donation_date_label.grid(row=7, column=0, padx=10, pady=10)
        last_donation_date_entry = Entry(new_donor_window)
        last_donation_date_entry.grid(row=7, column=1, padx=10, pady=10)

# Submit Button
submit_button = Button(new_donor_window, text="Submit", command=lambda: submit_donor_info(donor_id_entry, name_entry, contact_entry, blood_type_combobox, dob_entry, gender_combobox, health_history_entry, last_donation_date_entry))
submit_button.grid(row=8, columnspan=2, padx=10, pady=10)

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