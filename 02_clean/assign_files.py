# 02.code/assign_files.py
# Assign tiles to waste / non-waste folders and train/val/test subfolders

from pathlib import Path
import shutil
import random

import geopandas as gpd
import pandas as pd

from pyprojroot.here import here



def delete_all_files_in_folder():
    folder_base_path = "data/raw/"

    for cv_i in [1,2,3,4,5]:
        for category_i in ["train", "val", "test"]:
            for folder_name_i in ["waste", "non_waste"]:
                if category_i in ["train", "val"]:
                    folder_path = folder_base_path + "images" + "/cv" + str(cv_i) + "/" + category_i + "/" + folder_name_i

                else:
                    folder_path = folder_base_path + "images_test" + "/" + folder_name_i
                    
                for file_path in Path(here(folder_path)).iterdir():
                    print(file_path)
                    if os.path.isfile(file_path):
                        os.remove(file_path)


delete_all_files_in_folder()



# ====== Load GeoJSON and preprocess ======
df = gpd.read_file(
    here("data/points/merged.geojson")
)



def generate_tiles_for_cv(df, cv_i, layer_i, seed=111):
    # Filter for the layer
    df_based = df[df["layer"] == layer_i]

    # ---- Test set ----
    df_cv_test = df_based[df_based["fold"] == cv_i]
    list_files_test = df_cv_test["tile_id"].drop_duplicates().tolist()

    # ---- Validation set: 15% sampled within each fold (except cv_i) ----
    df_not_test = df_based[df_based["fold"] != cv_i]

    # Equivalent of dplyr::slice_sample(prop=0.15, by="fold")
    # 12.5 means that 15% of full samples is 12.5% of remaining 80%
    np.random.seed(seed)
    df_cv_val = (
        df_not_test.groupby("fold", group_keys=False)
        .apply(lambda g: g.sample(frac=0.125, replace=False, random_state=seed))
    )

    list_files_val = df_cv_val["tile_id"].drop_duplicates().tolist()

    # ---- Train set: remove tiles used in test and val ----
    df_cv_train = df_based[
        ~df_based["tile_id"].isin(list_files_test)
        & ~df_based["tile_id"].isin(list_files_val)
    ]

    list_files_train = df_cv_train["tile_id"].drop_duplicates().tolist()

    # Return a dict similar to R’s list()
    return {
        "train": list_files_train,
        "val": list_files_val,
        "test": list_files_test
    }

def generate_cv_files(df, layer_i):
    list_cv1 = generate_tiles_for_cv(df, cv_i=1, layer_i=layer_i)
    list_cv2 = generate_tiles_for_cv(df, cv_i=2, layer_i=layer_i)
    list_cv3 = generate_tiles_for_cv(df, cv_i=3, layer_i=layer_i)
    list_cv4 = generate_tiles_for_cv(df, cv_i=4, layer_i=layer_i)
    list_cv5 = generate_tiles_for_cv(df, cv_i=5, layer_i=layer_i)

    list_cv = {
        "cv1": list_cv1,
        "cv2": list_cv2,
        "cv3": list_cv3,
        "cv4": list_cv4,
        "cv5": list_cv5,
    }
    return list_cv





list_cv_waste = generate_cv_files(df, layer_i="waste_point")
list_cv_non_waste = generate_cv_files(df, layer_i="non-waste_point")



def assign_files(list_cv, category_i: str, layer_i: str, cv_i = None):
    """
    list_files: list of filenames
    category_i: "train", "val", or "test"
    layer_i: "waste_point" or "non-waste_point"
    """
    folder_base_path = "data/raw/"

    # list_files = list_cv[category_i]
    for cv_i in range(1, 6) :
        for category_i in ["train", "val", "test"]:
            list_files = list_cv["cv" + str(cv_i)][category_i]
            for fname in list_files:
                src = "data/raw/tiles/" + fname + ".tif"
                if category_i in ["train", "val"]:
                    dst = folder_base_path + "images" + "/cv" + str(cv_i) + "/" + category_i + "/" + layer_i + "/" + fname + ".tif"
                elif category_i == "test":
                    dst = folder_base_path + "images_test" + "/" + layer_i + "/" + fname + ".tif"
                
                src_path = here(src)
                dst_path = here(dst)
                if Path(src_path).exists():
                    shutil.copy2(src_path, dst_path)
                else:
                    print(f"File not found, skipped: {src_path}")



fname = "r2187_c207"
src = "data/raw/tiles/" + fname + ".tif"
dst = folder_base_path + "images" + "/cv" + str(cv_i) + "/" + category_i + "/" + layer_i + "/" + fname + ".tif"




assign_files(list_cv_waste, category_i="train", layer_i="waste")
assign_files(list_cv_non_waste, category_i="train", layer_i="non_waste")
