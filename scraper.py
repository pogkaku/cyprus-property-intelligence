import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path


# --------------------------------------------------
# Website configuration
# --------------------------------------------------

headers = {
    "User-Agent": "Mozilla/5.0"
}

url = "https://index.cy/for-sale/"


# --------------------------------------------------
# Helper function
# --------------------------------------------------

# Some properties don't have floor numbers,
# so this avoids errors
def get_text_or_none(soup, selector):

    element = soup.select_one(selector)

    if element:
        return element.get_text(" ", strip=True)

    return None


# --------------------------------------------------
# Create a scraper
# --------------------------------------------------

def scrape_property(url):

    response = requests.get(
        url,
        headers=headers
    )

    soup = BeautifulSoup(
        response.content,
        "html.parser"
    )

    title = get_text_or_none(
        soup,
        ".lv2-title"
    )

    location = get_text_or_none(
        soup,
        ".lv2-meta-place"
    )

    property_id = get_text_or_none(
        soup,
        ".lv2-meta-id"
    )

    price = get_text_or_none(
        soup,
        ".lv2-price"
    )

    price_per_m2 = get_text_or_none(
        soup,
        ".lv2-ppm"
    )

    bedrooms = get_text_or_none(
        soup,
        '.lv2-fact[title^="Bedrooms"] strong'
    )

    bathrooms = get_text_or_none(
        soup,
        '.lv2-fact[title^="Bathrooms"] strong'
    )

    covered_area = get_text_or_none(
        soup,
        '.lv2-fact[title^="Covered area"] strong'
    )

    parking = get_text_or_none(
        soup,
        '.lv2-fact[title^="Parking"] strong'
    )

    floor = get_text_or_none(
        soup,
        '.lv2-fact[title^="Floor"] strong'
    )

    return {
        "property_id": property_id,
        "title": title,
        "location": location,
        "price": price,
        "price_per_m2": price_per_m2,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "covered_area": covered_area,
        "parking": parking,
        "floor": floor
    }


# --------------------------------------------------
# Main scraping process
# --------------------------------------------------

def main():

    print("Starting Cyprus property scraping...")

    # Request the property-for-sale page
    response = requests.get(
        url,
        headers=headers
    )

    if response.status_code == 200:
        print("successful")
    else:
        print(
            "failed:",
            response.status_code
        )
        return

    # Parse the page
    soup = BeautifulSoup(
        response.content,
        "html.parser"
    )

    # Find all sv2-track links
    property_links = soup.find_all(
        "a",
        class_="sv2-track"
    )

    print(
        "Number of property links:",
        len(property_links)
    )

    # Turn the links into a Python list
    property_urls = [
        link.get("href")
        for link in property_links
    ]

    print(
        "Number of urls:",
        len(property_urls)
    )

    # --------------------------------------------------
    # Run the scraper across all URLs
    # --------------------------------------------------

    properties = []

    for i, url in enumerate(
        property_urls,
        start=1
    ):

        property_data = scrape_property(url)

        properties.append(property_data)

        print(
            f"Scraped {i}/{len(property_urls)}"
        )

    # --------------------------------------------------
    # Create the raw property dataset
    # --------------------------------------------------

    df_properties = pd.DataFrame(properties)

    print("\nRaw property dataset:")
    print(df_properties)

    # --------------------------------------------------
    # Save the raw dataset
    # --------------------------------------------------

    output_path = Path(
        "data/raw/cyprus_properties_raw.csv"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df_properties.to_csv(
        output_path,
        index=False
    )

    print("\nRaw dataset saved to:")
    print(output_path)


if __name__ == "__main__":
    main()
