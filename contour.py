from PIL import Image
import numpy
import statistics

def image_to_numpy(image_path):
    """Get a numpy array of an image so that one can access values[x][y]."""
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
    pixel_values = numpy.array(pixel_values).reshape((width, height, channels))
    return pixel_values

def edge_detection(image_path):
    pixels = image_to_numpy(image_path)
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for i in range(len(pixels) - 1):
        for j in range(len(pixels[0]) - 1):
            if statistics.stdev(pixels[i][j]) > 10:
                for di, dj in directions:
                    if statistics.stdev(pixels[i+di][j+dj]) < 11:
                        pixels[i][j] = [255, 0, 0]
    return pixels

def final_processing(image_path):
    np2d = edge_detection(image_path)
    fn1d = []
    for i in range(len(np2d)):
        for j in range(len(np2d[0])):
            fn1d.append(tuple(np2d[i][j]))

    return fn1d

processed = final_processing('data/brush.JPG')
im = Image.new('RGB', (415, 414))
im.putdata(processed)
im.show()
    

        