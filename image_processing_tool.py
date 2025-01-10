from PIL import Image, ImageTk
import numpy as np
import tkinter as tk
from tkinter import Label
from tkinter import filedialog
import matplotlib.pyplot as plt

# GUI
root = tk.Tk()
root.geometry("100x100")
root.config(bg="white")

#IMAGE UPLOADER FUNCTION:
def imageUploader():
    fileTypes = [("Image files","png","jpg","jpeg")] # Correct formatting? 
    path = tk.filedialog.askopenfilename(filetypes=fileTypes)

    if len(path):
        img = Image.open(path)
        img = img.resize((200,200))
        pic = ImageTk.PhotoImage(img)

        #re-sizing the app window in order to fit the picture
        # and button?
        app.geometry("560x300")
        label.config(image=pic)
        label.image = pic

        # if no file is selected, then display an error message:
    else:
        print("No file is chosen. Please choose a file")


# SETTING UP BACKGROUND IMAGE:
if __name__ == "__main__":

# Defining tkinter object
    app = tk.Tk()
    app.geometry("560x270")

    # adding background image
    img = ImageTk.PhotoImage(file='') # add an actual file here
    imgLabel = Label(app, image=img)
    imgLabel.place(x=0, y=0)


# DEFINING UPLOAD BUTTON
app.option_add("*Label*Background", "white")
app.option_add("*Button*Background", "lightgreen")

label = tk.Label(app)
label.pack(pady=10)

#defining the upload button
uploadButton = tk.Button(app, text"Locate Image", command=imageUploader)
uploadButton.pack(side=tk.BOTTOM, pady=20)

app.mainloop()


#GREYSCALE CONVERSION
# Loading the image
image = Image.open("example.jpg") # Replace with your image path
image_array = np.array(image) # Convert to NumPy array

print("Image shape:", image_array.shape) #Check the dimensions( height, width, 3 for RGB)

#Convert to greyscale by averaging the R, G, B channels
greyscale_array = np.mean(image_array, axis=2).astype(np.uint8) # Average along the color axis

#Display the original and greyscale images side by side
plt.figure(figsize=(10,5))
plt.subplot(1,2,1)
plt.imshow(greyscale_array, cmap='gray') # Show greyscale image
plt.title("Greyscale Image")
plt.axis("off")

plt.show()

#Image Blurring
# Load the image and convert to grayscale
image = Image.open("example.jpg").convert("L") # Convert to grayscale
image_array = np.array(image) # Convert to NumPy array

# Display the original image
plt. imshow(image_array, cmap= 'gray')
plt.title("Original Image")
plt.axis("off")
plt.show()

#Define the 3x3 blur kernel
kernel = np.array([[1,1,1],
                   [1,1,1],
                   [1,1,1]])/9 # Normalise the kernel to sum to 1

def convolve(image, kernel):
    #Get dimensions of the image and kernel

    #Determine the padding size
    pad_h = kernel_height // 2
    pad_w = kernel_width // 2

    #Pad the image with zeros( To handle edges)
    padded_image = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant')

    # Create an output array for the blurred image
    output = np.zeros_like(image)

    #Perform the convolution
    for i in range(image_height):

        for j in range(image_width):
        #Extract the region of the image under the kernel
        # Compute the weighted sum

            return output
        
    blurred_image = convolve(image_array, kernel)

    #Display the blurred image
    plt.imshow(blurred_image, cmap='gray')
    plt.title("Blurred Image")
    plt.axis("off")
    plt.show()


#Edge Detection:

#Define the Sobel filters
sobel_x = np.array([[-1, 0, 1],
                    [-2, 0, 2], 
                    [-1, 0, 1]])

sobel_y = np.array([[-1, 0, 1],
                    [-2, 0, 2], 
                    [-1, 0, 1]])

# Write a function to apply a kernel(filter) to an image using convolution(from previous sections)
#Compute the horizontal and vertical gradients

# Apply the sobel filters
gradient_x = convolve(image_array, sobel_x)
gradient_y = convolve(image_array, sobel_y)

#Display the gradients
plt.figure(figsize=(10,5))

plt.subplot(1,2,1)
plt.imshow(np.abs(gradient_x), cmap='gray')
plt.title("Horizontal Gradient (Gx)")
plt.axis("off")

plt.subplot(1,2,2)
plt.imshow(np.abs(gradient_y), cmap='gray')
plt.title("Vertical Gradient (Gy)")
plt.axis("off")

plt.show()

#Compute the edge magnitude using the formula

# To retain only strong edges apply a threshold. This filters out weak edges (low gradiet magnitudes)

root.mainloop()