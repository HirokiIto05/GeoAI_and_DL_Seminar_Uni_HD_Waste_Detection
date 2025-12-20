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

import plotnine as pn

def read_data(grid_size):
    if grid_size == 5:  
        df = gpd.read_file(here("data/predicted_tiles/results_all_tiles_97.gpkg"))

        df_waste = df.copy()
        dict_mapping = {"waste": 1, "non_waste": 0}
        df_waste["density"] = df_waste["label"].map(dict_mapping)
        df_waste = df_waste.dropna(subset=["density", "geometry"]).reset_index(drop=True)
        df_waste["density"].value_counts()
    elif grid_size != 5:
        df = gpd.read_file(here(f"data/density/waste_density_{grid_size}.gpkg"))

        df_waste = df.copy()
        df_waste = df_waste.dropna(subset=["density", "geometry"]).reset_index(drop=True)
        df_waste["density"].value_counts()
    
    return df


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

def summary_moran(mi, grid_size_i):
    
    df = pd.DataFrame({
        "moran_I": [mi.I],
        "p_value": [mi.p_sim]
    })

    df["grid_resolution"] = grid_size_i

    df["moran_I"] = df["moran_I"].round(5)
    df["p_value"] = df["p_value"].round(6)

    return df

def plot_morans_I(df_moran_summary):

    p = (
        pn.ggplot(df_moran_summary, pn.aes(x="grid_resolution", y="moran_I"))
        + pn.geom_bar(stat="identity")
        + pn.labs(
            x="Grid resolution (m)",
            y="Global Moran’s I"
        )
        + pn.theme_bw() 
        + pn.theme(
          axis_text=pn.element_text(size=13),
          axis_title=pn.element_text(size=15),
        )
        + pn.scale_x_discrete(limits=["5", "10", "20", "30", "40"])
        + pn.scale_y_continuous(limits=[0, 0.55])
    )

    return p

