from matplotlib import pyplot as plt
import numpy as np
import cv2, morphology, connected_components, transform, barcode, math

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
	sudoku_filename = 'sudoku.jpg'
	barcode_filename = 'barcode6.jpg'

	while(True):
		print("\n")
		print('Tarea 02 de MC - BARCODE POSTPROCESSING')
		print('1. Morphology')
		print('2. Connected component detection')
		print('3. Transformations')
		print('4. Barcode processing')
		print('5. exit')
		option = input('Select option [1 - 5]: ')

		if valid_input(option)==1:
			option = int(option)
			if option > 0 and option < 6:
				if option==1:
					print('\n')
					print('1. Erosion')
					print('2. Dilation')
					print('3. Opening')
					print('4. Closure')
					print('5. Compare all')
					print('6. back')
					method = input('Select method [1 - 6]: ')

					if valid_input(method)==1:
						method = int(method)
						if method > 0 and method < 7:
							if method==1:
								
								print("\n")
								factor = input('Write erosion factor (default=2): ')
								if factor=="":
									morphology.erosion(d_filename)
								else:
									if valid_input(factor):
										factor = int(factor)
										morphology.erosion(d_filename, factor)

							elif method==2:
								
								print("\n")
								factor = input('Write dilation factor (default=2): ')
								if factor=="":
									morphology.dilation(d_filename)
								else:
									if valid_input(factor):
										factor = int(factor)
										morphology.dilation(d_filename, factor)

							elif method==3:
								morphology.opening(d_noise_filename)
							elif method==4:
								morphology.closing(d_dotted_filename)
							elif method==5:

								print("\n")
								factor = input('Write erosion/dilation factor (default=2): ')
								if factor=="":
									morphology.compare(d_filename)
								else:
									if valid_input(factor):
										factor = int(factor)
										morphology.compare(d_filename, factor)
						else:
							print('No valid input');


				elif option==2:
					print('\n')
					print('1. 4-neighbour')
					print('2. 8-neigbour')
					print('3. Compare all')
					print('4. back')
					method = input('Select method [1-4]: ')

					if method=="":
						connected_components.compare(figures_filename)
					else:
						if valid_input(method)==1:
							method = int(method)
							if method>0 and method<5:
								if method==3:
									connected_components.compare(figures_filename)
								elif method==4:
									pass
								else:
									method=method*4
									connected_components.connected_components(figures_filename, method)
							else:
								print('No valid input');
				elif option==3:
					print('\n')
					print('1. Hough lines')
					print('2. Fourier')
					print('3. back')
					method = input('Select operation [1-3]: ')

					if valid_input(method)==1:
						method = int(method)
						if method>0 and method<4:
							if method==1:
								print("\n")
								factor = input('Write min votes of lines (default=200): ')
								if factor=="":
									transform.hough(sudoku_filename)
								else:
									if valid_input(factor):
										factor = int(factor)
										transform.hough(sudoku_filename, factor)
							elif method==2:
								transform.fourier(barcode_filename)
						else:
							print('No valid input');
				elif option==4:
					method = input('Select barcode available [1-6]: ')
					if valid_input(method)==1 and int(method)>0 and int(method)<7:
						barcode.run('barcode'+method+'.jpg')
					else:
						print('No valid input');
				elif option==5:
					break;
			else:
				print('No valid input');

if __name__=='__main__':
	main()