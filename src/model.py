from dit import Distribution
from scipy.io import loadmat
import pickle
import os
import random
import string
import pathlib
import statsmodels.api as sm
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import binarize


class Model:
    def __init__(self,
                 time_series_path,
                 mni_coords_path,
                 num_rois=6,
                 model_type=sm.tsa.DynamicFactor,
                 maxiter=500,
                 num_sims=10000000,
                 output_path='../data/output'):
        self.time_series_path = time_series_path
        self.mni_coords_path = mni_coords_path
        self.num_rois = num_rois
        self.model_type = model_type
        self.num_sims = num_sims
        self.maxiter = maxiter
        self.output_path = output_path
        self.time_series = None
        self.mni_coords = None
        self.fitted_model = None
        self.roi_idxs = None
        self.dist = None

    def load(self):
        self.time_series = loadmat(self.time_series_path)['X']
        self.mni_coords = pd.read_csv(self.mni_coords_path,
                                      sep='\t',
                                      header=None)

    def select_rois(self, network):
        df = (self.mni_coords[3] == network)
        idxs = self.mni_coords[3][df].index
        self.roi_idxs = random.sample(list(idxs), k=self.num_rois)

    def fit(self):
        x = np.take(self.time_series, self.roi_idxs, 0)
        x_norm = (x - x.mean()) / x.std()
        mdl = self.model_type(x_norm.T,
                              k_factors=1,
                              factor_order=4,
                              error_order=1)
        self.fitted_model = mdl.fit(maxiter=self.maxiter)

    def synthesize(self):
        z = self.fitted_model.simulate(self.num_sims)

        # binarize
        z = binarize(z)

        df = pd.DataFrame(z, dtype='int')
        groups = df.groupby(list(range(self.num_rois))).groups

        probs = {}
        for g in groups:
            probs[g] = groups[g].size / self.num_sims

        self.dist = Distribution(probs)

    def save(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        output_path = os.path.join(dir_path, self.output_path)
        now = datetime.now()
        path = os.path.join(output_path, now.strftime("%Y%m%dT%H%M%S"))
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        letters = string.ascii_lowercase
        filename = ''.join(random.choice(letters) for _ in range(10))
        file_handle = open(f'{path}/{filename}.obj', 'wb')
        pickle.dump(self.dist, file_handle)
