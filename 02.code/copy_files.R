library(sf)
library(tidyverse)
library(here)

df_merged_raw <- st_read("/Users/ito_hiroki/05.Lecture/GeoAI/GeoAI/data/points/merged.geojson", quiet = TRUE)

df_merged <- df_merged_raw |> 
    mutate(
        is_waste = if_else(layer == "Waste", TRUE, FALSE),
    ) |>
    select(id, is_waste, row, col, geometry) |>
    arrange(id, row, col)

# Copy pictures with waste to another folder
base_path <- here("data/images/")
base_filename <- "690585b76415e43597ffd7eb_complete_"

generate_list_files <- function(df_merged, is_waste_i) {

  list_output <- df_merged |>
    dplyr::filter(
        is_waste == is_waste_i
    ) |>
    mutate(
        file_path = paste0(base_filename, "r", row, "_c", col, ".tif")
    ) |>
    pull(file_path)

  return(list_output)
}

copy_files <- function(df_merged, is_waste_i) {

    list_files <- generate_list_files(df_merged, is_waste_i)

    if(is_waste_i) {
        folder_name <- "waste"
    } else {
        folder_name <- "non_waste"
    }

    for (i in list_files) {
        file.copy(
          from = here("01.data", "Freetown_tiles_5m", i),
          to   = here("01.data", folder_name),
          overwrite = TRUE
        )
    }

}

copy_files(df_merged, TRUE)  # Copy waste files
copy_files(df_merged, FALSE)  # Copy non-waste files


assign_files <- function(list_files, category_i, folder_name) {

  for (i in list_files) {
    file.copy(
      from = here("01.data", folder_name, i),
      to   = here("01.data", "intermediate", category_i, folder_name),
      overwrite = TRUE
    )
  }

}


copy_files_to_category <- function(is_waste_i) {

    if(is_waste_i) {
        folder_name <- "waste"
    } else {
        folder_name <- "non_waste"
    }

    # list_filesを7割、1.5割、1.5割に分割
    set.seed(1111)  
    list_files <- list.files(here("01.data", folder_name))

    total_n <- length(list_files)
    idx <- sample(total_n)
    train <- floor(total_n * 0.7)
    val <- floor(total_n * 0.15)
    test <- total_n - train - val

    list_files_train <- list_files[idx[1:train]]
    list_files_val <- list_files[idx[(train+1):(train+val)]]
    list_files_test <- list_files[idx[(train+val+1):total_n]]

    assign_files(list_files_train, "train", folder_name)
    assign_files(list_files_val, "val", folder_name)
    assign_files(list_files_test, "test", folder_name)

}

copy_files_to_category(TRUE)
copy_files_to_category(FALSE)
