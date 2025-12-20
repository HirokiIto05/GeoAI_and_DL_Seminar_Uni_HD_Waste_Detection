import geopandas as gpd
import pandas as pd

from pyprojroot.here import here

from k_means_constrained import KMeansConstrained

def generate_balanced_clusters(df):
    # Convert coordinates to numpy array
    coords = df.geometry.apply(lambda p: [p.x, p.y]).tolist()

    # --- 2. Set cluster count and cluster size ---
    n_clusters = 5
    size_per_cluster = len(df) // n_clusters

    # --- 3. Run Balanced K-means ---
    clf = KMeansConstrained(
        n_clusters=n_clusters,
        size_min=size_per_cluster,
        size_max=size_per_cluster,
        random_state=111
    )

    labels = clf.fit_predict(coords)

    # --- 4. Add results to GeoDataFrame ---
    df['fold'] = labels

    return df