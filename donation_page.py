from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]


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

    # Set the new position for the frame containing input widgets
    input_frame.place(x=bar_x, y=bar_y)

root = Tk()
root.geometry("500x500")
root.title("Make a Donation")

# Load the original image
original_image = Image.open("image1.jpg")

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

root.mainloop()