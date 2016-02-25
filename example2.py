import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('barcode2_gir.jpg')
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img = cv2.GaussianBlur(img,(3,3), 0)
# Otsu's thresholding


f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)
magnitude_spectrum = 20*np.log(np.abs(fshift))
magnitude_spectrum = cv2.convertScaleAbs(magnitude_spectrum)
#print(np.where(magnitude_spectrum>255))

_,magnitude_spectrum = cv2.threshold(magnitude_spectrum,220,255,cv2.THRESH_BINARY)

lines = cv2.HoughLines(magnitude_spectrum, 1, np.pi/180, 10)
for rho, theta in lines[0]:
	a = np.cos(theta)
	b = np.sin(theta)
	x0 = a*rho
	y0 = b*rho
	x1 = int(x0 + 1000*(-b))
	y1 = int(y0 + 1000*(a))
	x2 = int(x0 - 1000*(-b))
	y2 = int(y0 - 1000*(a))
	line_img = img.copy()
	cv2.line(line_img,(x1,y1),(x2,y2),(0,0,255),2)

plt.subplot(221),plt.imshow(img, cmap = 'gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(222),plt.imshow(magnitude_spectrum, cmap = 'gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.subplot(223),plt.imshow(line_img, cmap = 'gray')
plt.title('Lines'), plt.xticks([]), plt.yticks([])
plt.show()