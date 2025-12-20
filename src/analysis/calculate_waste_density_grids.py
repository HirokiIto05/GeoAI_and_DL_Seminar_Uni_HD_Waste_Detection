# ------------------------------------------------------------
# calculate_waste_density_grids.py
#
# This script calculates waste density statistics for spatial grids
# by merging grid geometries with predicted tile features, and
# prepares data for spatial autocorrelation and further analysis.
#
# ------------------------------------------------------------


import os
import csv
import pandas as pd
from pyprojroot import here
import geopandas as gpd

import rasterio
from rasterstats import zonal_stats
import statsmodels.api as sm

import json
from shapely.geometry import shape
import plotnine as pn


# Functions

# read grid features 
def read_grid_data(gird_size):
  
    if gird_size == 10:
        grid = gpd.read_file(here("data/raw/grid/moran_10.gpkg"))
    elif gird_size == 20:
        grid = gpd.read_file(here("data/raw/grid/moran_20.gpkg"))
    elif gird_size == 30:
        grid = gpd.read_file(here("data/raw/grid/moran_30.gpkg"))
    elif gird_size == 40:
        grid = gpd.read_file(here("data/raw/grid/moran_40.gpkg"))
    elif gird_size == 50:
        grid = gpd.read_file(here("data/raw/grid/moran_50.gpkg"))
    else:
        raise ValueError("Unsupported grid size")
    return grid


def read_features():
  # features is centroided points of tiles with prediction results
  features = gpd.read_file(here("data/predicted_tiles/results_all_tiles_points.gpkg"))
  features = features[features["label"].notna()].reset_index(drop=True)
  return features

def merge_grid_with_features(grid, features):    
  # merge the grid with features
  df = grid.sjoin(features, how="left", predicate="contains")
  df = df[df['tile_id'].notna()]
  df.sort_values(by=["id"])

  return df


def count_waste_non_waste(df_points):
    # count waste and non_waste per XXm grid
    df_count = df_points.groupby(["id", "label"]).aggregate({"tile_id": "count"}).reset_index()
    df_count.sort_values(by=["id"])
    df_count = df_count[(df_count['label'] == 'waste') | (df_count['label'] == 'non_waste')]

    df_count["id"] = df_count["id"].astype(int)
    df_count["label"] = df_count["label"].astype(str)

    return df_count

# count waste and non_waste per XXm gri



def generate_waste_non_waste_df(df_count):
    
    # pivot the count data to have waste and non_waste columns
    df_waste = (
        df_count[df_count["label"] == "waste"]
        .rename(columns={"tile_id": "waste"})
        .drop(columns=["label"])
    )

    df_non_waste = (
        df_count[df_count["label"] == "non_waste"]
        .rename(columns={"tile_id": "non_waste"})
        .drop(columns=["label"])
    )

    df_count_pivot = (
        df_non_waste
        .merge(df_waste, on="id", how="outer")
    )

    # NA → 0
    df_count_pivot["waste"] = df_count_pivot["waste"].fillna(0)
    df_count_pivot["non_waste"] = df_count_pivot["non_waste"].fillna(0)

    # density = waste / (waste + non_waste)
    df_count_pivot["density"] = df_count_pivot["waste"] / (df_count_pivot["waste"] + df_count_pivot["non_waste"])

    return df_count_pivot


def wrap_calculate_waste_density_grids(grid):
    # merge geometry with count data
    features = read_features()
    df = merge_grid_with_features(grid, features)

    df_geometry = df[["id", "geometry"]]
    df_points = df.drop(columns="geometry")

    df_count = count_waste_non_waste(df_points)
    df_count_pivot = generate_waste_non_waste_df(df_count)
    
    df_output = df_geometry.merge(df_count_pivot, on="id", how="left")

    return df_output
