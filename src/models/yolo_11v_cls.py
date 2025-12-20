import pandas as pd
from ultralytics import YOLO
import os
from pyprojroot.here import here

import torch
from great_tables import GT
from great_tables.data import gtcars
import gt_extras as gte
from great_tables import GT
from great_tables.data import airquality
from great_tables import html

# Randon sampling Analysis

def train_base():

    model = YOLO("yolo11n-cls.pt")  # small model
    dir_data_i = here("data/raw/images/base")
    print(f"Training Base ...")
    
    model.train(
      data=dir_data_i,    # The parent directory containing train/val folders
      epochs=100,        # Number of epochs to train
      patience = 20,
      imgsz=256,        # Image size (resize images to this size)
      batch=8,         # Batch size
      # project=here(f"models/runs/cls"f"{cv_i}"),  # Location to save the results
      project=here(f"models/runs/batch8_imgsz256/base"),  # Location to save the results
      # name=f"waste_cls_cv"     # Subdirectory name for this training session
      device='mps'
    )

# Cross Validation Analysis

def generate_dir_train_val():

  list_dir_data = {
    1: here("data/raw/images/cv1/"),
    2: here("data/raw/images/cv2/"),
    3: here("data/raw/images/cv3/"),
    4: here("data/raw/images/cv4/"),
    5: here("data/raw/images/cv5/")
  }
  return list_dir_data

# Train the model

def train_each_cv(cv_i):

    model = YOLO("yolo11n-cls.pt")  # small model
    dir_data_i = list_dir_path[cv_i]
    print(f"Training CV{cv_i} ...")
    
    model.train(
      data=dir_data_i,    # The parent directory containing train/val folders
      epochs=100,        # Number of epochs to train
      patience = 20,
      imgsz=256,        # Image size (resize images to this size)
      batch=8,         # Batch size
      # project=here(f"models/runs/cls"f"{cv_i}"),  # Location to save the results
      project=here(f"models/runs/batch8_imgsz256/cv{cv_i}"), # Location to save the results
      device='mps' 
      # name=f"waste_cls_cv"     # Subdirectory name for this training session
    )