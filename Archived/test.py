import os, sys, tkinter as tk, asyncio, kasa, pygame.mixer
from distutils import dir_util
from tkinter import PhotoImage, Button, Label, Canvas, Tk, ttk, simpledialog
from PIL import Image, ImageTk, ImageOps
from kasa import SmartPlug
from functools import partial
from os import getcwd as cwd

def rename_string():
    # Get the current string
    current_string = label_var.get()

    # Show a popup dialog for renaming
    new_string = simpledialog.askstring("Rename String", "Enter a new name:", initialvalue=current_string)

    # Update the label with the new string if a value is provided
    if new_string:
        label_var.set(new_string)

# Create the main window
root = tk.Tk()
root.title("String Renaming Example")

# Create a label with an initial string
label_var = tk.StringVar(value="Original String")
label = tk.Label(root, textvariable=label_var)
label.pack(pady=10)

# Create a button to trigger the renaming
rename_button = tk.Button(root, text="Rename String", command=rename_string)
rename_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()