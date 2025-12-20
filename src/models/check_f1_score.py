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


# Fuctions
def generate_test_base(is_waste_i):
    if is_waste_i:
        folder_name_i = "waste"
    else:
        folder_name_i = "non_waste"
  
    dir_test_png = here(f"data/intermediate/images_test/base/test/{folder_name_i}/")
    list_test_png = [f for f in os.listdir(dir_test_png) if f.endswith('.png')]
    return list_test_png



def generate_test_png_dir(cv_i, is_waste_i):
    if is_waste_i:
        folder_name_i = "waste"
    else:
        folder_name_i = "non_waste"
  
    dir_test_png = here(f"data/intermediate/images_test/cv{cv_i}/test/{folder_name_i}/")
    list_test_png = [f for f in os.listdir(dir_test_png) if f.endswith('.png')]
    return list_test_png



def generate_list_cv_test(is_waste_i):
    list_cv1_test = generate_test_png_dir(1, is_waste_i)
    list_cv2_test = generate_test_png_dir(2, is_waste_i)
    list_cv3_test = generate_test_png_dir(3, is_waste_i)
    list_cv4_test = generate_test_png_dir(4, is_waste_i)
    list_cv5_test = generate_test_png_dir(5, is_waste_i)

    list_cv = {
        "cv1": list_cv1_test,
        "cv2": list_cv2_test,
        "cv3": list_cv3_test,
        "cv4": list_cv4_test,
        "cv5": list_cv5_test,
    }
    return list_cv



# List to store the results
def check_prediction(list_image_path, is_waste_i, model_path, cv_i = None) :
  results_list = []

  model = YOLO(here(model_path))


  if is_waste_i:
      folder_name_i = "waste"
  else:
      folder_name_i = "non_waste"

  if cv_i is None:
      base_path = here(f"data/intermediate/images_test/base/test/{folder_name_i}/")
  else:
      base_path = here(f"data/intermediate/images_test/cv{cv_i}/test/{folder_name_i}/")

  for image_name in list_image_path:

      image_path = os.path.join(base_path, image_name)

      # Perform inference on the image
      results = model(image_path)

      # Get the results from the inference
      r = results[0]  # Inference result
      top1 = r.probs.top1  # Index of the predicted class
      conf = r.probs.top1conf  # Confidence score of the prediction
      label = r.names[top1]  # Predicted class name

      # Check if the prediction is correct
      is_correct = label == folder_name_i  # True if prediction matches the actual label

      # Append the result to the list
      results_list.append([image_name, folder_name_i, label, is_correct])
  
  return results_list



def aggregate_accuracy_cvs(list_test, is_waste_i):

    cv1_accuracy = check_prediction(list_test["cv1"], is_waste_i = is_waste_i, model_path=here("models/runs/batch8_imgsz256/cv1/train/weights/best.pt"), cv_i = 1)
    cv2_accuracy = check_prediction(list_test["cv2"], is_waste_i = is_waste_i, model_path=here("models/runs/batch8_imgsz256/cv2/train/weights/best.pt"), cv_i = 2)
    cv3_accuracy = check_prediction(list_test["cv3"], is_waste_i = is_waste_i, model_path=here("models/runs/batch8_imgsz256/cv3/train/weights/best.pt"), cv_i = 3)
    cv4_accuracy = check_prediction(list_test["cv4"], is_waste_i = is_waste_i, model_path=here("models/runs/batch8_imgsz256/cv4/train/weights/best.pt"), cv_i = 4)
    cv5_accuracy = check_prediction(list_test["cv5"], is_waste_i = is_waste_i, model_path=here("models/runs/batch8_imgsz256/cv5/train/weights/best.pt"), cv_i = 5)
    list_cv_test_results = {
        "cv1_accuracy": cv1_accuracy,
        "cv2_accuracy": cv2_accuracy,
        "cv3_accuracy": cv3_accuracy,
        "cv4_accuracy": cv4_accuracy,
        "cv5_accuracy": cv5_accuracy,
    }
  
    return list_cv_test_results




