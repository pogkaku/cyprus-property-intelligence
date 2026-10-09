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


def analyze_price_by_district(df):
    """Calculate and visualize property prices by district."""

    price_by_district = (
        df.groupby("district")["price"]
        .agg(["count", "mean", "median", "min", "max"])
        .round(2)
        .sort_values("mean", ascending=False)
    )

    print("\nPrice by district:")
    print(price_by_district)

    # Plot average property price by district
    plt.figure(figsize=(10, 6))

    price_by_district["mean"].plot(
        kind="bar"
    )

    plt.title("Average Property Price by District")
    plt.xlabel("District")
    plt.ylabel("Average Price (€)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_path = OUTPUT_DIR / "average_price_by_district.png"
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"\nChart saved to: {output_path}")

    return price_by_district


def analyze_price_per_m2_by_district(df):
    """Calculate and visualize price per square metre by district."""

    price_per_m2_by_district = (
        df.groupby("district")["price_per_m2"]
        .agg(["count", "mean", "median", "min", "max"])
        .round(2)
        .sort_values("mean", ascending=False)
    )

    print("\nPrice per m² by district:")
    print(price_per_m2_by_district)

    # Plot average price per m² by district
    plt.figure(figsize=(10, 6))

    price_per_m2_by_district["mean"].plot(
        kind="bar"
    )

    plt.title("Average Property Price per m² by District")
    plt.xlabel("District")
    plt.ylabel("Average Price per m² (€)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_path = OUTPUT_DIR / "average_price_per_m2_by_district.png"
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"\nChart saved to: {output_path}")

    return price_per_m2_by_district


def analyze_price_vs_area(df):
    """Analyze the relationship between covered area and property price."""

    analysis_df = df[
        ["covered_area", "price"]
    ].dropna()

    correlation = analysis_df["covered_area"].corr(
        analysis_df["price"]
    )

    print("\nPrice vs covered area:")
    print(f"Pearson correlation: {correlation:.2f}")

    # Scatter plot
    plt.figure(figsize=(10, 6))

    plt.scatter(
        analysis_df["covered_area"],
        analysis_df["price"]
    )

    plt.title("Property Price vs Covered Area")
    plt.xlabel("Covered Area (m²)")
    plt.ylabel("Property Price (€)")
    plt.tight_layout()

    output_path = OUTPUT_DIR / "price_vs_covered_area.png"
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Chart saved to: {output_path}")

    return correlation


def analyze_distributions(df):
    """Analyze distributions and skewness of key numerical variables."""

    numerical_columns = [
        "price",
        "price_per_m2",
        "covered_area",
        "bedrooms",
        "bathrooms",
        "floor_number",
        "total_floor"
    ]

    skewness = (
        df[numerical_columns]
        .skew()
        .round(2)
        .sort_values(ascending=False)
    )

    print("\nSkewness of numerical variables:")
    print(skewness)

    # Create distribution plots
    for column in numerical_columns:

        data = df[column].dropna()

        if data.empty:
            continue

        plt.figure(figsize=(10, 6))

        plt.hist(data, bins=15)

        plt.title(f"Distribution of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.tight_layout()

        output_path = OUTPUT_DIR / f"{column}_distribution.png"
        plt.savefig(output_path, dpi=300)
        plt.close()

        print(f"Chart saved to: {output_path}")

    return skewness


def analyze_bedrooms_bathrooms(df):
    """Analyze property prices by bedrooms and bathrooms."""

    bedroom_analysis = (
        df.groupby("bedrooms")["price"]
        .agg(["count", "mean", "median"])
        .round(2)
    )

    bathroom_analysis = (
        df.groupby("bathrooms")["price"]
        .agg(["count", "mean", "median"])
        .round(2)
    )

    print("\nPrice by number of bedrooms:")
    print(bedroom_analysis)

    print("\nPrice by number of bathrooms:")
    print(bathroom_analysis)

    # Price by bedrooms
    plt.figure(figsize=(10, 6))

    bedroom_analysis["mean"].plot(kind="bar")

    plt.title("Average Property Price by Number of Bedrooms")
    plt.xlabel("Bedrooms")
    plt.ylabel("Average Price (€)")
    plt.xticks(rotation=0)
    plt.tight_layout()

    output_path = OUTPUT_DIR / "average_price_by_bedrooms.png"
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"\nChart saved to: {output_path}")

    # Price by bathrooms
    plt.figure(figsize=(10, 6))

    bathroom_analysis["mean"].plot(kind="bar")

    plt.title("Average Property Price by Number of Bathrooms")
    plt.xlabel("Bathrooms")
    plt.ylabel("Average Price (€)")
    plt.xticks(rotation=0)
    plt.tight_layout()

    output_path = OUTPUT_DIR / "average_price_by_bathrooms.png"
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Chart saved to: {output_path}")

    return bedroom_analysis, bathroom_analysis


def main():
    """Run the complete property analysis pipeline."""

    # Load data
    df = load_data()

    # Run analyses
    analyze_price_by_district(df)

    analyze_price_per_m2_by_district(df)

    analyze_price_vs_area(df)

    analyze_distributions(df)

    analyze_bedrooms_bathrooms(df)

    print("\nAll analyses completed successfully.")
    print(f"Analysis outputs saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
