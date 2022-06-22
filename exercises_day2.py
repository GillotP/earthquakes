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

	def set_frame(self, ax, geo_coordinates, extra_frame_size=10.0, num_ticks=4):
		border_geo_coordinates = {
								  "N": np.array([max(-90.0, np.min(geo_coordinates["N"]) - extra_frame_size), 
								  				 min(90.0, np.max(geo_coordinates["N"]) + extra_frame_size)]),
								  "E": np.array([max(-180.0, np.min(geo_coordinates["E"]) - extra_frame_size), 
								  				 min(180.0, np.max(geo_coordinates["E"]) + extra_frame_size)])
								 }
		top_bottom, left_right = self.geo_coordinates_2_idxs(border_geo_coordinates)
		ax.set_xlim(left_right)
		ax.set_ylim(top_bottom)
		xticks = np.linspace(left_right[0], left_right[1], num_ticks)
		yticks = np.linspace(top_bottom[1], top_bottom[0], num_ticks)
		ax.set_xticks(xticks)
		ax.set_yticks(yticks)
		geo_coordinates_ticks = self.idxs_2_geo_coordinates(i=yticks, j=xticks)
		ax.set_xticklabels(np.round(geo_coordinates_ticks["E"], 2))
		ax.set_yticklabels(np.round(geo_coordinates_ticks["N"], 2))

	def geo_coordinates_2_idxs(self, geo_coordinates):
		i = np.round((90 - geo_coordinates["N"]) * ((self.map.shape[0] - 1) / 180)).astype(int)  # i <==> latitude
		j = np.round((180 + geo_coordinates["E"]) * ((self.map.shape[1] - 1) / 360)).astype(int) # j <==> longitude
		# Safeguard:
		i = np.minimum(np.maximum(i, 0), self.map.shape[0] - 1)
		j = np.minimum(np.maximum(j, 0), self.map.shape[1] - 1)
		return i, j

	def idxs_2_geo_coordinates(self, i, j):
		geo_coordinates = {
						   "N": -(i / ((self.map.shape[0] - 1) / 180) - 90.0),
						   "E": (j / ((self.map.shape[1] - 1) / 360) - 180.0)
						  }
		# Safeguard:
		geo_coordinates["N"] = np.minimum(np.maximum(geo_coordinates["N"], -90.0), 90.0)
		geo_coordinates["E"] = np.minimum(np.maximum(geo_coordinates["E"], -180.0), 180.0)
		return geo_coordinates

	def predict_land_or_water(self, geo_coordinates, show_predictions=bool(0)):
		i, j = self.geo_coordinates_2_idxs(geo_coordinates)
		water = self.map == 0
		water_predictions = water[i, j]
		if show_predictions:
			fig, ax = plt.subplots(1, 1)
			self.set_frame(ax, geo_coordinates)
			ax.imshow(self.map, aspect="auto", cmap=colors.ListedColormap(MARYLAND_COLORS))
			ax.scatter(j[water_predictions], i[water_predictions], marker="o", c="k", label="Water")
			ax.scatter(j[~water_predictions], i[~water_predictions], marker="x", c="k", label="Land")
			ax.set_xlabel("Longitude")
			ax.set_ylabel("Latitude")
			ax.legend(loc="best")
			plt.show()
		return i, j, water_predictions

class EarthquakesRecord():

	def __init__(self, path_earth_map, path_earthquakes_record, subsampling_factor=1):
		self.load_data(path_earth_map, path_earthquakes_record, subsampling_factor)
		
	def load_data(self, path_earth_map, path_earthquakes_record, subsampling_factor):
		self.earth_map = EarthMap(path_earth_map, subsampling_factor)
		self.earthquakes = pd.read_csv(path_earthquakes_record, sep=";", header=6, encoding = "ISO-8859-1")

	def predict_land_or_water_earthquakes(self, show_predictions):
		earthquakes_geo_coordinates = {
									   "N": self.earthquakes["Latitudine"].to_numpy(),
									   "E": self.earthquakes["Longitudine"].to_numpy()
									  }
		return self.earth_map.predict_land_or_water(earthquakes_geo_coordinates, show_predictions)

def main(show_predictions, subsampling_factor):
	earthquakes_record = EarthquakesRecord(path_earth_map="gl-latlong-1km-landcover.bsq", 
										   path_earthquakes_record="events_4.5.txt",
										   subsampling_factor=subsampling_factor)
	earthquakes_record.predict_land_or_water_earthquakes(show_predictions)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--show', action=argparse.BooleanOptionalAction, default=False)
	parser.add_argument('--subsample', type=int, default=1)
	args = parser.parse_args()
	main(show_predictions=args.show, subsampling_factor=args.subsample)