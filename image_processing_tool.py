from PIL import Image, ImageTk, ImageFilter
import numpy as np
import tkinter as tk
from tkinter import Label
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
import cv2


# GUI setup
root = tk.Tk()
root.geometry("700x700")
root.config(bg="white")
root.title("Image Processing Tool")

path = " "

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


# DEFINING GUI COMPONENTS
root.option_add("*Label*Background", "white")
root.option_add("*Button*Background", "lightgreen")

label = tk.Label(root)
label.pack(pady=10)

#defining the upload button
uploadButton = tk.Button(root, text="Locate Image", command=lambda:imageUploader())
uploadButton.pack(side=tk.BOTTOM, pady=20)

root.mainloop()

