# Amazon ASIN Scraper Pro

A powerful desktop application for scraping Amazon product data using ASINs. Extract product titles, brands, prices, ratings, and images from multiple Amazon regions with a beautiful modern GUI.

## Features

### Core Functionality
- **Multi-Region Support**: Scrape from 10 Amazon regions (US, UK, Germany, France, Italy, Spain, Canada, Japan, India, Australia)
- **Flexible Input**: Load ASINs from Excel (.xlsx, .xls) or TXT files, or enter manually
- **Multi-threading**: Configure 1-10 threads for parallel scraping
- **Real-time Progress**: Live progress tracking and logging

### Selectable Data Fields
Choose exactly what data to scrape:
- Title
- Brand
- Price
- Rating
- Images

Quick select buttons for common combinations:
- Select All / Deselect All
- Only Images
- Only Prices
- Only Brands
- Brand + Price
- Price + Images

### Export Options
- Export to Excel (only includes selected fields)
- Download product images (organized by brand)
- Create ZIP archive of all images

## Installation

### Prerequisites
```bash
pip install pandas requests beautifulsoup4 pillow openpyxl lxml
```

### Running the Application
```bash
python amazon_asin_scraper_enhanced.py
```

## Usage Guide

### 1. Input Tab
- **Load from File**: Click "Browse" to select an Excel or TXT file containing ASINs, then click "Load ASINs"
- **Manual Input**: Enter ASINs directly in the text area (one per line), then click "Add Manual ASINs"
- View loaded ASINs in the table below

### 2. Scraping Tab
- **Select Data Fields**: Choose which product information to extract using checkboxes
- **Quick Select**: Use preset buttons for common field combinations
- **Configure Settings**:
  - Select Amazon region from dropdown
  - Set number of threads (1-10)
  - Set delay between requests (1-10 seconds)
- **Start/Stop**: Click "Start Scraping" to begin, "Stop Scraping" to halt
- Monitor progress in the log section

### 3. Results Tab
- View scraped data in the results table
- Export data to Excel
- Download images as ZIP file

### 4. Settings Tab
- Customize User-Agent header
- Set output directory
- Configure image download options

## Screenshots

### Main Interface
![Main Interface](https://raw.githubusercontent.com/Anshgrag/amazon-tools-dashboard/master/screenshot-main.png)

### Input Tab
![Input Tab](https://raw.githubusercontent.com/Anshgrag/amazon-tools-dashboard/master/screenshot-input.png)

### Scraping Tab - Field Selection
![Field Selection](https://raw.githubusercontent.com/Anshgrag/amazon-tools-dashboard/master/screenshot-fields.png)

### Scraping Tab - Configuration
![Configuration](https://raw.githubusercontent.com/Anshgrag/amazon-tools-dashboard/master/screenshot-config.png)

### Results Tab
![Results](https://raw.githubusercontent.com/Anshgrag/amazon-tools-dashboard/master/screenshot-results.png)

## Technical Details

### Dependencies
- **tkinter**: GUI framework (built-in with Python)
- **pandas**: Data handling and Excel export
- **requests**: HTTP requests
- **beautifulsoup4**: HTML parsing
- **pillow**: Image processing
- **openpyxl**: Excel file support
- **lxml**: XML/HTML parsing

### Output Structure
```
output/
├── amazon_scraped_data_20260302_123456.xlsx
├── amazon_product_images_20260302_123456.zip
└── images/
    ├── BrandName1/
    │   ├── ASIN1_1.jpg
    │   ├── ASIN1_2.jpg
    │   └── ...
    ├── BrandName2/
    │   └── ...
    └── ...
```

## Legal Disclaimer

This tool is for educational purposes only. Scraping Amazon may violate their Terms of Service. Use responsibly and at your own risk.

## License

MIT License
