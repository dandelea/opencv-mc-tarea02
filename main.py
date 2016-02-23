from matplotlib import pyplot as plt
import argparse, cv2

def run(image_filename):
	image = cv2.imread(image_filename)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# Scharr operator
	scharrx = cv2.Scharr(gray,cv2.CV_16S,1,0)
	scharry = cv2.Scharr(gray,cv2.CV_16S,0,1)
	scharr = cv2.convertScaleAbs(cv2.addWeighted(scharrx,0.5,scharry,0.5,0))

	# Blur with average filter
	blurred = cv2.blur(scharr, (3,3))
	
	# Threshold binary
	(_, threshold) = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY)

	

	plt.subplot(2,3,1),plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB),cmap = 'gray')
	plt.title('Original'), plt.xticks([]), plt.yticks([])
	plt.subplot(2,3,2),plt.imshow(gray,cmap = 'gray')
	plt.title('Gray'), plt.xticks([]), plt.yticks([])
	plt.subplot(2,3,3),plt.imshow(blurred,cmap = 'gray')
	plt.title('Scharr operation + Blurred'), plt.xticks([]), plt.yticks([])
	plt.subplot(2,3,4),plt.imshow(threshold,cmap = 'gray')
	plt.title('Threshold'), plt.xticks([]), plt.yticks([])

	plt.show()

	return None

if __name__=='__main__':
	argument_parser = argparse.ArgumentParser(description="Detect barcode in image")
	argument_parser.add_argument("-i", "--image", required = True, help = "Relative path to barcode image file")
	args = vars(argument_parser.parse_args())
	run(args["image"])