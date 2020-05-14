# Find the pixels on the boundaries of a brushed area on an image 
# Store them in a list and output to a .txt file
# Paint them to a different color (in this case, Red) and show/save the modified image

from PIL import Image
import numpy as np
import statistics

def image_to_numpyarr(image_path):
    """
    Get a numpy array of an image so that one can access values[x][y]
    type image_path: str
    rtype: numpy.ndarray
    """
    image = Image.open(image_path, 'r')
    width, height = image.size
    pixel_values = list(image.getdata())
    if image.mode == 'RGB':
        channels = 3
    elif image.mode == 'L':
        channels = 1
    else:
        print("Unknown mode: %s" % image.mode)
        return None
    pixel_values = np.array(pixel_values).reshape((width, height, channels))
    return pixel_values

def is_label(pixel):
    """
    Tell whether a pixel is part of the labeled(brushed) area
    type pixel: numpy.ndarray 
    rtype: bool
    """  
    if statistics.stdev(pixel) > 10:
        return True
    else:
        return False

def boundary_detection(image_path):
    """
    Find pixels on the labeled boundary and store their (i, j) in a list
    type image_path: str
    rtype: List[tuple]
    """
    pixels = image_to_numpyarr(image_path)
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    boundary = []
    for i in range(len(pixels) - 1):
        for j in range(len(pixels[0]) - 1):
            if is_label(pixels[i][j]):
                for di, dj in directions:
                    if is_label(pixels[i+di][j+dj]) is False:
                        boundary.append((i, j))
    return boundary

def paint_boundary(image_path):
    """
    Find pixels on the labeled boundary and change their color to Red(in this case)
    type image_path: str
    rtype: numpy.ndarray
    """
    pixels = image_to_numpyarr(image_path)
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for i in range(len(pixels) - 1):
        for j in range(len(pixels[0]) - 1):
            if is_label(pixels[i][j]):
                for di, dj in directions:
                    if is_label(pixels[i+di][j+dj]) is False:
                        pixels[i][j] = [255, 0, 0]
    return pixels

def flatten_numpyarr(image_path):
    """
    Transform the 2D numpy array of pixel datat into a flattend list of tuples
    type image_path: str
    rtype: List[tuples]
    """
    np2d = paint_boundary(image_path)
    fn1d = []
    for i in range(len(np2d)):
        for j in range(len(np2d[0])):
            fn1d.append(tuple(np2d[i][j]))
    return fn1d

if __name__ == "__main__":

    image_path = 'data/brush.JPG'
    image = Image.open(image_path, 'r')
    pixels = flatten_numpyarr(image_path)
    points = boundary_detection(image_path)

    with open('boundary_positions.txt', 'w') as f:
        for tuple in points:
            f.write('%s %s\n' % tuple)

    im = Image.new('RGB', (image.size[0], image.size[1]))
    im.putdata(pixels)
    im.show()
    im.save("boundary_extracted.jpeg")
    

        