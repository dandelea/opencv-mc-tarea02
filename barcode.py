import cv2, math
import numpy as np
from matplotlib import pyplot as plt

def rotate_about_center(img, angle, scale=1.):
    w = img.shape[1]
    h = img.shape[0]
    rangle = np.deg2rad(angle)  # angle in radians
    # calculate new image width and height
    nw = (abs(np.sin(rangle)*h) + abs(np.cos(rangle)*w))*scale
    nh = (abs(np.cos(rangle)*h) + abs(np.sin(rangle)*w))*scale
    # get rotation matrix
    rot_mat = cv2.getRotationMatrix2D((nw/2, nh/2), angle, scale)
    # calculate the move from the old center to the new center combined
    # with the rotation
    rot_move = np.dot(rot_mat, np.array([(nw-w)/2, (nh-h)/2,0]))
    # the move only affects the translation, so update the translation
    # part of the transform
    rot_mat[0,2] += rot_move[0]
    rot_mat[1,2] += rot_move[1]
    return cv2.warpAffine(img, rot_mat, (int(math.ceil(nw)), int(math.ceil(nh))))

def run(img_url):
	img = cv2.imread(img_url)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	f = np.fft.fft2(gray) #DFT
	fshift = np.fft.fftshift(f)
	magnitude_spectrum = 20*np.log(np.abs(fshift)) #DFT centered
	magnitude_spectrum = cv2.convertScaleAbs(magnitude_spectrum)

	# threshold on the DFT. Will result on an image with perpendicular lines of the barcode
	_,magnitude_spectrum = cv2.threshold(magnitude_spectrum,220,255,cv2.THRESH_BINARY)

	# Hough algorithm. Get lines coordinates of the DFT
	lines = cv2.HoughLines(magnitude_spectrum, 1, np.pi/180, 10)
	line_img = img.copy()

	for rho,theta in lines[0]:
		angle = math.degrees(theta) - 90

	# rotate
	rotated = rotate_about_center(gray, angle)

	# Scharr operator
	scharrx = cv2.Scharr(rotated,cv2.CV_16S,1,0)
	scharry = cv2.Scharr(rotated,cv2.CV_16S,0,1)
	scharr = cv2.convertScaleAbs(cv2.addWeighted(scharrx,0.5,scharry,0.5,0))

	# Blur with average filter
	blurred = cv2.blur(scharr, (7,7))
	
	# Threshold binary
	(_, threshold) = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY)

	# construct a closing kernel and apply it to the thresholded image
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
	# opening reduces white noise
	closed = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)
	# closing fills empty spaces between lines
	closed = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)

	# erosions and dilations clean the image noises
	closed = cv2.erode(closed, kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7)), iterations = 2)
	closed = cv2.dilate(closed, kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7)), iterations = 2)

	# find the contours in the thresholded image, then sort the contours
	# by their area, keeping only the largest one
	_, cnts, _ = cv2.findContours(closed.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	sorted_comp = max(cnts, key = cv2.contourArea)
 
	# compute the rotated bounding box of the largest contour
	rect = cv2.minAreaRect(sorted_comp)
	box = np.int0(cv2.boxPoints(rect))
 
	# draw a bounding box arounded the detected barcode
	new_image = rotate_about_center(img, angle)
	cv2.drawContours(new_image, [box], -1, (0, 255, 0), 3)

	plt.subplot(2,3,1),plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB),cmap = 'gray')
	plt.title('Original'), plt.xticks([]), plt.yticks([])
	plt.subplot(2,3,2),plt.imshow(rotated,cmap = 'gray')
	plt.title('Rotated'), plt.xticks([]), plt.yticks([])
	plt.subplot(2,3,3),plt.imshow(blurred,cmap = 'gray')
	plt.title('Scharr operation + Blurred'), plt.xticks([]), plt.yticks([])
	plt.subplot(2,3,4),plt.imshow(threshold,cmap = 'gray')
	plt.title('Threshold'), plt.xticks([]), plt.yticks([])
	plt.subplot(2,3,5),plt.imshow(closed,cmap = 'gray')
	plt.title('Closed'), plt.xticks([]), plt.yticks([])
	plt.subplot(2,3,6),plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB),cmap = 'gray')
	plt.title('New image'), plt.xticks([]), plt.yticks([])


	plt.show()

	return None