import numpy as np
import matplotlib.pyplot as plt

def load_data(path):
	return np.fromfile(path, dtype=np.uint8).reshape([21600, 43200])

def visualize_data(data, block=bool(1)):
	fig, ax = plt.subplots(1, 1)
	ax.imshow(data, aspect="auto")
	ax.set_xticks([])
	ax.set_yticks([])
	plt.show(block=block)

def main():
	data = load_data("./gl-latlong-1km-landcover.bsq")
	visualize_data(data)


if __name__ == '__main__':
	main()