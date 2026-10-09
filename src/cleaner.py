"""
Cyprus Property Intelligence
Data Cleaning Pipeline

This module loads the raw Cyprus property dataset,
cleans and standardizes the data, validates data quality,
and saves the cleaned dataset.
"""

from pathlib import Path
import pandas as pd
import numpy as np


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_FILE = PROJECT_ROOT / "data" / "raw" / "cyprus_properties_raw.csv"

CLEANED_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cyprus_property_cleaned.csv"
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

def load_raw_data():
    """Load the raw property dataset."""

    df = pd.read_csv(RAW_FILE)

    print(f"Raw dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

    return df


# ---------------------------------------------------------
# TEXT CLEANING
# ---------------------------------------------------------

def clean_text_columns(df):
    """Clean and standardize text-based columns."""

    text_columns = [
        "property_id",
        "title",
        "location",
        "parking",
        "floor"
    ]

    for column in text_columns:
        if column in df.columns:
            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
                .replace(
                    {
                        "": pd.NA,
                        "nan": pd.NA,
                        "None": pd.NA,
                        "N/A": pd.NA,
                        "NA": pd.NA,
                        "-": pd.NA
                    }
                )
            )

    return df


# ---------------------------------------------------------
# PROPERTY ID
# ---------------------------------------------------------

def clean_property_id(df):
    """Remove the ID prefix and standardize property IDs."""

    if "property_id" in df.columns:

        df["property_id"] = (
            df["property_id"]
            .astype("string")
            .str.replace("ID ", "", regex=False)
            .str.strip()
        )

        df["property_id"] = pd.to_numeric(
            df["property_id"],
            errors="coerce"
        ).astype("Int64")

    return df


# ---------------------------------------------------------
# PRICE
# ---------------------------------------------------------

