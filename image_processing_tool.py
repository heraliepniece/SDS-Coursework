from PIL import Image, ImageTk, ImageFilter
import numpy as np
import tkinter as tk
from tkinter import Label, Toplevel
from tkinter import messagebox, filedialog
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
from threading import Thread
import requests
from datetime import datetime

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
        if any(file.endswith(f".{file_extension}") for file in fileTypes):
            try:
                matched = True
                break
            except:
                logging.error("Unsupported image type.")
                messagebox.showerror("Unsupported image type. Please select an image with the following file extensions: png,jpg,jpeg")

        else:
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
    
    messagebox.showinfo("Success!", "Logged in successfully!")
    return credentials

def googleAuth():
    try:
        credentials = get_credentials()
        uploadimage()
    except Exception as e:
        logging.error(f"Google authentication failed: {e}")
        messagebox.showerror("Authentication Error", "Google login failed.")
    finally:
        root.withdraw()
       
#GUI SETUP
root = tk.Tk()
root.geometry("700x700")
root.config(bg="white")
root.title("Image Processing Tool")

path = ""

# upload image window
def uploadimage():
    global window1
    window1 = Toplevel(root)
    window1.geometry("500x500")
    window1.title("Upload and Image")
    j = Label(window1,text = "Please choose an image to upload.")

    j.pack()

    #defining the upload button
    uploadButton = tk.Button(window1, text="Locate Image", command=imageUploader)
    uploadButton.pack(side="bottom", pady=20)

#window for image processing functions:
def imageprocessing():
    window = Toplevel(root)
    window.geometry("500x500")
    window.title("Processing tools")
    i = Label(window,text = "Please select which image processing tool you would like to use:")

    i.pack(pady=10)

    if path:
        original = Image_open(path)
        orignal.thumbnail((300,300))

        img1 = ImageTk.PhotoImage(original)

        image_label = Label(window, image=img1)
        image_label.img1 = img1
        image_label.pack(pady=10)

    greyscaleButton = tk.Button(window, text="Greyscale Conversion", command=greyscaleConversion)
    greyscaleButton.pack(side="bottom", pady=10)

    blurringButton = tk.Button(window, text="Image Blurring", command=imageBlur)
    blurringButton.pack(side="bottom", pady=20)

    edgeButton = tk.Button(window, text="Edge Detection", command=edgeDetection)
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

    submitButton = tk.Button(top, text="Submit Details", command=getDetails)
    submitButton.pack(side="bottom", pady=20)


def getDetails():
                global top, name_entry, photographer_entry, description_entry, date_entry, submission_entry, window1
                name = name_entry.get()
                photographer = photographer_entry.get()  
                description = description_entry.get()
                date = date_entry.get()
                submission = submission_entry.get()


                if len(description_entry.get()) > 250:  
                    logging.error("Character length exceeded.")
                    messagebox.showerror('Error', 'Please limit your description to 250 characters.')
                    return
                
                if not photographer_entry.get():
                    logging.error("Null entry")
                    messagebox.showerror('Error', 'Please fill in all fields.')
                    return
                
                if not description_entry.get():
                    logging.error("Null entry")
                    messagebox.showerror('Error', 'Please fill in all fields.')
                    return
                
                if not date_entry.get():
                    logging.error("Null entry")
                    messagebox.showerror('Error', 'Please fill in all fields.')
                    return
                
                if not submission_entry.get():
                    logging.error("Null entry")
                    messagebox.showerror('Error', 'Please fill in all fields.')
                    return
                
                try:
                    datetime.strptime(date, "%d/%m/%y")
                except ValueError:
                    logging.error("Invalid date format for date field.")
                    messagebox.showerror('Error', 'Please write the date of image taken in the following format: dd/mm/yy.')
                    return

                try:
                    datetime.strptime(submission, "%d/%m/%y")
                except ValueError:
                    logging.error("Invalid date format for submission field.")
                    messagebox.showerror('Error', 'Please write the date of submission in the following format: dd/mm/yy.')
                    return

                print(f"Name: {name}, Photographer: {photographer}, Description:{description}, Date of image: {date}, Date of Submission: {submission}")
                top.destroy()

                window1.destroy()

                imageprocessing()

#IMAGE UPLOADER FUNCTION:
def imageUploader():
    try:
        global path
        global fileTypes
        fileTypes = [("Image files","*.png;*.jpg;*.jpeg")]   
        path = tk.filedialog.askopenfilename(filetypes=fileTypes)

        if len(path) > 0 and os.path.isfile(path):
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

    loaded_image = Image.open(path) 
    image_array = np.array(loaded_image) #Convert to NumPy array

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
    loaded_image = Image.open(path)

    gaussian_blurred_image = loaded_image.filter(ImageFilter.GaussianBlur(radius=2))

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
    loaded_image = Image.open(path)

    #Convert image to greyscale
    loaded_image = loaded_image.convert("L")

    # Detect edges
    edge_detection = loaded_image.filter(ImageFilter.FIND_EDGES)

    # Display edge detected image
    plt.imshow(edge_detection, cmap='gray') 
    plt.title("Edge Detection")
    plt.axis("off")
    plt.show()

# DEFINING GUI COMPONENTS
def main():
    global label

    root.option_add("*Label*Background", "white")
    root.option_add("*Button*Background", "lightgreen")

    label = tk.Label(root)
    label.pack(pady=10)

    intro_label = tk.Label(root, text = "Welcome to my image processing tool. Please log in to continue", font =("Times New Roman", 15))
    intro_label.pack(pady=40)

    #login button:
    loginbutton = tk.Button(root, text= "Log in with google",command=googleAuth)
    loginbutton.pack(pady=10)



main()

root.mainloop()

