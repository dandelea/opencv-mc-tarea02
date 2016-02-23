#!/usr/bin/python

#
# Implements 8-connectivity connected component labeling
# 
# Algorithm obtained from "Optimizing Two-Pass Connected-Component Labeling 
# by Kesheng Wu, Ekow Otoo, and Kenji Suzuki
#

import cv2
import random
import numpy as np
from matplotlib import pyplot as plt

def run(img):
	height, width = img.shape
 
	#
	# First pass
	#
 
	# Dictionary of point:label pairs
	labels = np.zeros((height,width), np.uint8)

	# Current label being assigned
	current_label = 0;

	# Equivalent labels
	# Dictionary of label->label
	eq_labels = {}
 
	for x in range(0, height):
		for y in range(0, width):

			#
			# Pixel names were chosen as shown:
			#
			#   -------------
			#   |   | a |   |
			#   -------------
			#   | b | c |   |
			#   -------------
			#   |   |   |   |
			#   -------------
			#
			# The current pixel is c
			# a and b are its neighbors of interest
			#
			# 255 is white, 0 is black
			# White pixels part of the background, so they are ignored
			# If a pixel lies outside the bounds of the image, it default to white
			#
	 
			# If the current pixel is white, it's obviously not a component...
			if img[x, y] == 255:
				pass
			
			else:
				# If pixel a is in the image and black, and pixel d is in the image and black
				# 	 a, b and c are neighbors, so they are all part of the same component
				# 	 Therefore, check components of a and b
				if y > 0 and img[x, y-1] == 0 and x > 0 and img[x-1, y] == 0:
					labels[x, y] = labels[x, y-1]
					# If component of a and b are not the same
					# 	 Store a reference a->b
					if labels[x, y-1] != labels[x-1, y]:
						print(str(x) + "," + str(y))
						eq_labels[max(labels[x, y-1], labels[x-1, y])] = min(labels[x, y-1], labels[x-1, y])

				else:

					# If pixel a is in the image and black:
					#    b and c are its neighbors, so they are all part of the same component
					#    Therefore, there is no reason to check their labels
					#    so simply assign a's label to c
					if y > 0 and img[x, y-1] == 0:
						labels[x, y] = labels[x, y-1]
					# If pixel d is in the image and black
					#    We already know a is white
					#    so simpy assign b's label to c
					elif x > 0 and img[x-1, y] == 0:
						labels[x, y] = labels[x-1, y]
					# All the neighboring pixels are white,
					# Therefore the current pixel is a new component
					else:
						current_label += 1;
						labels[x, y] = current_label

	#
	# Second pass
	#

	colors = {}

	# Image to display the components in a nice, colorful way
	out_img = np.zeros((height,width,3), np.uint8)

	for x in range(0, height):
		for y in range(0, width):
			component = labels[x, y]
			if component in eq_labels:
				# Update components in image
				labels[x, y] = eq_labels[component]
				component = eq_labels[component]


			if component not in colors:
				if component==0:
					colors[component] = (0,0,0)
				else:
					colors[component] = (random.randint(0,255), random.randint(0,255),random.randint(0,255))

			# Colorize the image
			out_img[x, y] = colors[component]

	return (labels, out_img)
 
def main():
	image = cv2.imread('../prueba.png')
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# Scharr operator
	scharrx = cv2.Scharr(gray,cv2.CV_16S,1,0)
	scharry = cv2.Scharr(gray,cv2.CV_16S,0,1)
	scharr = cv2.convertScaleAbs(cv2.addWeighted(scharrx,0.5,scharry,0.5,0))

	# Blur with average filter
	blurred = cv2.blur(scharr, (5,5))
	
	# Threshold binary
	(_, threshold) = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY)

	# erosions and dilations
	threshold = cv2.erode(threshold, None, iterations = 4)
	threshold = cv2.dilate(threshold, None, iterations = 4)

	plt.subplot(1,1,1),plt.imshow(255-threshold,cmap = 'gray')
	plt.title('Threshold'), plt.xticks([]), plt.yticks([])
	plt.show()

	(labels, out_img) = run(gray)

	plt.subplot(1,1,1),plt.imshow(out_img ,cmap = 'gray')
	plt.title('Resultado'), plt.xticks([]), plt.yticks([])

	plt.show()

if __name__ == "__main__": main()