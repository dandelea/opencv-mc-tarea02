from matplotlib import pyplot as plt
import cv2
import numpy as np

def erosion(img_url, factor):
	img = cv2.imread(img_url, 0)
	kernel = np.ones((5,5),np.uint8)
	erosion = cv2.erode(img, kernel, iterations = factor)

	plt.subplot(1,2,1),plt.imshow(img ,cmap = 'gray')
	plt.title('Original'), plt.xticks([]), plt.yticks([])
	plt.subplot(1,2,2),plt.imshow(erosion ,cmap = 'gray')
	plt.title('Erosion x' + str(factor)), plt.xticks([]), plt.yticks([])

	plt.show()

def dilation(img_url, factor):
	img = cv2.imread(img_url, 0)
	kernel = np.ones((5,5),np.uint8)
	dilation = cv2.dilate(img, kernel, iterations = factor)

	plt.subplot(1,2,1),plt.imshow(img ,cmap = 'gray')
	plt.title('Original'), plt.xticks([]), plt.yticks([])
	plt.subplot(1,2,2),plt.imshow(dilation ,cmap = 'gray')
	plt.title('Dilation x' + str(factor)), plt.xticks([]), plt.yticks([])

	plt.show()

def opening(img_url):
	img = cv2.imread(img_url, 0)
	kernel = np.ones((5,5),np.uint8)
	opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

	plt.subplot(1,2,1),plt.imshow(img ,cmap = 'gray')
	plt.title('Original'), plt.xticks([]), plt.yticks([])
	plt.subplot(1,2,2),plt.imshow(opening ,cmap = 'gray')
	plt.title('Opening'), plt.xticks([]), plt.yticks([])

	plt.show()

def closing(img_url):
	img = cv2.imread(img_url, 0)
	kernel = np.ones((5,5),np.uint8)
	closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

	plt.subplot(1,2,1),plt.imshow(img ,cmap = 'gray')
	plt.title('Original'), plt.xticks([]), plt.yticks([])
	plt.subplot(1,2,2),plt.imshow(closing ,cmap = 'gray')
	plt.title('Closing'), plt.xticks([]), plt.yticks([])

	plt.show()