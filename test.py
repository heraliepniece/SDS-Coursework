from PIL import Image, ImageTk
import numpy as np
import tkinter as tk
from tkinter import Label
from tkinter import filedialog
import matplotlib.pyplot as plt

# GUI setup
root = tk.Tk()
root.geometry("100x100")
root.config(bg="white")

path = " "


#IMAGE UPLOADER FUNCTION:
def imageUploader():
    fileTypes = [("Image files","*.png;*.jpg;*.jpeg")] 
    path = tk.filedialog.askopenfilename(filetypes=fileTypes)

    if len(path):
        img = Image.open(path)
        img = img.resize((200,200))
        pic = ImageTk.PhotoImage(img)

        #re-sizing the app window in order to fit the picture
        # and button?
        root.geometry("560x300")
        label.config(image=pic)
        label.image = pic

        # if no file is selected, then display an error message:
    else:
        print("No file is chosen. Please choose a file")


# SETTING UP BACKGROUND IMAGE:
#if __name__ == "__main__":

# Defining tkinter object
   # root.geometry("560x270")

    # adding background image
    #img = ImageTk.PhotoImage(file=path ) 
   # imgLabel = Label(root, image=img)
    #imgLabel.place(x=0, y=0)


# DEFINING UPLOAD BUTTON
root.option_add("*Label*Background", "white")
root.option_add("*Button*Background", "lightgreen")

label = tk.Label(root)
label.pack(pady=10)

#defining the upload button
uploadButton = tk.Button(root, text="Locate Image", command=imageUploader())
uploadButton.pack(side=tk.BOTTOM, pady=20)

root.mainloop()