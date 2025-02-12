from itertools import combinations
from sklearn.metrics import cohen_kappa_score
import numpy as np
import pandas as pd
import os


print("______________")
print("IAA")
print("______________")


def iaa(col: int):
    # Specify the folder containing the CSV files
    folder_path = 'notes/data/iaa/iaa_data/'

    # Read all CSV files and extract the annotations from column 2
    ids = None
    ratings = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)

            # Extract IDs from the first column
            if ids is None:
                ids = df.iloc[:, 0].tolist()  # Store the IDs once
            else:
                # Check if IDs are consistent across all files
                assert ids == df.iloc[:, 0].tolist(), f"ID mismatch in {filename}"

            # Assuming column 2 is the annotations (index 1 in 0-based Python)
            annotations = df.iloc[:, col].tolist()
            ratings.append(annotations)
            #print(f"Loaded annotations from: {filename}")

    # Check if we have enough raters
    if len(ratings) < 2:
        raise ValueError("Need at least 2 raters for Cohen's Kappa")
    # Calculate Cohen's Kappa for all pairs
    pairwise_kappas = []
    disagreements = set()
    pairs = list(combinations(range(len(ratings)), 2))
    for i, j in pairs:
        kappa = cohen_kappa_score(ratings[i], ratings[j])
        pairwise_kappas.append(kappa)
        print(f"Cohen's Kappa for Rater {i+1} and Rater {j+1}: {kappa}")

        # Track disagreements for each item
        for index, (anno_i, anno_j) in enumerate(zip(ratings[i], ratings[j])):
            if anno_i != anno_j:
                disagreements.add(ids[index])

    # Calculate the average pairwise Kappa
    average_kappa = np.mean(pairwise_kappas)
    print(f"\nAverage Pairwise Cohen's Kappa: {average_kappa}")

    # Output IDs with disagreements
    if disagreements:
        print("\nIDs with disagreements:")
        print(sorted(disagreements))
    else:
        print("\nNo disagreements found.")

print("IAA stimulus")
iaa(1)
print()
print("IAA metacommunication")
iaa(2)
