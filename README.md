# Amazon Tools Dashboard

A collection of Selenium-based scraping tools for Amazon product data.

## Tools

### 1. Price Scraper (`backend/price.py`)
Scrapes product prices from Amazon.com
- Reads ASINs from `asins.txt`
- Sets US ZIP code for accurate pricing
- Outputs to `asin_prices1.xlsx`

### 2. Brand Scraper (`backend/brand.py`)
Scrapes brand names from Amazon.de
- Reads ASINs from `asins.txt`
- Outputs to `asin_brands.xlsx`

### 3. Photo Scraper (`backend/photo.py.py`)
Downloads product images from Amazon.co.uk
- Multi-threaded (4 workers)
- Saves images to `asin_images/` folder
- Tracks successful/failed ASINs in separate files

## Setup

```bash
cd backend
pip install -r requirements.txt
```

## Usage

1. Create `asins.txt` with one ASIN per line
2. Run desired script:
   ```bash
   python backend/price.py    # Price scraper
   python backend/brand.py    # Brand scraper
   python backend/photo.py.py # Image downloader
   ```

## Requirements

- Python 3.8+
- Chrome browser
- See `backend/requirements.txt` for Python dependencies
