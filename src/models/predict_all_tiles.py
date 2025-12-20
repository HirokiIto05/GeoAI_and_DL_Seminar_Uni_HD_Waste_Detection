from pathlib import Path
import shutil
import random

import pandas as pd
from ultralytics import YOLO
import os
from pyprojroot.here import here


def delete_all_predict():

    folder_path = "data/intermediate/predicted_tiles/predict/labels"

    for file_path in Path(here(folder_path)).iterdir():
        print(file_path)
        if os.path.isfile(file_path):
            os.remove(file_path)

def apply_model_to_all_tiles():
    results_list = []
  
    model = YOLO(here("models/runs/cv4/train/weights/best.pt"))
  
    list_image_path = [f for f in os.listdir(here("data/intermediate/tiles_png/"))]

    for image_name in list_image_path:
  
        image_path = here("data/intermediate/tiles_png/" + image_name)
  
        # Perform inference on the image
        results = model(image_path)
  
        # Get the results from the inference
        r = results[0]  # Inference result
  
        top1 = r.probs.top1  # Index of the predicted class
        conf = r.probs.top1conf  # Confidence score of the prediction
        label = r.names[top1]  # Predicted class name
        # Append the result to the list
        results_list.append([image_name, label])

    return results_list