import pandas as pd
from pathlib import Path


# Input and output paths
INPUT_PATH = Path("data/processed/cyprus_property_cleaned.csv")
OUTPUT_PATH = Path("data/processed/cyprus_property_cleaned.csv")


def create_dashboard_dataset(df):
    """Create the final dataset used by the Looker Studio dashboard."""

    dashboard_df = df[
        [
            "property_id",
            "title",
            "district",
            "location",
            "price",
            "price_per_m2",
            "bedrooms",
            "bathrooms",
            "covered_area",
            "parking",
            "floor_number",
            "total_floor"
        ]
    ].copy()

    return dashboard_df


def main():
    """Load the cleaned data, create the dashboard dataset, and save it."""

    print("Starting dashboard data processing...")

    # Load cleaned dataset
    df = pd.read_csv(INPUT_PATH)

    print(f"Cleaned dataset loaded: {len(df)} rows, {len(df.columns)} columns")

    # Create dashboard dataset
    dashboard_df = create_dashboard_dataset(df)

    print(
        f"Dashboard dataset created: "
        f"{len(dashboard_df)} rows, {len(dashboard_df.columns)} columns"
    )

    # Display final columns
    print("\nFinal dashboard columns:")
    print(dashboard_df.columns.tolist())

    # Save final dashboard dataset
    dashboard_df.to_csv(OUTPUT_PATH, index=False)

    print(f"\nDashboard dataset saved to:")
    print(OUTPUT_PATH)

    print("\nProcessing completed successfully.")


if __name__ == "__main__":
    main()
