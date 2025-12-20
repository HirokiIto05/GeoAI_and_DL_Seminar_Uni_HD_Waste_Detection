import pandas as pd
from pyprojroot import here
import geopandas as gpd
from libpysal.weights import Queen
from esda.moran import Moran
from esda.moran import Moran_Local
from libpysal.weights import Queen

def generate_table_quadrant_summary(df):
    quadrant_counts = df['quadrant'].value_counts().sort_index()
    total_count = len(df)

    summary_df = pd.DataFrame({
        'Quadrant': quadrant_counts.index,
        'Count': quadrant_counts.values,
        'Percentage': (quadrant_counts.values / total_count * 100).round(2)
    })

    return summary_df