from tkinter import *
from PIL import Image, ImageTk


# Create the Tkinter window
dbms_root = Tk()
dbms_root.geometry("600x345")
dbms_root.minsize(300,300)

dbms_root.configure(background='black')  # Set background color to black

# Open and resize the image
image = Image.open(r"image/istockphoto-1224861391-612x612.jpg")
image = image.resize((dbms_root.winfo_screenwidth(), dbms_root.winfo_screenheight()))
background_image = ImageTk.PhotoImage(image)

# Create a Label with the background image
background_label = Label(dbms_root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Add other widgets on top of the background image
donation_label = Label(dbms_root, text="BLOOD DONATION PROJECT", font=("Helvetica", 24), bg="navyblue", fg="white")
donation_label.pack(pady=20)

# Run the Tkinter event loop
dbms_root.mainloop()

