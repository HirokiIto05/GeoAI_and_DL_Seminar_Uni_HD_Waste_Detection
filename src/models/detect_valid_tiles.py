import os
import csv
import pandas as pd
from pyprojroot import here
import geopandas as gpd

def text_to_dataframe(dir_txt_files):

    results = []
    # filename = os.listdir(dir_txt_files)[1]
    for filename in os.listdir(dir_txt_files):

        filepath = os.path.join(dir_txt_files, filename)

        with open(filepath, "r") as f:
            line = f.readline().strip()  # Read only the first line

        # Example: "0.99 non_waste"
        score_str, label = line.split()

        # Use txt filename as tile_id
        tile_id = os.path.splitext(filename)[0]
        results.append({"tile_id": tile_id, "label": label, "score": float(score_str)})

    return results