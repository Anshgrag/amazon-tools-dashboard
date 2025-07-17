import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from openpyxl import Workbook

ZIP_CODE = "10001"  # US location

# === Setup Chrome Headless ===
options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)

# === Set ZIP Code to US ===
def set_zip_code():
    driver.get("https://www.amazon.com")
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "nav-global-location-popover-link"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "GLUXZipUpdateInput"))).send_keys(ZIP_CODE)
        driver.find_element(By.XPATH, '//span[@id="GLUXZipUpdate"]/span/input').click()
        time.sleep(2)
        try:
            driver.find_element(By.ID, "GLUXConfirmClose").click()
        except:
            pass
        time.sleep(2)
    except Exception as e:
        print(f"⚠️ ZIP code setup failed: {e}")

# === Get Price or Unavailability ===
def get_price():
    try:
        # Detect if the product is unavailable
        unavailable = driver.find_element(By.XPATH, '//span[contains(text(), "Currently unavailable")]')
        if unavailable:
            return "Currently unavailable"
    except NoSuchElementException:
        pass

    selectors = [
        (By.CSS_SELECTOR, 'span.a-price span.a-offscreen'),
        (By.ID, 'priceblock_ourprice'),
        (By.ID, 'priceblock_dealprice'),
        (By.ID, 'priceblock_saleprice'),
        (By.ID, 'price_inside_buybox'),
    ]
    for method, selector in selectors:
        try:
            element = driver.find_element(method, selector)
            price = element.text.strip()
            if price:
                return price
        except NoSuchElementException:
            continue
    try:
        whole = driver.find_element(By.CLASS_NAME, 'a-price-whole').text
        fraction = driver.find_element(By.CLASS_NAME, 'a-price-fraction').text
        return f"${whole}.{fraction}"
    except:
        return "Not Found"

# === Read ASINs ===
with open("asins.txt", "r") as f:
    asins = [line.strip() for line in f if line.strip()]

# === Excel Setup ===
wb = Workbook()
ws = wb.active
ws.title = "ASIN Prices"
ws.append(["ASIN", "Sale Price"])

# === Start ===
set_zip_code()

for asin in asins:
    url = f"https://www.amazon.com/dp/{asin}"
    print(f"🔍 Scraping: {asin}")
    driver.get(url)
    time.sleep(3)
    price = get_price()
    print(f"→ Result: {price}")
    ws.append([asin, price])

# === Save Output ===
driver.quit()
wb.save("asin_prices1.xlsx")
print("\n✅ Done! Output saved to asin_prices1.xlsx")
