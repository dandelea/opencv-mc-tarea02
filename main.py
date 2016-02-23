from matplotlib import pyplot as plt
import argparse, cv2
import numpy as np

def run(image_filename):
	image = cv2.imread(image_filename)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# Scharr operator
	scharrx = cv2.Scharr(gray,cv2.CV_16S,1,0)
	scharry = cv2.Scharr(gray,cv2.CV_16S,0,1)
	scharr = cv2.convertScaleAbs(cv2.addWeighted(scharrx,0.5,scharry,0.5,0))

	# Blur with average filter
	blurred = cv2.blur(scharr, (5,5))
	
	# Threshold binary
	(_, threshold) = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY)

	# construct a closing kernel and apply it to the thresholded image
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
	closed = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)

	# erosions and dilatations
	closed = cv2.erode(closed, None, iterations = 4)
	closed = cv2.dilate(closed, None, iterations = 4)

	# find the contours in the thresholded image, then sort the contours
	# by their area, keeping only the largest one
	_, cnts, _ = cv2.findContours(closed.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	sorted_comp = max(cnts, key = cv2.contourArea)
 
	# compute the rotated bounding box of the largest contour
	rect = cv2.minAreaRect(sorted_comp)
	box = np.int0(cv2.boxPoints(rect))
 
	# draw a bounding box arounded the detected barcode and display the
	# image
	new_image = cv2.drawContours(image.copy(), [box], -1, (0, 255, 0), 3)

	closed_copy = closed.copy()
	ret, markers = cv2.connectedComponents(closed_copy, connectivity=4)
	markers += 1

	plt.subplot(2,3,1),plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB),cmap = 'gray')
	plt.title('Original'), plt.xticks([]), plt.yticks([])
	plt.subplot(2,3,2),plt.imshow(gray,cmap = 'gray')
	plt.title('Gray'), plt.xticks([]), plt.yticks([])
	plt.subplot(2,3,3),plt.imshow(blurred,cmap = 'gray')
	plt.title('Scharr operation + Blurred'), plt.xticks([]), plt.yticks([])
	plt.subplot(2,3,4),plt.imshow(threshold,cmap = 'gray')
	plt.title('Threshold'), plt.xticks([]), plt.yticks([])
	plt.subplot(2,3,5),plt.imshow(closed,cmap = 'gray')
	plt.title('Closed'), plt.xticks([]), plt.yticks([])
	plt.subplot(2,3,6),plt.imshow(markers,cmap = 'gray')
	plt.title('New image'), plt.xticks([]), plt.yticks([])


	plt.show()

	return None

if __name__=='__main__':
	argument_parser = argparse.ArgumentParser(description="Detect barcode in image")
	argument_parser.add_argument("-i", "--image", required = True, help = "Relative path to barcode image file")
	args = vars(argument_parser.parse_args())
	run(args["image"])