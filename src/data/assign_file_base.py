# ------------------------------------------------------------
# assign_file_base.py
#
# This script prepares base train/validation/test splits for geospatial tile data.
# It deletes old split files, reads the merged point data, splits the data into
# train/val/test sets (20% test, 10% val of remaining, rest train), and copies
# the corresponding tile images into the appropriate folders for each class.
# ------------------------------------------------------------


from pathlib import Path
import shutil
import random

import geopandas as gpd
import pandas as pd
import numpy as np

from pyprojroot.here import here

import os
import csv


def delete_all_files_in_base():
    """
    Delete all files in the base train/val/test folders for both waste and non_waste classes.
    """
    folder_base_path = "data/raw/"

    for category_i in ["train", "val", "test"]:
        for folder_name_i in ["waste", "non_waste"]:
            # Determine the correct folder path for each split
            if category_i in ["train", "val"]:
                folder_path = folder_base_path + "images" + "/" + "base" + "/" + category_i + "/" + folder_name_i
            else:
                folder_path = folder_base_path + "images_test" + "/" + "base" + "/" + category_i + "/" + folder_name_i
            # Delete all files in the folder
            for file_path in Path(here(folder_path)).iterdir():
                print(file_path)
                if os.path.isfile(file_path):
                    os.remove(file_path)

delete_all_files_in_base()


def generate_tiles_for_base(df, layer_i, seed=111):
    """
    Split the data for a given class (layer_i) into train/val/test sets:
    - 20% test (random sample)
    - 10% val of the remaining (i.e., 12.5% of 80%)
    - rest train
    Returns a dict with lists of tile_ids for each split.
    """
    # Filter for the layer/class
    df_based = df[df["layer"] == layer_i]

    # Test set: 20% random sample
    np.random.seed(seed)
    df_base_test = df_based.sample(frac=0.2, random_state=seed)
    list_files_test = df_base_test["tile_id"].drop_duplicates().tolist()

    # Train + Validation set: remaining 80%
    df_base_train_val = df_based[~df_based["tile_id"].isin(list_files_test)]

    # Validation set: 10% of train+val (12.5% of 80%)
    np.random.seed(seed)
    df_base_val = df_base_train_val.sample(frac=0.125, random_state=seed)
    list_files_val = df_base_val["tile_id"].drop_duplicates().tolist()

    # Train set: remove tiles used in test and val
    df_base_train = df_base_train_val[
        ~df_base_train_val["tile_id"].isin(list_files_test)
        & ~df_base_train_val["tile_id"].isin(list_files_val)
    ]
    list_files_train = df_base_train["tile_id"].drop_duplicates().tolist()

    # Return a dict with lists for each split
    list_output = {
        "train": list_files_train,
        "val": list_files_val,
        "test": list_files_test
    }
    return list_output




def assign_files_for_base(list_files_dict, layer_i: str):
    """
    Copy tile image files for each split (train/val/test) and class (layer_i)
    into the appropriate folders. Skips missing files.
    """
    folder_base_path = "data/raw/"
    for category_i in ["train", "val", "test"]:
        list_files = list_files_dict[category_i]
        for fname in list_files:
            src = "data/raw/tiles/" + fname + ".tif"
            if category_i in ["train", "val"]:
                dst = folder_base_path + "images" + "/" + "base" + "/" + category_i + "/" + layer_i + "/" + fname + ".tif"
            elif category_i == "test":
                dst = folder_base_path + "images_test" + "/" + "base" + "/" + category_i + "/" + layer_i + "/" + fname + ".tif"
            src_path = here(src)
            dst_path = here(dst)
            if Path(src_path).exists():
                shutil.copy2(src_path, dst_path)
            else:
                print(f"File not found, skipped: {src_path}")

