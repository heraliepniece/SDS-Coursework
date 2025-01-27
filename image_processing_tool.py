from PIL import Image, ImageTk, ImageFilter
import numpy as np
import tkinter as tk
from tkinter import Label, Toplevel
from tkinter import messagebox, filedialog
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
import requests
import httplib2
import os
import webbrowser 
from tkinter import *
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapliclient.dicovery import build

# INITIALIZING LOGGING
import logging
logger = logging.getLogger(__name__)

logging.basicConfig(filename='app.log',format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)

# INITIALIZING SIGNATURES
def signature_test():
    global fileTypes
    SIGNATURES = {
    'png': bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]),
    'jpg': bytes([0xFF, 0xD8, 0xFF, 0xE0]),
    'jpeg':bytes([0xFF, 0xD8, 0xFF])
    }

    for file_extension, sig in SIGNATURES.items():

        try:
            if fileTypes.startswith(SIGNATURES[sig]):   #check if this works
                matched = True
                break
            else:
                logging.error("Unsupported image type.")
                messagebox.showerror("Unsupported image type. Please select an image with the following file extensions: png,jpg,jpeg")

        except:
            logging.error(f"Signature {sig} is missing a file extension.") # make all logging messages more descriptive
            messagebox.showerror(f"Signature {sig} is missing a file extension.")

    
# OAUTH SETUP

SCOPES = 'openid email'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Image Processing tool'

def get_credentials():
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secrets.json',
        scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email' ]
    )
    
    flow.run_local_server()
    credentials = flow.credentials

    user_info_service = build('oauth2', 'v2', credentials=credentials)
    user_info = user_info_service.userinfo().get().execute()
     # add a log?
    return credentials
def googleAuth():
    credentials = get_credentials()

       
#GUI SETUP
root = tk.Tk()
root.geometry("700x700")
root.config(bg="white")
root.title("Image Processing Tool")

path = ""

#window for image processing functions:
def imageprocessing():
    window = Toplevel(root)
    window.geometry("500x500")
    window.title("Processing tools")
    i = Label(window,text = "Please select which image processing tool you would like to use:")

    i.pack()

    greyscaleButton = tk.Button(root, text="Greyscale Conversion", command=greyscaleConversion)
    greyscaleButton.pack(side="bottom", pady=10)

    blurringButton = tk.Button(root, text="Image Blurring", command=imageBlur)
    blurringButton.pack(side="bottom", pady=20)

    edgeButton = tk.Button(root, text="Edge Detection", command=edgeDetection)
    edgeButton.pack(side="bottom", pady=30)


#FORM DETAILS FOR IMAGE
def enterDetails():
    global top, name_entry, photographer_entry, description_entry, date_entry, submission_entry
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

    photographer_label = tk.Label(top, text="Enter the name of the photographer:")
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

    submitButton = tk.Button(root, text="Submit Details", command=getDetails)
    submitButton.pack(side="bottom", pady=20)


def getDetails():
                global top, name_entry, photographer_entry, description_entry, date_entry, submission_entry
                name = name_entry.get()
                photographer = photographer_entry.get()  
                description = description_entry.get()
                date = date_entry.get()
                submission = submission_entry.get()

                if len(description_entry.get()) > 250:  
                    logging.error("Character length exceeded.")
                    messagebox.showerror('Error', 'Please limit your description to 250 characters.')
                    return

                print(f"Name: {name}, Photographer: {photographer}, Description:{description}, Date of image: {date}, Date of Submission: {submission}")
                top.destroy()


#IMAGE UPLOADER FUNCTION:
def imageUploader():
    try:
        global path
        global fileTypes
        fileTypes = [("Image files","*.png;*.jpg;*.jpeg")]   
        path = tk.filedialog.askopenfilename(filetypes=fileTypes)

        if len(path):
            img = Image.open(path)
            img = img.resize((200,200))
            pic = ImageTk.PhotoImage(img)

            # re-sizing the app window in order to fit the picture
            root.geometry("560x300")
            label.config(image=pic)
            label.image = pic
            
            enterDetails()
            
        # if no file is selected, then display an error message:
        else:
            logging.error("No file was chosen.")
            messagebox.showerror("File Selection Error","No file is chosen. Please choose a file")
    except FileNotFoundError:
       logging.error("File could not be located. ")
       messagebox.showerror("File Not Found Error", "No file could be found. Please check the path.")
    except Exception as e:
        logging.error(f"{e}")
        messagebox.showerror("Error", f"An error occured: {e}")

#GREYSCALE CONVERSION
# Loading the image
def greyscaleConversion():
    if not path:
        logging.error("No image was chosen.")
        messagebox.showerror("No image was selected.")
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
        logging.error("No image was chosen.")
        messagebox.showerror("No image was selected.")
        exit()
    #Load image
    image = Image.open(path)

    gaussian_blurred_image = image.filter(ImageFilter.GaussianBlur(radius=2))

    #Display blurred image using Matplotlib
    plt.imshow(gaussian_blurred_image) 
    plt.title("Blurred Image")
    plt.axis("off")
    plt.show()

#Edge Detection:
def edgeDetection():
    if not path:
        logging.error("No image was chosen.")
        messagebox.showerror("No image was selected.")
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
def main():

    root.option_add("*Label*Background", "white")
    root.option_add("*Button*Background", "lightgreen")

    label = tk.Label(root)
    label.pack(pady=10)

    #login button:
    loginbutton = tk.Button(root, text= "Log in with google",command=googleAuth)
    loginbutton(row=1, column=0)



    #defining the upload button
    uploadButton = tk.Button(root, text="Locate Image", command=imageUploader())
    uploadButton.pack(side="bottom", pady=20)

main()

root.mainloop()

