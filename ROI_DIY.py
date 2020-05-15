from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from numba import jit
import copy
import bisect
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

    # Map the boundaries and thinning them on each row
    mapped = mp(pixels)

    # Green the pixels enclosed by the red marks
    masked = mask(pixels, mapped)

    # Display the masked results
    displayResults(pixels, masked)

    # Flatten the numpy arr
    flattened = flatten_numpyarr(masked)

    # Save final masked image
    im = Image.new('RGB', (image.size[0], image.size[1]))
    im.putdata(flattened)
    im.save("ROI_DIY.jpeg")


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
def mp(pixels):
    """
    Create a map where red pixels's position in a row is recorded
    """ 
    # Initialize the map
    mp = []

    # For each row in the given numpy array
    for i in range(len(pixels)):
        # Initialize a list with 0
        pos = [0]
        # First loop we add every red pixel to pos
        for j in range(len(pixels[0])):  
            if isRed(pixels[i][j]):
                pos.append(j)
        # Initialize an empty list
        new = []
        # Second loop we filter the pos such that continuous red pixels only have 1 mark
        for p in range(1, len(pos)): 
            # If a red pixel is at least 10 pixel apart from the previous cluster we mark it
            if pos[p] - pos[p-1] > 10:
                new.append(pos[p])
        # Map[i] is now a list of thinned markers
        mp.append(new)
    return mp


@jit
def mask(pixels, mp):
    """
    Paint a pixel as green if it is inside 
    """ 
    # We don't have to deep copy but we are displaying 2 graphs side by side, manipulating the original pixel would make them the same
    pixels = copy.deepcopy(pixels)

    # For each row of the image pixels
    for i in range(len(pixels)):
        # If our map indicates that there is at least 2 red pixel clusters
        if len(mp[i]) > 1:
            # From the leftmost red pixel to the rightmost red pixel 
            for j in range(mp[i][0]+1, mp[i][-1]):
                # If it is not a red pixel
                if isRed(pixels[i][j]) == False:
                    # 'insrt' gives us the left index in a sorted list where we would insert the value
                    insrt = bisect.bisect_left(mp[i], j)
                    # Using 'insrt' we can tell how many points to the left and right of the pixel are red -> odd for either means inside
                    if insrt % 2 == 1 or (len(mp[i]) - insrt) % 2 == 1:
                        # Paint it green for visual purposes
                        pixels[i][j] = [0, 255, 0]
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


def displayResults(pixels, masked):
    """
    Display original and masked original image
    """
    fig = plt.figure()
    fig.suptitle('Results')
    fig.add_subplot(1, 2, 1)
    plt.imshow(pixels)
    plt.title('Original')
    fig.add_subplot(1, 2, 2)
    plt.imshow(masked)
    plt.title('Masked Original Image')
    plt.show()


if __name__ == "__main__":
    main()