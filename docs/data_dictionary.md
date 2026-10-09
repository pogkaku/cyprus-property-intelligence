# Cyprus Property Intelligence
## Data Dictionary

### Project Objective

This project collects publicly available Cyprus property listing data,
cleans and standardizes the data, performs analysis, and presents the
findings through an interactive Looker Studio dashboard.

---

## Property Dataset

| Field | Data Type | Description |
|---|---|---|
| property_id | string | Unique identifier assigned to the property |
| title | string | Original property listing title |
| property_type | categorical | Apartment, house, villa, land, etc. |
| city | categorical | Cyprus city |
| district | categorical | District or neighborhood |
| price | numeric | Property asking price |
| currency | string | Currency of the asking price |
| bedrooms | integer | Number of bedrooms |
| bathrooms | integer | Number of bathrooms |
| area_m2 | numeric | Property area in square metres |
| price_per_m2 | numeric | Asking price divided by property area |
| floor | string | Floor information |
| year_built | integer | Year property was constructed |
| furnished | categorical | Furnished, unfurnished, or unknown |
| parking | categorical | Parking availability |
| pool | categorical | Swimming pool availability |
| listing_url | string | Original listing URL |
| source | string | Website from which the listing was collected |
| scraped_at | datetime | Date and time the listing was collected |

---

## Data Quality Requirements

The pipeline should:

1. Detect duplicate listings.
2. Standardize property prices.
3. Standardize property areas.
4. Standardize categorical values.
5. Identify missing values.
6. Identify invalid numerical values.
7. Detect potential outliers.
8. Calculate price per square metre.
9. Preserve the original raw data.
10. Produce a clean dataset suitable for analysis.

---

## Derived Variables

### Price per Square Metre

```text
price_per_m2 = price / area_m2
