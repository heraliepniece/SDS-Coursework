import cv2
import skimage.feature
import sys

#Edge Detection:

image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

if image is None:
    print('Could not read image')

def edgedectection(image_path):   

    #Define the Sobel filters
    sobel_x = np.array([[-1, 0, 1],
                        [-2, 0, 2], 
                        [-1, 0, 1]])

    sobel_y = np.array([[-1, 0, 1],
                        [-2, 0, 2], 
                        [-1, 0, 1]])


#Compute the horizontal and vertical gradients
    gradient_x = cv2.filter2D(image,-1, sobel_x )
    gradient_y = sp.signal.convolve2d(image,-1,sobel_y )

#Compute the edge magnitude using the formula
    magnitude = np.sqrt(gradient_x ** 2 + gradient_y ** 2)

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

    plt.subplot(1,3,3)
    plt.imshow(magnitude, cmap='gray')
    plt.title("Edge magnitude")
    plt.axis("off")

    # Strong edge control
    sigma = float(sys.argv[2])
    low_threshold = float(sys.argv[3])
    high_threshold = float(sys.argv[4])

    edges = skimage.feature.canny(
        image = image,
        sigma = sigma,
        low_threshold= low_threshold, 
        high_threshold = high_threshold,
    )

    plt.show()

edgedetection(image)

   