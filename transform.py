import cv2
import numpy as np
from matplotlib import pyplot as plt

## Transformations: Hough lines, Fourier

def hough(img_url, votes=200):
	img = cv2.imread(img_url)
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray,50,150,apertureSize = 3)
	img_lines = img.copy()

	lines = cv2.HoughLines(edges,1,np.pi/180,votes)
	for line in lines:
		for rho,theta in line:
			a = np.cos(theta)
			b = np.sin(theta)
			x0 = a*rho
			y0 = b*rho
			x1 = int(x0 + 1000*(-b))
			y1 = int(y0 + 1000*(a))
			x2 = int(x0 - 1000*(-b))
			y2 = int(y0 - 1000*(a))

			cv2.line(img_lines,(x1,y1),(x2,y2),(0,0,255),2)

	plt.subplot(1,2,1),plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB),cmap = 'gray')
	plt.title('Original'), plt.xticks([]), plt.yticks([])
	plt.subplot(1,2,2),plt.imshow(cv2.cvtColor(img_lines, cv2.COLOR_BGR2RGB),cmap = 'gray')
	plt.title('Lines detected\n(Votes: '+str(votes)+")"), plt.xticks([]), plt.yticks([])

	plt.show()

def fourier(img_url):
	img = cv2.imread(img_url)
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray,(3,3), 0)

	f = np.fft.fft2(gray)
	fshift = np.fft.fftshift(f)
	magnitude_spectrum = 20*np.log(np.abs(fshift))
	magnitude_spectrum = cv2.convertScaleAbs(magnitude_spectrum)

	_,magnitude_spectrum = cv2.threshold(magnitude_spectrum,220,255,cv2.THRESH_BINARY)

	plt.subplot(121),plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), cmap = 'gray')
	plt.title('Input Image'), plt.xticks([]), plt.yticks([])
	plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
	plt.title('DFT centered to (0,0)'), plt.xticks([]), plt.yticks([])

	plt.show()