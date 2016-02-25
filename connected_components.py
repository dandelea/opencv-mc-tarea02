import numpy as np
import random
import cv2
from matplotlib import pyplot as plt

## Connected components algorithms

def connected_components (img_url, n=8):
	img = cv2.imread(img_url, 0)
	if n==4:
		_, img4 = connected_components_4neighbours(img)
		plt.subplot(1,2,1),plt.imshow(img ,cmap = 'gray')
		plt.title('Original'), plt.xticks([]), plt.yticks([])
		plt.subplot(1,2,2),plt.imshow(img4 ,cmap = 'gray')
		plt.title('CompConex 4Vecindad'), plt.xticks([]), plt.yticks([])
		plt.show()
	elif n==8:
		_, img8 = connected_components_8neighbours(img)
		plt.subplot(1,2,1),plt.imshow(img ,cmap = 'gray')
		plt.title('Original'), plt.xticks([]), plt.yticks([])
		plt.subplot(1,2,2),plt.imshow(img8 ,cmap = 'gray')
		plt.title('CompConex 8Vecindad'), plt.xticks([]), plt.yticks([])
		plt.show()
	else:
		raise NotImplementedError

def compare(img_url):
	img = cv2.imread(img_url, 0)
	_, img4 = connected_components_4neighbours(img)
	_, img8 = connected_components_8neighbours(img)

	plt.subplot(2,2,1),plt.imshow(img ,cmap = 'gray')
	plt.title('Original'), plt.xticks([]), plt.yticks([])
	plt.subplot(2,2,2),plt.imshow(img4 ,cmap = 'gray')
	plt.title('CompConex 4Vecindad'), plt.xticks([]), plt.yticks([])
	plt.subplot(2,2,3),plt.imshow(img8 ,cmap = 'gray')
	plt.title('CompConex 8Vecindad'), plt.xticks([]), plt.yticks([])
	plt.show()

def connected_components_4neighbours(img):
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
			#	   y ->
			#    -------------
			#  x |   | a |   |
			#  | -------------
			#  v | b | c |   |
			#    -------------
			#    |   |   |   |
			#    -------------
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
				if x > 0 and img[x-1, y] == 0 and y > 0 and img[x, y-1] == 0:
					labels[x, y] = labels[x, y-1]
					# If component of a and b are not the same
					# 	 Store a reference a->b
					if labels[x-1, y] != labels[x, y-1]:
						eq_labels[max(labels[x, y-1], labels[x-1, y])] = min(labels[x, y-1], labels[x-1, y])

				else:

					# If pixel a is in the image and black:
					#    b and c are its neighbors, so they are all part of the same component
					#    Therefore, there is no reason to check their labels
					#    so simply assign a's label to c
					if x > 0 and img[x-1, y] == 0:
						labels[x, y] = labels[x-1, y]
					# If pixel b is in the image and black
					#    We already know a is white
					#    so simpy assign b's label to c
					elif y> 0 and img[x, y-1] == 0:
						labels[x, y] = labels[x, y-1]
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

def connected_components_8neighbours(img):
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
			#	   y -> 
			#    -------------
			#  x | a | b | c |
			#  | -------------
			#  v | d | e |   |
			#    -------------
			#    |   |   |   |
			#    -------------
			#
			# The current pixel is e
			# a, b, c and d are its neighbors of interest
			#
			# 255 is white, 0 is black
			# White pixels part of the background, so they are ignored
			# If a pixel lies outside the bounds of the image, it default to white
			#

			# Neighbours list
			neighbours = []

			# If the current pixel is white, it's obviously not a component...
			if img[x, y] == 255:
				pass

			else:

				# If pixel a is in the image and black
				# 	Add pixel a to neighbours
				if x>0 and y>0 and img[x-1,y-1]==0:
						neighbours.append((x-1, y-1))
				# If pixel b is in the image and black
				# 	Add pixel a to neighbours
				if x>0 and img[x-1,y]==0:
						neighbours.append((x-1,y))
				# If pixel c is in the image and black
				# 	Add pixel a to neighbours
				if x>0 and y<width-1 and img[x-1, y+1]==0:
						neighbours.append((x-1, y+1))
				# If pixel d is in the image and black
				# 	Add pixel a to neighbours
				if y>0 and img[x,y-1]==0:
						neighbours.append((x,y-1))

				if len(neighbours)==0:
					current_label += 1
					labels[x,y] = current_label
				else:
					neighbours_labels = list(set([labels[n[0], n[1]] for n in neighbours]))
					labels[x,y] = min(neighbours_labels)

					for nl in neighbours_labels:
						if nl != labels[x,y]:
							eq_labels[nl] = labels[x,y]
							
							


	#
	# Second pass
	#
	colors = {}
	# Image to display the components in a nice, colorful way
	out_img = np.zeros((height,width,3), np.uint8)

	for x in range(0, height):
		for y in range(0, width):
			component = labels[x, y]

			while component in eq_labels:
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