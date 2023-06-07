import os
from src import Model

dir_path = os.path.dirname(os.path.realpath(__file__))
relative_input_path = "../data/input"
input_path = os.path.join(dir_path, relative_input_path)
time_series_path = os.path.join(input_path, "hcp_time_series.mat")
mni_coords_path = os.path.join(input_path, "Lausanne_463_MNI_coords.node")

m = Model(time_series_path, mni_coords_path)

m.load()
m.select_rois(1)
m.fit()
m.synthesize()
m.save()