def calculate_f1_score(cv_i, results_waste, results_non_waste) :

    if cv_i == None:
        df_results_waste = pd.DataFrame(results_waste["base_waste"], columns=["file_name", "actual", "prediction", "is_correct"])
        df_results_non_waste = pd.DataFrame(results_non_waste["base_non_waste"], columns=["file_name", "actual", "prediction", "is_correct"])
    else:
        df_results_waste = pd.DataFrame(results_waste[f"cv{cv_i}_accuracy"], columns=["file_name", "actual", "prediction", "is_correct"])
        df_results_non_waste = pd.DataFrame(results_non_waste[f"cv{cv_i}_accuracy"], columns=["file_name", "actual", "prediction", "is_correct"])


    df_true_positive = df_results_waste[df_results_waste['is_correct'] == True]
    df_false_negative = df_results_waste[df_results_waste['is_correct'] == False]
    
    df_false_positive = df_results_non_waste[df_results_non_waste['is_correct'] == False]
    df_true_negative = df_results_non_waste[df_results_non_waste['is_correct'] == True]

    true_positive = len(df_true_positive)
    false_negative = len(df_false_negative)
    false_positive = len(df_false_positive)
    true_negative = len(df_true_negative)
    
    precision = true_positive / (true_positive + false_positive) 
    recall = true_positive / (true_positive + false_negative) 

    f1_score = (2 * precision * recall) / (precision + recall)

    overall = {
      "precision": precision,
      "recall": recall,
      "f1_score": f1_score  
    }

    # summary = pd.DataFrame([overall])
    return overall



def aggregate_score_summary(results_waste, results_non_waste):

    cv1_score_summary = calculate_f1_score(1, results_waste, results_non_waste)
    cv2_score_summary = calculate_f1_score(2, results_waste, results_non_waste)
    cv3_score_summary = calculate_f1_score(3, results_waste, results_non_waste)
    cv4_score_summary = calculate_f1_score(4, results_waste, results_non_waste)
    cv5_score_summary = calculate_f1_score(5, results_waste, results_non_waste)

    list_cv_test_summary = {
        "cv1_summary": cv1_score_summary,
        "cv2_summary": cv2_score_summary,
        "cv3_summary": cv3_score_summary,
        "cv4_summary": cv4_score_summary,
        "cv5_summary": cv5_score_summary,
    }

    return list_cv_test_summary


def summary_base_epoch():
    df_info_raw = pd.read_csv(here(f"models/runs/batch8_imgsz256/base/train/results.csv"))
    epoch_max = df_info_raw['epoch'].max()
    
    return epoch_max

def generate_table_base_summary(df, best_epoch):
    df['best_epoch'] = best_epoch
    df['batch_size'] = 8
    df['image_size'] = 256
    df['epoch_initial'] = 100
    df['precision'] = df['precision'].round(3)
    df['recall'] = df['recall'].round(3)
    df['f1_score'] = df['f1_score'].round(3)
    return df


def concat_cv_score_df(metrics_cv):
    df_list = []
    for cv_i in range(1, 6):
        df_cv = pd.DataFrame([metrics_cv[f"cv{cv_i}_summary"]])
        df_cv["cv"] = cv_i
        df_list.append(df_cv)
    df_all = pd.concat(df_list, ignore_index=True)
    return df_all

# Train Infomation
def summary_epoch() :
    df_list = []
    for cv_i in range(1, 6):
        df_info_raw = pd.read_csv(here(f"models/runs/batch8_imgsz256/cv{cv_i}/train/results.csv"))
        epoch_max = df_info_raw['epoch'].max()
        dict_cv_i = {
            "cv": cv_i,
            "best_epoch": epoch_max
        }
        df_list.append(pd.DataFrame([dict_cv_i]))

    df_all = pd.concat(df_list, ignore_index=True)
    return df_all

def generate_table_summary(df_summary_f1, list_epoch_info):
    df_summary = df_summary_f1.merge(list_epoch_info, on="cv", how="left")
    df_summary['batch_size'] = 8
    df_summary['image_size'] = 256
    df_summary['epoch_initial'] = 100

    df_summary['precision'] = df_summary['precision'].round(3)
    df_summary['recall'] = df_summary['recall'].round(3)
    df_summary['f1_score'] = df_summary['f1_score'].round(3)
    return df_summary 