def clean_price(df):
    """Convert property prices from text to numeric euros."""

    if "price" in df.columns:

        df["price"] = (
            df["price"]
            .astype("string")
            .str.replace("€", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.replace(" ", "", regex=False)
            .str.strip()
        )

        df["price"] = pd.to_numeric(
            df["price"],
            errors="coerce"
        )

    return df


# ---------------------------------------------------------
# PRICE PER SQUARE METRE
# ---------------------------------------------------------

def clean_price_per_m2(df):
    """Convert price per square metre to numeric."""

    if "price_per_m2" in df.columns:

        df["price_per_m2"] = (
            df["price_per_m2"]
            .astype("string")
            .str.replace("€", "", regex=False)
            .str.replace("/m²", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.replace(" ", "", regex=False)
            .str.strip()
        )

        df["price_per_m2"] = pd.to_numeric(
            df["price_per_m2"],
            errors="coerce"
        )

    return df


# ---------------------------------------------------------
# COVERED AREA
# ---------------------------------------------------------

def clean_covered_area(df):
    """Convert covered property area to numeric square metres."""

    if "covered_area" in df.columns:

        df["covered_area"] = (
            df["covered_area"]
            .astype("string")
            .str.replace("m²", "", regex=False)
            .str.replace("m2", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.replace(" ", "", regex=False)
            .str.strip()
        )

        df["covered_area"] = pd.to_numeric(
            df["covered_area"],
            errors="coerce"
        )

    return df


# ---------------------------------------------------------
# BEDROOMS AND BATHROOMS
# ---------------------------------------------------------

def clean_room_counts(df):
    """Convert bedroom and bathroom counts to numeric values."""

    for column in ["bedrooms", "bathrooms"]:

        if column in df.columns:

            df[column] = (
                df[column]
                .astype("string")
                .str.extract(r"(\d+(?:\.\d+)?)", expand=False)
            )

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    return df


# ---------------------------------------------------------
# PARKING
# ---------------------------------------------------------

def clean_parking(df):
    """Standardize parking categories."""

    if "parking" in df.columns:

        df["parking"] = (
            df["parking"]
            .astype("string")
            .str.strip()
            .str.lower()
        )

        parking_mapping = {
            "covered": "Covered",
            "uncovered": "Uncovered",
            "yes": "Available",
            "no": "Not Available",
            "none": "Not Available",
            "available": "Available"
        }

        df["parking"] = df["parking"].replace(parking_mapping)

        df["parking"] = df["parking"].fillna("Unknown")

    return df

# ---------------------------------------------------------
# FLOOR
# ---------------------------------------------------------

def clean_floor(df):
    """Clean and standardize floor information."""

    if "floor" in df.columns:

        floor = (
            df["floor"]
            .astype("string")
            .str.strip()
            .str.lower()
        )

        # Clean floor information
        df["floor_number"] = pd.to_numeric(
            floor.str.extract(r"(\d+)")[0],
            errors="coerce"
        )

        df["total_floor"] = pd.to_numeric(
            floor.str.extract(r"of\s*(\d+)")[0],
            errors="coerce"
        )

    return df

# ---------------------------------------------------------
# DISTRICT
# ---------------------------------------------------------

def extract_district(df):
    """
    Extract the Cyprus district from the location field.

    Examples:
    'Livadia Larnakas, Larnaca district'
    -> 'Larnaca'

    'Germasogeia, Limassol district'
    -> 'Limassol'
    """

    if "location" in df.columns:

        df["district"] = (
            df["location"]
            .astype("string")
            .str.extract(
                r"([A-Za-z]+)\s+district",
                expand=False
            )
            .str.strip()
            .str.title()
        )

    return df


# ---------------------------------------------------------
# MISSING VALUES
# ---------------------------------------------------------

def handle_missing_values(df):
    """Standardize missing values without unnecessarily
    removing valid property records."""

    # Numerical variables remain NaN when information
    # was not available.
    numeric_columns = [
        "price",
        "price_per_m2",
        "bedrooms",
        "bathrooms",
        "covered_area",
        "floor_number",
        "total_floor"
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # Categorical fields use Unknown where appropriate.
    categorical_columns = [
        "location",
        "parking",
        "floor",
        "district"
    ]

    for column in categorical_columns:
        if column in df.columns:
            df[column] = df[column].fillna("Unknown")

    return df


# ---------------------------------------------------------
# DUPLICATES
# ---------------------------------------------------------

def remove_duplicates(df):
    """Remove duplicate property listings."""

    before = len(df)

    if "property_id" in df.columns:

        df = df.drop_duplicates(
            subset=["property_id"],
            keep="first"
        )

    else:

        df = df.drop_duplicates()

    removed = before - len(df)

    print(f"Duplicate rows removed: {removed}")

    return df


# ---------------------------------------------------------
# VALIDATION
# ---------------------------------------------------------

def validate_cleaned_data(df):
    """Generate basic data-quality information."""

    validation = {
        "rows": len(df),
        "columns": len(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_values": int(df.isnull().sum().sum())
    }

    print("\nData validation")
    print("----------------")
    print(f"Rows: {validation['rows']}")
    print(f"Columns: {validation['columns']}")
    print(f"Duplicate rows: {validation['duplicate_rows']}")
    print(f"Total missing values: {validation['missing_values']}")

    print("\nMissing values by column:")
    print(df.isnull().sum())

    return validation


# ---------------------------------------------------------
# SAVE DATA
# ---------------------------------------------------------

def save_cleaned_data(df):
    """Save the cleaned dataset."""

    CLEANED_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        CLEANED_FILE,
        index=False
    )

    print(f"\nCleaned dataset saved to:")
    print(CLEANED_FILE)


# ---------------------------------------------------------
# COMPLETE CLEANING PIPELINE
# ---------------------------------------------------------

def clean_data():
    """Run the complete cleaning pipeline."""

    print("\nStarting Cyprus property data cleaning...\n")

    df = load_raw_data()

    df = clean_text_columns(df)
    df = clean_property_id(df)
    df = clean_price(df)
    df = clean_price_per_m2(df)
    df = clean_covered_area(df)
    df = clean_room_counts(df)
    df = clean_parking(df)
    df = clean_floor(df)
    df = extract_district(df)
    df = handle_missing_values(df)
    df = remove_duplicates(df)

    validate_cleaned_data(df)

    save_cleaned_data(df)

    print("\nCleaning completed successfully.")

    return df


# ---------------------------------------------------------
# RUN SCRIPT
# ---------------------------------------------------------

if __name__ == "__main__":
    clean_data()
