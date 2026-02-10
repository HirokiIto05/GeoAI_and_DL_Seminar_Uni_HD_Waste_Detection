import os
import csv
import pandas as pd
import numpy as np
from pyprojroot import here
import geopandas as gpd
from libpysal.weights import Queen
from esda.moran import Moran
from esda.moran import Moran_Local
import libpysal
from libpysal.weights import Queen
from libpysal import io

from pysal.lib import weights  # Spatial weights

from splot.esda import moran_scatterplot
from plotnine import *


def read_data(grid_size):
    if grid_size == 5:  
        df = gpd.read_file(here("data/intermediate/predicted_tiles/results_all_tiles_97.gpkg"))

        df_waste = df.copy()
        dict_mapping = {"waste": 1, "non_waste": 0}
        df_waste["density"] = df_waste["label"].map(dict_mapping)
        df_waste = df_waste.dropna(subset=["density", "geometry"]).reset_index(drop=True)
        df_waste["density"].value_counts()
    elif grid_size == 20:
        df = gpd.read_file(here("data/intermediate/density/waste_density_20.gpkg"))

        df_waste = df.copy()
        df_waste = df_waste.dropna(subset=["density", "geometry"]).reset_index(drop=True)
        df_waste["density"].value_counts()
    
    return df_waste


def calculate_weights(df):
    # Create spatial weights matrix
    w = Queen.from_dataframe(df, silence_warnings=True)
    w.transform = "r"
    return w


def calculate_global_moran(df, w):
    y = df["density"].values
    np.random.seed(111)
    mi = Moran(y, w)
    return mi


def summary_moran(mi, label=""):
    print(f"Moran’s I {label}: {mi.I:.5f}")
    print(f"Expected I: {mi.EI:.5f}")
    print(f"Z-score: {mi.z_sim:.3f}")
    print(f"P-value (permutation): {mi.p_sim:.6f}")


def calculate_local_moran(df, w):
    y = df["density"].values
    lisa = Moran_Local(y, w, permutations=99, n_jobs=1)
    return lisa


def add_moral_local_results(df, lisa):
    df["local_I"] = lisa.Is          # Local Moran's I value
    df["p_value"] = lisa.p_sim      # Permutation p-value
    df["quadrant"] = lisa.q         # Cluster type (1–4)

    df["significant"] = df["p_value"] < 0.05
    df["quadrant"] = df["quadrant"].map({1: "HH", 2: "LH", 3: "LL", 4: "HL"})
    df["significant_quadrant"] = df["quadrant"].where(df["significant"], np.nan)

    df['density_significant'] = np.nan
    df.loc[df['significant_quadrant'] == 'HH', 'density_significant'] = df['density']
    

    return df