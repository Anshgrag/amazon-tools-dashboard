import os
import time
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# === Configuration ===
ASIN_FILE = "asins.txt"
OUTPUT_DIR = "asin_images"
FAILED_FILE = "failed_asins.txt"
SUCCESS_FILE = "successful_asins.txt"
SKIPPED_FILE = "skipped_or_crashed_asins.txt"
DEBUG_HTML_DIR = "debug_pages"
HEADLESS = True
MAX_WORKERS = 4
TIMEOUT = 10

# === Lock for ChromeDriver init ===
driver_lock = Lock()

# === Setup undetected Chrome Driver ===
def get_chrome_driver():
    options = uc.ChromeOptions()
    if HEADLESS:
        options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Safari/537.36")

    # Your Chrome version is 138.x → use version_main=138
    with driver_lock:
        driver = uc.Chrome(options=options, version_main=138)
    return driver

# === Prepare Output Folders ===
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DEBUG_HTML_DIR, exist_ok=True)

# === Load ASINs ===
with open(ASIN_FILE, "r") as f:
    asins = [line.strip() for line in f if line.strip()]

# === Thread-safe shared lists ===
successful_asins = []
failed_asins = []
crashed_asins = []
lock = Lock()

# === Scrape Function ===
def scrape_image(asin):
    try:
        driver = get_chrome_driver()
        url = f"https://www.amazon.co.uk/dp/{asin}"
        print(f"[🔍] {asin}: Scraping...")

        try:
            driver.get(url)
            WebDriverWait(driver, TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Block check
            if "Robot Check" in driver.title or "To discuss automated access" in driver.page_source:
                raise Exception("Blocked by Amazon (CAPTCHA/Access Denied)")

            # Try primary and fallback image selectors
            try:
                img_element = driver.find_element(By.ID, "landingImage")
                img_url = img_element.get_attribute("src")
            except NoSuchElementException:
                try:
                    img_element = driver.find_element(By.CSS_SELECTOR, "#imgTagWrapperId img")
                    img_url = img_element.get_attribute("src") or img_element.get_attribute("data-old-hires")
                except NoSuchElementException:
                    raise Exception("Image element not found")

            if not img_url or "pixel" in img_url:
                raise Exception("Invalid or placeholder image")

            # Download image
            response = requests.get(img_url, timeout=10)
            img_path = os.path.join(OUTPUT_DIR, f"{asin}.jpg")
            with open(img_path, "wb") as f:
                f.write(response.content)

            print(f"[✅] {asin}: Image saved.")
            with lock:
                successful_asins.append(asin)

        except Exception as e:
            print(f"[❌] {asin}: Failed ({e})")
            with lock:
                failed_asins.append(asin)
            debug_path = os.path.join(DEBUG_HTML_DIR, f"{asin}.html")
            with open(debug_path, "w", encoding="utf-8") as f:
                f.write(driver.page_source)

        finally:
            driver.quit()

    except Exception as e_outer:
        print(f"[💥] {asin}: Crashed unexpectedly ({e_outer})")
        with lock:
            crashed_asins.append(asin)

# === Start Timer ===
start_time = time.time()

# === Run Threads ===
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = [executor.submit(scrape_image, asin) for asin in asins[:1000]]
    for future in as_completed(futures):
        pass

# === Write Logs ===
if successful_asins:
    with open(SUCCESS_FILE, "w") as f:
        for asin in successful_asins:
            f.write(asin + "\n")
    print(f"\n✅ Successful ASINs saved to '{SUCCESS_FILE}' ({len(successful_asins)} entries)")

if failed_asins:
    with open(FAILED_FILE, "w") as f:
        for asin in failed_asins:
            f.write(asin + "\n")
    print(f"🚫 Failed ASINs saved to '{FAILED_FILE}' ({len(failed_asins)} entries)")

if crashed_asins:
    with open(SKIPPED_FILE, "w") as f:
        for asin in crashed_asins:
            f.write(asin + "\n")
    print(f"⚠️ Crashed/Skipped ASINs saved to '{SKIPPED_FILE}' ({len(crashed_asins)} entries)")

# === Detect Any Unprocessed ASINs ===
processed_asins = set(successful_asins + failed_asins + crashed_asins)
missing_asins = [asin for asin in asins[:1000] if asin not in processed_asins]

if missing_asins:
    with open("missing_asins.txt", "w") as f:
        for asin in missing_asins:
            f.write(asin + "\n")
    print(f"🕵️ Unprocessed ASINs (not reached at all): {len(missing_asins)} → saved to 'missing_asins.txt'")

# === Total Time Output ===
end_time = time.time()
elapsed = end_time - start_time
minutes = int(elapsed // 60)
seconds = int(elapsed % 60)

print(f"\n🎉 All done! Images saved in '{OUTPUT_DIR}'.")
print(f"⏱️ Total time taken: {minutes} min {seconds} sec")
