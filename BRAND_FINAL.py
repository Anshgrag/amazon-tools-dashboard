from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from openpyxl import Workbook
from time import sleep

# === Chrome Setup ===
options = Options()
options.add_argument("--headless=new")  # Run in headless mode
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)

# === Read ASINs from File ===
with open("asins.txt", "r") as f:
    asins = [line.strip() for line in f if line.strip()]

# === Prepare Excel Workbook ===
wb = Workbook()
ws = wb.active
ws.title = "ASIN Brand Data"
ws.append(["ASIN", "Brand Name"])

# === Scrape Each ASIN ===
for asin in asins:
    url = f"https://www.amazon.de/dp/{asin}"
    print(f"Scraping ASIN: {asin}")
    driver.get(url)
    sleep(3)

    try:
        brand = driver.find_element(By.ID, "bylineInfo").text.strip()
    except NoSuchElementException:
        brand = "Not Found"

    print(f"→ Brand: {brand}")
    ws.append([asin, brand])

# === Finalize ===
driver.quit()
wb.save("asin_brands.xlsx")
print("\n✅ Done! Saved to asin_brands.xlsx")
