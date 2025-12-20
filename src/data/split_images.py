import geopandas as gpd
import subprocess
from pyprojroot.here import here

def split_images():
    for i, row in grid_filtered.iterrows():
        tile = row["tile_id"]
        xmin, ymin, xmax, ymax = row.geometry.bounds

        cmd = [
            "gdal_translate",
            "--config", "CPL_PROGRESS", "1",
            "-projwin", str(xmin), str(ymax), str(xmax), str(ymin),
            "-co", "COMPRESS=LZW",
            tif,
            f"../01_data/raw/tiles_c664/{tile}.tif"
        ]

        print(f"Processing {tile} ...")
        subprocess.run(cmd)

