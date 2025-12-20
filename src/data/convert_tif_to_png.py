# ------------------------------------------------------------
# convert_tif_to_png.py
#
# This script deletes old PNG files and converts TIFF (.tif) images to PNG (.png)
# for geospatial tile datasets. It supports conversion for cross-validation test
# sets, base test sets, and all tiles. The script uses PIL for image conversion
# and organizes outputs into appropriate folders.
#
# ------------------------------------------------------------

def delete_all_files_in_test():
    """
    Delete all files in the cross-validation test PNG folders for both waste and non_waste classes.
    """

    for cv_i in [1,2,3,4,5]:
        for folder_name_i in ["waste", "non_waste"]:
            folder_path = "data/intermediate/images_test/" + "cv" + str(cv_i) + "/" + "test" + "/" + folder_name_i
            # Delete all files in the folder
            for file_path in Path(here(folder_path)).iterdir():
                print(file_path)
                if os.path.isfile(file_path):
                    os.remove(file_path)


def convert_tif_to_png(is_waste_i):
    """
    Convert all .tif files in the cross-validation test set to .png for a given class.
    """
    if is_waste_i:
        folder_name_i = "waste"
    else:
        folder_name_i = "non_waste"
  
    for cv_i in [1,2,3,4,5]:
        list_files = [f for f in os.listdir(here(f"data/raw/images_test/cv{cv_i}/test/{folder_name_i}/")) if f.endswith('.tif')]
        for fname in list_files:
            src = here(f"data/raw/images_test/cv{cv_i}/test/{folder_name_i}/{fname}")
            dst_folder = here(f"data/intermediate/images_test/cv{cv_i}/test/{folder_name_i}")
            png_fname = fname.replace(".tif", ".png")
            dst = os.path.join(dst_folder, png_fname)
            # Check the source file exists
            if src.exists():
                # Open the TIFF image and save as PNG
                with Image.open(src) as img:
                    img.save(dst, "PNG")
                # print(f"Converted and moved: {src} to {dst}")
            else:
                print(f"File not found, skipped: {src}")


# convert_tif_to_png(is_waste_i=True)
# convert_tif_to_png(is_waste_i=False)

def delete_all_files_in_test_base():
    """
    Delete all files in the base test PNG folders for both waste and non_waste classes.
    """

    for folder_name_i in ["waste", "non_waste"]:
        folder_path = "data/intermediate/images_test/" + "base"  + "/test/" + folder_name_i
        # Delete all files in the folder
        for file_path in Path(here(folder_path)).iterdir():
            print(file_path)
            if os.path.isfile(file_path):
                os.remove(file_path)

def convert_tif_to_png_base(is_waste_i):
    """
    Convert all .tif files in the base test set to .png for a given class.
    """
    if is_waste_i:
        folder_name_i = "waste"
    else:
        folder_name_i = "non_waste"
  
    list_files = [f for f in os.listdir(here(f"data/raw/images_test/base/test/{folder_name_i}/")) if f.endswith('.tif')]
    for fname in list_files:
        src = here(f"data/raw/images_test/base/test/{folder_name_i}/{fname}")
        dst_folder = here(f"data/intermediate/images_test/base/test/{folder_name_i}")
        png_fname = fname.replace(".tif", ".png")
        dst = os.path.join(dst_folder, png_fname)
        # Check the source file exists
        if src.exists():
            # Open the TIFF image and save as PNG
            with Image.open(src) as img:
                img.save(dst, "PNG")
            # print(f"Converted and moved: {src} to {dst}")
        else:
            print(f"File not found, skipped: {src}")


# Convert all tif files in the test set to png files
def convert_tif_to_png_all():
    """
    Convert all .tif files in the raw tiles folder to .png and save to the intermediate folder.
    """
    list_files = [f for f in os.listdir(here(f"data/raw/tiles")) if f.endswith('.tif')]
    for fname in list_files:
        src = here(f"data/raw/tiles/{fname}")
        dst_folder = here("data/intermediate/tiles_png/")
        png_fname = fname.replace(".tif", ".png")
        dst = os.path.join(dst_folder, png_fname)
        # Check the source file exists
        if src.exists():
            # Open the TIFF image and save as PNG
            with Image.open(src) as img:
                img.save(dst, "PNG")                
            # print(f"Converted and moved: {src} to {dst}")
        else:
            print(f"File not found, skipped: {src}")

