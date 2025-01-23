from PIL import Image, ImageTk, ImageFilter
import numpy as np
import tkinter as tk
from tkinter import Label, Toplevel
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
import cv2


#GUI SETUP
root = tk.Tk()
root.geometry("700x700")
root.config(bg="white")
root.title("Image Processing Tool")

path = " "

#FORM DETAILS FOR IMAGE
def enterDetails():
    global top
    top = Toplevel(root)
    top.geometry("500x500")
    top.title("Photo Description")
    l = Label(top,text = "Please describe your photo:")

    l.pack()

    # Labels and entry
    name_label = tk.Label(top, text="Enter the name of the image:")
    name_label.pack(pady=10)
    name_entry = tk.Entry(top)
    name_entry.pack(pady=5)

    photographer_label = tk.Label(top, text="Enter the name of the image:")
    photographer_label.pack(pady=10)
    photographer_entry = tk.Entry(top)
    photographer_entry.pack(pady=5)

    description_label = tk.Label(top, text="Enter a description of the image:")
    description_label.pack(pady=10)
    description_entry = tk.Entry(top)
    description_entry.pack(pady=5)
    
    date_label = tk.Label(top, text="Enter the date of the image:")
    date_label.pack(pady=10)
    date_entry = tk.Entry(top)
    date_entry.pack(pady=5)

    submission_label = tk.Label(top, text="Enter the date of submission of the image:")
    submission_label.pack(pady=10)
    submission_entry = tk.Entry(top)
    submission_entry.pack(pady=5)

def getDetails():
    global top, name_entry, photographer_entry, description_entry, date_entry, submission_entry
    name = name_entry.get()
    photographer = photographer_entry.get()  #is this right
    description = description_entry.get()
    date = date_entry.get()
    submission = submission_entry.get()

    if len(description_entry.get()) > 250:  # is this right?
        messagebox.showerror('Error', 'Please limit your description to 250 characters.')
        return

    print(f"Name: {name}, Photographer: {photographer}, Description:{description}, Date of image: {date}, Date of Submission: {submission}")

top.destroy()

submitButton = tk.Button(root, text="Submit Details", command=lambda:getDetails())
submitButton.pack(side=tk.BOTTOM, pady=20)

#IMAGE UPLOADER FUNCTION:
def imageUploader():
    try:
        global path
        fileTypes = [("Image files","*.png;*.jpg;*.jpeg")] 
        path = tk.filedialog.askopenfilename(filetypes=fileTypes)

        if len(path):
            img = Image.open(path)
            img = img.resize((200,200))
            pic = ImageTk.PhotoImage(img)

            #re-sizing the app window in order to fit the picture
            root.geometry("560x300")
            label.config(image=pic)
            label.image = pic

            getDetails()

         # if no file is selected, then display an error message:
        else:
            print("No file is chosen. Please choose a file")
    except Exception as e:
        print(f"An error occured: {e}")


#GREYSCALE CONVERSION
# Loading the image
def greyscaleConversion():
    if not path:
        print("No image was selected.")
        exit()

    image = Image.open(path) 
    image_array = np.array(image) # Convert to NumPy array

    print("Image shape:", image_array.shape) 

    #Convert to greyscale by averaging the R, G, B channels
    greyscale_array = np.mean(image_array, axis=2).astype(np.uint8) # Average along the color axis

    #Display the original and greyscale images side by side
    plt.figure(figsize=(10,5))
    plt.subplot(1,2,1)
    plt.imshow(greyscale_array, cmap='gray') # Show greyscale image
    plt.title("Greyscale Image")
    plt.axis("off")
    plt.show()

#IMAGE BLURRING
def imageBlur():
    if not path:
        print("No image was selected.")
        exit()
    #Load image
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    cv2.imshow('Original Image', image)
    cv2.waitKey(0)

    #Apply Gaussian Blur
    blurred_image = cv2.GaussianBlur(image, (5,5),0)

    #Display the blurred image
    cv2.imshow('Gaussian Blurring', blurred_image)
    cv2.waitKey(0)

    # Close all OpenCv Windows
    cv2.destroyAllWindows()

    #Display blurred image using Matplotlib
    plt.imshow(blurred_image, cmap='gray') 
    plt.title("Blurred Image")
    plt.axis("off")
    plt.show()

#Edge Detection:
def edgeDetection():
    if not path:
        print("No image was selected.")
        exit()
    # Load Image
    image = Image.open(path)

    #Convert image to greyscale
    image = image.convert("L")

    # Detect edges
    edge_detection = image.filter(ImageFilter.FIND_EDGES)

    # Display edge detected image
    plt.imshow(edge_detection, cmap='gray') 
    plt.title("Edge Detection")
    plt.axis("off")
    plt.show()

enterDetails()

# DEFINING GUI COMPONENTS
root.option_add("*Label*Background", "white")
root.option_add("*Button*Background", "lightgreen")

label = tk.Label(root)
label.pack(pady=10)

#defining the upload button
uploadButton = tk.Button(root, text="Locate Image", command=lambda:imageUploader())
uploadButton.pack(side=tk.BOTTOM, pady=20)

root.mainloop()

