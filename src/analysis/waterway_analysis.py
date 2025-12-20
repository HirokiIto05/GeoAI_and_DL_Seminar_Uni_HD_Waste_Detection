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

import plotnine as pn


def read_waste_data():
    df_raw = df_raw = gpd.read_file(here("output/density/waste_moran_5_points.gpkg"))
    df = df_raw[df_raw["significant_quadrant"] == "HH"].reset_index(drop=True)
    df = df[df["tile_id"].notna()].reset_index(drop=True)
    df = df.drop_duplicates()

    return df

def read_buffer_waterway():
    df_buffer = gpd.read_file(here("data/intermediate/waterway/buffer_waterway.gpkg"))
    df_buffer['waterway'] = True
    df_buffer = df_buffer.drop_duplicates(subset="geometry")
    df_buffer = df_buffer[['waterway', 'geometry']]

    return df_buffer


def merge_waste_waterway(df, df_buffer):
    df_waste_waterway = df_buffer.sjoin(df, how="left", predicate="contains")
    df_waste_waterway = df.sjoin(df_buffer, how="left", predicate="intersects")

    return df_waste_waterway