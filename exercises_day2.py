import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

def set_maryland_colormap():
	maryland_colors = np.array([( 68,  79, 137),
								(  1, 100,   0),
								(  1, 130,   0),
								(151, 191,  71),
								(  2, 220,   0),
								(  0, 255,   0),
								(146, 174,  47),
								(220, 206,   0),
								(255, 173,   0),
								(255, 251, 195),
								(140,  72,   9),
								(247, 165, 255),
								(255, 199, 174),
								(  0, 255, 255),]) / 255
	return colors.ListedColormap(maryland_colors)

def load_data(path):
	return np.fromfile(path, dtype=np.uint8).reshape([21600, 43200])

def visualize_data(data, subsample=1, block=bool(1)):
	assert type(subsample) == int
	fig, ax = plt.subplots(1, 1)
	ax.imshow(data[::subsample], aspect="auto", cmap=set_maryland_colormap())
	ax.set_xticks([])
	ax.set_yticks([])
	plt.show(block=block)

def main():
	data = load_data("./gl-latlong-1km-landcover.bsq")
	visualize_data(data, subsample=50)

if __name__ == '__main__':
	main()