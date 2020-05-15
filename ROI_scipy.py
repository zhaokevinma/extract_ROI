from PIL import Image
import numpy as np
from scipy import ndimage
from matplotlib import pyplot as plt
from numba import jit
from warnings import filterwarnings
filterwarnings('ignore')


@jit()
def main():
	# Load image as numpy array
	image_path = 'data/contour.JPG'
	image = Image.open(image_path, 'r')
	pixels = np.array(image)

	displayOriginal(pixels)

	# Get ROI
	roi = getROI(pixels)

	# ROI returns a polyline. Fill this in using the scipy ndimage binary fill holes function
	mask = ndimage.binary_fill_holes(roi).astype(int)


	# Apply mask to green channel
	masked = maskOriginal(pixels, mask)

	displayResults(roi, mask, masked)

	# Save final masked image
	im = Image.fromarray(masked)
	im.save('filled.jpg')


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
			if pixels[j, i, 0] > pixels[j, i, 1] + sensitivity and pixels[
			    j, i, 0] > pixels[j, i, 2] + sensitivity:
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
	# plt.imshow(mask, cmap='Greens', alpha=0.6)
	plt.title('Masked Original Image')
	plt.show()


if __name__ == "__main__":
	main()
