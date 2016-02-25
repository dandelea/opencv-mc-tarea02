from matplotlib import pyplot as plt
import argparse, cv2
import numpy as np
import morphology, connected_components

def valid_input(input):
	try:
		i = int(input)
		valid = 1;
	except ValueError:
		print('Not valid input');
		valid = 0;
	return valid;

def main():
	d_filename = 'd.jpg'
	d_dotted_filename = 'd_dotted.jpg'
	d_noise_filename = 'd_noise.jpg'
	figures_filename = 'figures.png'

	while(True):
		print("\n")
		print('Tarea 02 de MC - BARCODE POSTPROCESSING')
		print('1. Morphology')
		print('2. Connected component detection')
		print('3. Inclination detection')
		print('4. exit')
		option = input('Select option [1 - 4]: ')

		if valid_input(option)==1:
			option = int(option)
			if option > 0 and option < 7:
				if option==1:
					print('\n')
					print('1. Erosion')
					print('2. Dilation')
					print('3. Opening')
					print('4. Closure')
					print('5. back')
					method = input('Select method [1 - 5]: ')

					if valid_input(method)==1:
						method = int(method)
						if method > 0 and method < 6:
							if method==1:
								
								print("\n")
								factor = input('Write erosion factor (default=2): ')
								if factor=="":
									factor = 2
									morphology.erosion(d_filename, factor)
								else:
									if valid_input(factor):
										factor = int(factor)
										morphology.erosion(d_filename, factor)

							elif method==2:
								
								print("\n")
								factor = input('Write dilation factor (default=2): ')
								if factor=="":
									factor = 2
									morphology.dilation(d_filename, factor)
								else:
									if valid_input(factor):
										factor = int(factor)
										morphology.dilation(d_filename, factor)

							elif method==3:
								morphology.opening(d_noise_filename)
							elif method==4:
								morphology.closing(d_dotted_filename)
						else:
							print('No valid input');


				elif option==2:
					print('\n')
					print('1. 4-neighbour')
					print('2. 8-neigbour')
					print('3. Compare all')
					method = input('Select method (Default=2): ')

					if method=="":
						connected_components.connected_components(figures_filename, 8)
					else:
						if valid_input(method)==1:
							method = int(method)
							if method>0 and method<4:
								if method==3:
									connected_components.compare(figures_filename)
								else:
									method=method*4
									connected_components.connected_components(figures_filename, method)
				elif option==3:
					print('\n')
				elif option==4:
					break;
			else:
				print('No valid input');



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

	# erosions and dilations
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
	#argument_parser = argparse.ArgumentParser(description="Detect barcode in image")
	#argument_parser.add_argument("-i", "--image", required = True, help = "Relative path to barcode image file")
	#args = vars(argument_parser.parse_args())
	#run(args["image"])
	main()