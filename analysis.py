import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# Input and output paths
INPUT_PATH = Path("data/processed/cyprus_property_cleaned.csv")
OUTPUT_DIR = Path("outputs/analysis")

# Create output directory if it does not exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    """Load the final dashboard dataset."""

    df = pd.read_csv(INPUT_PATH)

    print(f"Dataset loaded: {len(df)} rows, {len(df.columns)} columns")

    return df
