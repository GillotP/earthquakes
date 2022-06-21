import numpy as np
import pandas as pd

def load_data(path):
	return np.fromfile(path, dtype=np.uint8).reshape([43200, 21600])

def main():
	data = load_data("./gl-latlong-1km-landcover.bsq")

	# subset = data[::50]
	print(data)
	print(data.shape)

if __name__ == '__main__':
	main()