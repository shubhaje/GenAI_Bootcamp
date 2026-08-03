# Assignment Overview

This folder contains a small end-to-end text feature engineering workflow for product review analysis.

## Files

- `text_feature_engineering.ipynb` — main notebook for preprocessing, vocabulary creation, vectorization, and sentiment classification.
- `scraper.py` — real scraper for collecting product reviews from a Flipkart-style review page.
- `generate_dataset.py` — script to generate a synthetic review dataset matching the expected schema.
- `data/` — folder for datasets such as review CSV files.
- `screenshots/` — generated plots from the notebook.

## Getting Started

1. Install dependencies from the project root:
   ```bash
   pip install -r ../requirements.txt
   ```

2. Open the notebook:
   ```bash
   jupyter notebook text_feature_engineering.ipynb
   ```

## Running the Dataset Generators

### Generate a synthetic dataset
From this folder, run:
```bash
python generate_dataset.py
```

### Scrape live reviews
Run the scraper with a valid review-page URL:
```bash
python scraper.py --url "https://example.com/product-reviews" --pages 5 --out data/reviews_scraped.csv
```

## Expected Data Format

The notebook expects a CSV with at least these columns:

- `product_name`
- `rating`
- `review_text`
- `sentiment`

If you use a different filename or location, update the path in the notebook accordingly.

## Notes

- The notebook uses the dataset at `data/reviews.csv` by default.
- If you want to use scraped data, save it to the same location or adjust the notebook path.
- The screenshots folder is used to store charts produced during analysis.
