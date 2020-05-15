from PIL import Image  # To open image and get raw pixel data
from matplotlib import pyplot as plt  # To plot and save image from numpy array
import numpy as np  # To reshape raw pixel data and access pixels[x][y]
import statistics  # Use stdev to detemine whether a given pixel is brushed
import bisect # To find where to insert an element in sorted list

def image_to_numpyarr(image_path):
    """
    Get a numpy array of an image so that one can access values[x][y]
    type image_path: str
    rtype: numpy.ndarray
    """
    image = Image.open(image_path, 'r')
    width, height = image.size
    pixel_values = list(image.getdata())  # 'pixels_values' is of type List[tuples] where each tuple is (R, G, B)
    if image.mode == 'RGB':  # This conditional block is to get 'channels' 'from image.mode'
        channels = 3
    elif image.mode == 'L':
        channels = 1
    else:
        print("Unknown mode: %s" % image.mode)  # Raise exception if 'image.mode' is neither 'RGB' nor 'L'
        return None
    pixel_values = np.array(pixel_values).reshape((height, width, channels))  # Reshape List[tuples] to numpy.ndarray
    return pixel_values

def isRed(pixel):
    """
    Tell whether a pixel is a red pixel
    type pixel: numpy.ndarray 
    rtype: bool
    """ 
    red = pixel[0]
    green = pixel[1]
    blue = pixel[2]
    if red - green > 50 and red - blue > 50 and abs(green - blue) < 30:  # There is more red in a red pixel 
        return True
    else:  # A normal CT pixel has similar/equal R G B values
        return False

def isBlue(pixel):
    """
    Tell whether a pixel is a blue pixel
    type pixel: numpy.ndarray 
    rtype: bool
    """ 
    red = pixel[0]
    green = pixel[1]
    blue = pixel[2]
    if red == 0 and green == 0 and blue == 255:  # [0, 0, 255]
        return True
    else:  # A normal CT pixel has similar/equal R G B values
        return False

def repaint_contour(pixels):
    """
    Repaint the contour to blue
    type pixel: numpy.ndarray 
    rtype: pixel numpy.ndarray 
    """ 
    for i in range(len(pixels)):
        for j in range(len(pixels[0])):
            if isRed(pixels[i][j]):
                pixels[i][j] = [0, 0, 255]
    return pixels

def mp(pixels):
    """
    Create a map where red pixels's position in a row is recorded
    type pixels: numpy.ndarray 
    rtype: List[List[int]]
    """ 
    mp = []
    for i in range(len(pixels)):
        pos = [0]
        for j in range(len(pixels[0])):  # First loop we add every red pixel to pos
            if isBlue(pixels[i][j]):
                pos.append(j)
        new = []
        count = 0
        for p in range(1, len(pos)):  # Second loop we filter the pos such that continuous red pixels only have 1 mark
            if pos[p] - pos[p-1] > 10 or count > 20:
                new.append(pos[p])
                count = 0
            else:
                count += 1
        mp.append(new)
    return mp

def mask(pixels, mp):
    """
    Paint a pixel as green if it is inside 
    type pixels: numpy.ndarray 
    rtype: List[List[int]]
    """ 
    for i in range(len(pixels)):
        if len(mp[i]) > 1:
            for j in range(mp[i][0]+1, mp[i][-1]):
                if isBlue(pixels[i][j]) == False:
                    insrt = bisect.bisect_left(mp[i], j)
                    if insrt % 2 == 1 or (len(mp[i]) - insrt) % 2 == 1: # If we find out that the intersection happens odd times we know it's inside
                        pixels[i][j] = [0, 255, 0]  # If it's inside the polygon we paint it green
    return pixels

def flatten_numpyarr(pixels):
    """
    Flatten the numpy array to a List[tuple]
    type pixels: numpy.ndarray 
    rtype: List[tuple]
    """ 
    np2d = pixels
    fn1d = []
    for i in range(len(np2d)):
        for j in range(len(np2d[0])):
            fn1d.append(tuple(np2d[i][j]))
    return fn1d

if __name__ == "__main__":

    image_path = 'data/contour.JPG'

    pixels = image_to_numpyarr(image_path)
    blued = repaint_contour(pixels)
    mapped = mp(blued)
    masked = mask(pixels, mapped)

    plt.imshow(masked)
    plt.show()