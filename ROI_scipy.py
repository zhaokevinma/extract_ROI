from PIL import Image
import numpy as np
from scipy import ndimage
from matplotlib import pyplot as plt
from numba import jit
from warnings import filterwarnings
filterwarnings('ignore')


@jit
def main():
    # Load image as numpy array
    image_path = 'data/contour.JPG'
    image = Image.open(image_path, 'r')
    pixels = image_to_numpyarr(image)

    # # Display the original data for testing purposes
    # displayOriginal(pixels)

    # Get ROI
    roi = getROI(pixels)

    # ROI returns a polyline. Fill this in using the scipy ndimage binary fill holes function
    mask = ndimage.binary_fill_holes(roi).astype(int)

    # Apply mask to green channel
    masked = maskOriginal(pixels, mask)

    # Display the masked results
    displayResults(roi, mask, masked)

    # Flatten the numpy arr
    flattened = flatten_numpyarr(masked)

    # Save final masked image
    im = Image.new('RGB', (image.size[0], image.size[1]))
    im.putdata(flattened)
    im.save('ROI_SciPy.jpeg')


@jit
def image_to_numpyarr(image):
    """
    Get a numpy array of an image so that one can access values[x][y]
    """
    width, height = image.size
    pixel_values = list(image.getdata())

    # Raise errors early on if image mode is not recognized
    if image.mode == 'RGB':
        channels = 3
    elif image.mode == 'L':
        channels = 1
    else:
        print("Unknown mode: %s" % image.mode)
        return None
    
    # Reshape 'pixel_values' to a 2d numpy arr 
    pixel_values = np.array(pixel_values).reshape((height, width, channels))
    return pixel_values


def isRed(pixel, sensitivity=50):
    """
    Return True if a pixel is red
    """ 
    # Get R G B values of the pixel
    red = pixel[0]
    green = pixel[1]
    blue = pixel[2]

    # If red value is greater than green and blue values within a sensitivity, consider it a red pixel
    if red - green > sensitivity and red - blue > sensitivity: 
        return True
    else:
        return False


@jit
def getROI(pixels, sensitivity=50):
    """
    Get ROI from original RGB image assuming it is red on a grayscale image
    """
    # Get size of image
    y, x = pixels.shape[:2]

    # Initialize output array
    roi = np.zeros((y, x), dtype=int)

    # Double for loop to go through each pixel in image
    for i in range(x):
        for j in range(y):
            # If red value is greater than green and blue values within a sensitivity, will mark as ROI
            if isRed(pixels[j, i]):
                roi[j, i] = 1
    return roi


@jit
def maskOriginal(pixels, mask):
    # Get size of image
    y, x = pixels.shape[:2]

    # Double for loop to go through each pixel in image
    for i in range(x):
        for j in range(y):
            # If the mask is present at a value, make green channel 255 and red and blue 0
            if mask[j, i] == 1:
                pixels[j, i, 0] = 0
                pixels[j, i, 1] = 255
                pixels[j, i, 2] = 0
    return pixels


@jit
def flatten_numpyarr(pixels):
    """
    Flatten the numpy array to list[tuple]
    """ 
    # Numpy 2d array
    np2d = pixels

    # Initialize a list
    fn1d = []

    # Append each pixel as (R, G, B)
    for i in range(len(np2d)):
        for j in range(len(np2d[0])):
            fn1d.append(tuple(np2d[i][j]))
    return fn1d


def displayOriginal(pixels):
    """
    Display R, G, and B channels separately to better view ROI
    """
    fig = plt.figure()
    fig.suptitle('RGB Channels')
    fig.add_subplot(2, 2, 1)
    plt.imshow(pixels)
    plt.title('RGB')
    fig.add_subplot(2, 2, 2)
    plt.imshow(pixels[:, :, 0], cmap='Reds_r')
    plt.title('Red')
    fig.add_subplot(2, 2, 3)
    plt.imshow(pixels[:, :, 1], cmap='Blues_r')
    plt.title('Blue')
    fig.add_subplot(2, 2, 4)
    plt.imshow(pixels[:, :, 2], cmap='Greens_r')
    plt.title('Green')
    plt.show()


def displayResults(roi, mask, pixels):
    """
    Display ROI, mask, and masked original image
    """
    fig = plt.figure()
    fig.suptitle('Results')
    fig.add_subplot(1, 3, 1)
    plt.imshow(roi, cmap='gray')
    plt.title('ROI')
    fig.add_subplot(1, 3, 2)
    plt.imshow(mask, cmap='gray')
    plt.title('Mask')
    fig.add_subplot(1, 3, 3)
    plt.imshow(pixels)
    plt.title('Masked Original Image')
    plt.show()


if __name__ == "__main__":
    main()