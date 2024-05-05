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


root = Tk()
root.geometry("500x500")
root.title("Make a Donation")

root.mainloop()