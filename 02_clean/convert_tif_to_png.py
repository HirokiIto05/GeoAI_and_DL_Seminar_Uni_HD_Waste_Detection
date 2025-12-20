from PIL import Image
from pyprojroot.here import here

# Open the TIFF image
dir_test = here("data/raw/images/test/waste/sample_image.tif")


# Save the image as PNG
png_image_path = "path/to/your/output_image.png"
image.save(png_image_path, "PNG")

print(f"Image saved as {png_image_path}")



list_files_waste = [f for f in os.listdir(here("data/raw/images/test/waste/")) if f.endswith('.tif')]
list_files_non_waste = [f for f in os.listdir(here("data/raw/images/test/non_waste/")) if f.endswith('.tif')]

def convert_tif_to_png(list_files, is_waste_i):
  if is_waste_i:
      folder_name_i = "waste"
  else:
      folder_name_i = "non_waste"

  for fname in list_files:
      src = here(f"data/raw/images/test/{folder_name_i}/{fname}")
      dst_folder = here(f"data/intermediate/test_images/{folder_name_i}")

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


convert_tif_to_png(list_files_waste, is_waste_i=True)
convert_tif_to_png(list_files_non_waste, is_waste_i=False)