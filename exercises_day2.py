import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors

class EarthMap():

	def __init__(self, path):
		self.load_data(path)

	def set_maryland_colormap(self):
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

	def load_data(self, path):
		self.map = np.fromfile(path, dtype=np.uint8).reshape([21600, 43200])

	def set_map_visualization(self, subsample=1):
		assert type(subsample) == int
		fig, ax = plt.subplots(1, 1)
		ax.imshow(self.map[::subsample], aspect="auto", cmap=self.set_maryland_colormap())
		ax.set_xticks([])
		ax.set_yticks([])
		return fig, ax

	def visualize_data(self, block=bool(1)):
		plt.show(block=block)


	def run(self):
		self.visualize_data(subsample=50)

	def predict_land_or_water(self, geographic_coordinates, show_predictions=bool(0)):
		i = np.floor(((90 - geographic_coordinates["N"]) / 180) * (self.map.shape[0] - 1)).astype(int)
		j = np.floor(((180 + geographic_coordinates["E"]) / 360) * (self.map.shape[1] - 1)).astype(int)
		water = self.map == 0
		if show_predictions:
			points = np.zeros(shape=self.map.shape, dtype=bool)
			points[i,j] = True
			water_and_points = np.where(points * water)
			land_and_points = np.where(points * ~water)
			fig, ax = self.set_map_visualization()
			ax.scatter(water_and_points[1], water_and_points[0], marker="o", c="k", label="Water")
			ax.scatter(land_and_points[1], land_and_points[0], marker="x", c="k", label="Land")
			fig.legend()
			self.visualize_data()
		return water[i, j]


class EarthquakesRecord():

	def __init__(self, path):
		self.load_data(path)

	def load_data(self, path):
		self.earthquakes = pd.read_csv(path, sep=";", header=6, encoding = "ISO-8859-1")

def main(task):

	earth_map = EarthMap(path="./gl-latlong-1km-landcover.bsq")
	#earth_map.visualize_data(subsample=50)
	geographic_coordinates = {}
	geographic_coordinates["N"] = 180 * np.random.rand(10) - 90
	geographic_coordinates["E"] = 360 * np.random.rand(10) - 180
	preds = earth_map.predict_land_or_water(geographic_coordinates, True)
	print(preds)
	exit()

	earthquakes_record = EarthquakesRecord(path="events_4.5.txt")
	print(earthquakes_record.earthquakes)


	#tasks[task].run()

if __name__ == '__main__':
	main(task=2)