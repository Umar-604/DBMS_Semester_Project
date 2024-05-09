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

def resize_image(event):
    # Get the new canvas size
    new_width = event.width
    new_height = event.height
    
    # Resize the image to fit the canvas
    resized_image = original_image.resize((new_width, new_height), Image.BICUBIC)
    photo = ImageTk.PhotoImage(resized_image)
    canvas.itemconfig(canvas_image, image=photo)
    canvas.image = photo  # Keep a reference to prevent garbage collection
    
    # Resize the rectangle
    canvas.coords(rectangle, 0, 0, new_width, new_height)
    
    # Reposition the input bar
    reposition_input_bar(new_width, new_height)

def reposition_input_bar(new_width, new_height):
    # Calculate the center position for the input bar
    bar_x = new_width // 2 - input_frame.winfo_reqwidth() // 2
    bar_y = new_height // 2 - input_frame.winfo_reqheight() // 2
    
    # Set the new position for the frame containing input widgets
    input_frame.place(x=bar_x, y=bar_y)

root = Tk()
root.geometry("500x500")
root.title("Make a Donation")

# Load the original image
original_image = Image.open("image/image1.jpg")

# Create a Canvas
canvas = Canvas(root)
canvas.pack(fill="both", expand=True)

# Bind the resize_image function to the canvas resize event
canvas.bind("<Configure>", resize_image)

# Resize the canvas to fit the window initially
width, height = root.winfo_width(), root.winfo_height()
canvas.config(width=width, height=height)

# Resize the image to fit the canvas initially
resized_image = original_image.resize((width, height), Image.BICUBIC)
photo = ImageTk.PhotoImage(resized_image)

# Create the background image on the canvas
canvas_image = canvas.create_image(0, 0, anchor=NW, image=photo)

# Create a semi-transparent white rectangle as a watermark
rectangle = canvas.create_rectangle(0, 0, width, height, fill="white", stipple="gray75")

# Create a frame for input widgets
input_frame = Frame(root, bg="white")

# Example input widgets

title_label = Label(input_frame, text="Enter Inventory Information", font=("Helvetica", 14, "bold"))
title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

label1 = Label(input_frame, text="Inventory ID:")
label1.grid(row=1, column=0, padx=10, pady=10)
inventory_id_entry = Entry(input_frame)
inventory_id_entry.grid(row=1, column=1, padx=10, pady=10)

label2 = Label(input_frame, text="Blood Bank ID:")
label2.grid(row=2, column=0, padx=10, pady=10)
blood_bank_id_entry = Entry(input_frame)
blood_bank_id_entry.grid(row=2, column=1, padx=10, pady=10)

label3 = Label(input_frame, text="Donor ID:")
label3.grid(row=3, column=0, padx=10, pady=10)
donor_id_entry = Entry(input_frame)
donor_id_entry.grid(row=3, column=1, padx=10, pady=10)

submit_button = Button(input_frame, text="Submit", width="15", command=lambda: submit_inventory_info(inventory_id_entry, blood_bank_id_entry, donor_id_entry))
submit_button.grid(row=4, columnspan=2, padx=10, pady=10)

root.mainloop()
