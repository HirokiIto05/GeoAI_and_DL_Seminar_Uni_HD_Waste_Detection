# Overview
The aim of this project is to identify illegally dumped waste in Freetown, Sierra Leone. The project was carried out using a machine learning approach (YOLO v11). The repository includes all relevant code.

The **src** directory contains a set of functions, and these functions are run — and outputs are saved — through the files in the **notebooks/** directory.

Functions in **src/data** are executed in **notebooks/data**, and functions in **src/models** are executed in **notebooks/models.qmd**. In this way, the **src** and **notebooks** directories correspond to each other.

Because the workflow moves back and forth between QGIS and Python, please refer to the **# WORKFLOW** section for more details.

# **Project Folder Structure(Omitted)**


data/
  raw/
  intermdiate/
src/ # Function scripts
  analysis/.
  data/.
  models/.
  visualization/.
notebooks/ # Execution scripts
  analysis.qmd
  data.qmd
  models.qmd
  visualization.qmd
models/ # Trained model outputs
output/ # Result outputs (e.g., F1 scores)


# **Data Processing Workflow**

Here is a cleaner, fully formatted **Markdown version** of your workflow script:

---

# **Data Processing Workflow**

## **1. Image Preparation**

### ** Split images into tiles — Python**

| Step | Task                              | Tool / Language | Inputs / Functions                                                 | Outputs                                         | Notebook             |
| ---- | --------------------------------- | --------------- | ------------------------------------------------------------------ | ----------------------------------------------- | -------------------- |
| 1.1  | Split images into tiles           | Python          | `src/data/split_images.py`                                         | `data/raw/tiles/*.tif`                          | `notebooks/data.qmd` |
| 1.2  | Annotate points                   | QGIS            | —                                                                  | `data/raw/merged.gpkg`                          | —                    |
| 1.3  | Assign files to folders           | Python          | `src/data/assign_files_base.py` <br> `src/data/assign_files_cv.py` | `data/raw/images/` <br> `data/raw/images_test/` | `notebooks/data.qmd` |
| 1.4  | Convert `.tif` → `.png` (testing) | Python          | `src/data/convert_tif_to_png.py`                                   | `data/intermediate/images_test/`                | `notebooks/data.qmd` |

---

## **2. Spatial Cross-Validation**

### ** Generate spatial folds (k-means clustering) — Python**

**Input Function:**
`src/data/clustering.py`

**Output:**
`data/intermediate/points_for_cv.gpkg`

**Execution Notebook:**
`notebooks/data.qmd`

---

## **3. Model Training and Evaluation**

### ** Train YOLO models — Python**

**Input Function:**
`src/models/yolo_11v_cls.py`

**Outputs:**

```
models/runs/batch8_imgsz256/base/
models/runs/batch8_imgsz256/cv1/
models/runs/batch8_imgsz256/cv2/
…
```

**Execution Notebook:**
`notebooks/models.qmd`

### ** Compute F1 scores — Python**

**Input Function:**
`src/models/check_f1_score.py`

**Outputs:**

```
output/f1_score/summary_yolo_batch8_imgsz256_base.csv
output/f1_score/summary_yolo_batch8_imgsz256_cv.csv
```

**Execution Notebook:**
`notebooks/models.qmd`

### ** Predict across all tiles — Python**

**Input Function:**
`src/models/predict_all_tiles.py`

**Output:**
`data/intermediate/predicted_tiles/results_all_tiles.gpkg`

**Execution Notebook:**
`notebooks/models.qmd`

### ** Filter tiles by confidence threshold — Python**

**Input Function:**
`src/models/detect_valid_tiles.py`

**Output:**
`data/intermediate/predicted_tiles/waste_points.gpkg`

**Execution Notebook:**
`notebooks/models.qmd`

---

## **4. Spatial Autocorrelation (Moran's I)**

* **[QGIS] Generate spatial grids**
  Resolutions: 10 m, 20 m, 30 m, 40 m

* **[QGIS] Convert predicted waste grids to point centroids**
  **Output:**
  `data/predicted_tiles/results_all_tiles_points.gpkg`

* **[Python] Calculate waste density per grid size**
  `src/analysis/calculate_waste_density_grids.py`
  Outputs:

  * `data/density/waste_density_10.gpkg`
  * `data/density/waste_density_20.gpkg`
  * …

* **[Python] Compute Global Moran’s I using grid density values**

* **[Python] Compute Local Moran’s I (5 m and 20 m grids)**

---

## **5. Waterway Analysis**

* **[QGIS] Generate centroids**
  Input: `waste_points.gpkg`

* **[QGIS] Extract waterways from OpenStreetMap**

* **[QGIS] Create buffer zones**

* **[Python] Identify waste points within buffer regions**

---


# **Project Folder Structure**
```
PROJECT/
├── data/
│   ├── raw/
│   │   ├── boundary/              # project boundary 
│   │   ├── geotiff/               # Original large geotiff images
│   │   ├── grids/                 # Spatial grids
│   │   ├── images/
│   │   │   ├── base/
│   │   │   │   ├── train/
│   │   │   │   └── val/
│   │   │   ├── cv1/
│   │   │   │   ├── train/
│   │   │   │   └── val/
│   │   │   └── images_test/
│   │   │       ├── base/
│   │   │       │   └── test/
│   │   │       ├── cv1/
│   │   │       │   └── test/
│   │   │       └── ...           
│   │   ├── points/                # Annotated points
│   │   ├── tiles/                 # Image tiles 
│   │   └── waterway/              # Waterway gpkg file
│   │
│   ├── intermediate/
│   │   ├── density/               # density data
│   │   ├── moran/                 # Moran's I results (5m & 20m grids)
│   │   ├── predicted_tiles/       # all predicted tiles
│   │   ├── scv/                   # spatial cross-validation points
│   │   ├── tiles_png/             # all PNG tiles 
│   │   └── tiles_test/            # tiles for F1 score calculation
│
├── notebooks/
│   ├── data.qmd                   # data preprocessing
│   ├── analysis.qmd
│   ├── models.qmd
│   └── visualization.qmd
│
├── src/
│   ├── data/
│   │   ├── assign_file_base.py
│   │   ├── assign_file_cv.py
│   │   ├── clustering.py
│   │   ├── convert_tif_to_png.py
│   │   └── split_images.py
│   │
│   ├── analysis/
│   │   ├── calculate_waste_density_grids.py
│   │   ├── moran.py
│   │   └── waterway_analysis.py
│   │
│   ├── models/
│   │   ├── check_f1_score.py
│   │   ├── detect_valid_tiles.py
│   │   ├── predict_all_tiles.py
│   │   └── yolo_11v_cls.py
│   │
│   └── visualisation/
│       ├── figure2_moran_plot.py
│       ├── table1_scv.py
│       ├── table2_local_moran.py
│       └── table3_waterway.py
│
├── models/
│   └── runs/
│       └── batch8_imgsz256/
│           ├── base/              # YOLO results
│           ├── cv1/
│           └── ...
│
└── output/
    └── f1_score/
        ├── summary_yolo_batch8_imgsz256_base.csv
        └── summary_yolo_batch8_imgsz256_cv.csv
```