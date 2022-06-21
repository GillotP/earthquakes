import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
import argparse

MARYLAND_COLORS = np.array([( 68,  79, 137),
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

class EarthMap():

	def __init__(self, path, subsampling_factor=1):
		self.load_data(path, subsampling_factor)

	def load_data(self, path, subsampling_factor):
		self.map = np.fromfile(path, dtype=np.uint8).reshape([21600, 43200])[::subsampling_factor]

	def set_figure(self):
		fig, ax = plt.subplots(1, 1)
		ax.imshow(self.map, aspect="auto", cmap=colors.ListedColormap(MARYLAND_COLORS))
		# ax.set_xticks([])
		# ax.set_yticks([])
		return fig, ax

	def set_frame(self, ax, geo_coordinates, extra_frame_size=10.0):
		border_geo_coordinates = {
								  "N": np.array([max(-90.0, np.min(geo_coordinates["N"]) - extra_frame_size), 
								  				 min(90.0, np.max(geo_coordinates["N"]) + extra_frame_size)]),
								  "E": np.array([max(-180.0, np.min(geo_coordinates["E"]) - extra_frame_size), 
								  				 min(180.0, np.max(geo_coordinates["E"]) + extra_frame_size)])
								 }
		top_bottom, left_right = self.geo_coordinates_2_idxs(border_geo_coordinates)
		ax.set_xlim(left_right)
		ax.set_ylim(top_bottom)

	def geo_coordinates_2_idxs(self, geo_coordinates):
		i = np.floor(((90 - geo_coordinates["N"]) / 180) * (self.map.shape[0] - 1)).astype(int)  # i <==> latitude
		j = np.floor(((180 + geo_coordinates["E"]) / 360) * (self.map.shape[1] - 1)).astype(int) # j <==> longitude
		return i, j

	def predict_land_or_water(self, geo_coordinates, show_predictions=bool(0)):
		i, j = self.geo_coordinates_2_idxs(geo_coordinates)
		water = self.map == 0
		if show_predictions:
			points = np.zeros(shape=self.map.shape, dtype=bool)
			points[i,j] = True
			water_and_points = np.where(points * water)
			land_and_points = np.where(points * ~water)
			fig, ax = self.set_figure()
			self.set_frame(ax, geo_coordinates)
			ax.scatter(water_and_points[1], water_and_points[0], marker="o", c="k", label="Water")
			ax.scatter(land_and_points[1], land_and_points[0], marker="x", c="k", label="Land")
			fig.legend()
			plt.show()
		return i, j, water[i, j]

class EarthquakesRecord():

	def __init__(self, path_earth_map, path_earthquakes_record):
		self.load_data(path_earth_map, path_earthquakes_record)
		
	def load_data(self, path_earth_map, path_earthquakes_record):
		self.earth_map = EarthMap(path=path_earth_map, subsampling_factor=10)
		self.earthquakes = pd.read_csv(path_earthquakes_record, sep=";", header=6, encoding = "ISO-8859-1")

	def predict_land_or_water_earthquakes(self, show_predictions):
		earthquakes_geo_coordinates = {
									   "N": self.earthquakes["Latitudine"].to_numpy(),
									   "E": self.earthquakes["Longitudine"].to_numpy()
									  }
		return self.earth_map.predict_land_or_water(earthquakes_geo_coordinates, show_predictions)

def main(show_predictions):
	earthquakes_record = EarthquakesRecord(path_earth_map="gl-latlong-1km-landcover.bsq", 
										   path_earthquakes_record="events_4.5.txt")
	earthquakes_record.predict_land_or_water_earthquakes(show_predictions)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--show', action=argparse.BooleanOptionalAction, default=False)
	args = parser.parse_args()
	main(show_predictions=args.show)