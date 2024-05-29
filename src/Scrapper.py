import asyncio
import aiohttp
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from asyncio import Semaphore
import logging

# Define the locators with both XPath and CSS selectors
locators = {
    "reference_number": {'xpath': '/html/body/div[2]/main/div/div[1]/div/div/div/div[2]/div/div/div[4]/div/p', 'css': '.pdp-header__product-description--product-number'},
    "watch_URL": None,
    "type": None,
    "brand": None,
    "year_introduced": None,
    "parent_model": {'xpath': '/html/body/div[2]/main/div/div[1]/div/div/div/div[2]/div/div/p/a'},
    "specific_model": {'xpath': '//*[@id="hw-content"]/div[1]/div/div/div/div[2]/div/div/h1/text()', 'css': '#hw-content > div.component.pdp-header.bg-color-light-off-white.content--full-width > div > div > div > div.pdp-header__column.col-12.col-md-5 > div > div > h1'},
    "nickname": {'xpath': '//*[@id="hw-content"]/div[1]/div/div/div/div[2]/div/div/h1/text()'},
    "marketing_name": {'css':'#hw-content > div.component.pdp-header.bg-color-light-off-white.content--full-width > div > div > div > div.pdp-header__column.col-12.col-md-5 > div > div > div.pdp-header__product-limited-edition'},
    "style": None,
    "currency": None,
    "price": None,
    "image_URL": {'xpath': '/html/body/div[2]/main/div/div[1]/div/div/div/div[1]/div/div/div/div[2]/ul/li[1]/img'},
    "made_in": None,
    "case_shape": None,
    "case_finish": None,
    "between_lugs": None,
    "lug_to_lug": None,
    "bezel_material": None,
    "bezel_color": None,
    "crystal": None,
    "weight": None,
    "dial_color": {'xpath': '/html/body/div[2]/main/div/div[5]/div/div/div/div/div[2]/div[3]/div[2]', 'css': 'div.pdp-timepiece-specifications__specs-section:nth-child(3) > div:nth-child(2)'},
    "numerals": None,
    "bracelet_material": {'xpath': '//*[@id="hw-content"]/div[5]/div/div/div/div/div[2]/div[3]/div[2]'},
    "bracelet_color": {'xpath': '//*[@id="hw-content"]/div[5]/div/div/div/div/div[2]/div[3]/div[2]'},
    "clasp_type": {'xpath': '/html/body/div[2]/main/div/div[5]/div/div/div/div/div[2]/div[4]/div[2]/div[3]/div/p'},
    "movement": {'xpath': '/html/body/div[2]/main/div/div[5]/div/div/div/div/div[2]/div[2]/div[2]/div[1]/div/p', 'css': 'div.pdp-timepiece-specifications__specs-section:nth-child(2) > div:nth-child(2) > div:nth-child(1)'},
    "caliber": {'xpath': '/html/body/div[2]/main/div/div[5]/div/div/div/div/div[2]/div[2]/div[2]/div[2]/div/p', 'css': 'div.pdp-timepiece-specifications__specs-section:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2)'},
    "power_reserve": None,
    "frequency": None,
    "jewels": None,
    "features": {'xpath': '/html/body/div[2]/main/div/div[5]/div/div/div/div/div[2]/div[2]/div[2]/div[3]', 'css': 'div.pdp-timepiece-specifications__specs-section:nth-child(2) > div:nth-child(2) > div:nth-child(3) > div:nth-child(2)'},
    "description": {'xpath':'//*[@id="hw-content"]/div[1]/div/div/div/div[2]/div/div/div[4]/p/text()'},
    "short_description": {'css': '#hw-content > div:nth-child(5) > div > div > div > div > div.pdp-timepiece-specifications__specs-wrapper.col-12.col-lg-10.offset-lg-1 > div:nth-child(5) > div.pdp-timepiece-specifications__specs-section-row > div:nth-child(1)'}
}

# Labels to be handled dynamically
label_value_pairs = {
    "Material": "case_material",
    "Dimensions": "diameter",
    "Height": "case_thickness",
    "Caseback": "caseback",
    "Type": "movement",
    "Caliber": "caliber",
    "Composition": "dial_color",
    "Material": "bracelet_material",
    "Buckle": "clasp_type",
    "Functions": "features",
    "Limited Edition": "description"
}
field_order = [
    "reference_number", "watch_URL", "type", "brand", "year_introduced", "parent_model", "specific_model",
    "nickname", "marketing_name", "style", "currency", "price", "image_URL", "made_in", "case_shape",
    "case_material", "case_finish", "caseback", "diameter", "between_lugs", "lug_to_lug", "case_thickness",
    "bezel_material", "bezel_color", "crystal", "water_resistance", "weight", "dial_color", "numerals",
    "bracelet_material", "bracelet_color", "clasp_type", "movement", "caliber", "power_reserve", "frequency",
    "jewels", "features", "description", "short_description"
]
# List of URLs
urls = [
    "https://www.harrywinston.com/en/products/high-jewelry-timepieces-by-harry-winston",
    "https://www.harrywinston.com/en/products/harry-winston-emerald-collection",
    "https://www.harrywinston.com/en/products/harry-winston-the-ocean-collection",
    "https://www.harrywinston.com/en/products/harry-winston-the-avenue-collection",
    "https://www.harrywinston.com/en/products/harry-winston-the-premier-collection",
    "https://www.harrywinston.com/en/products/harry-winston-midnight-collection",
    "https://www.harrywinston.com/en/products/histoire-de-tourbillon-and-opus"
]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')  # Recommended when images are disabled
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    #prefs = {
    #"profile.media_playback_requires_user_gesture": True,  # Disable media loading
    #"profile.default_content_settings.popups": 0  # Block pop-ups (optional)
#}
    #chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--disable-cache")
    chrome_options.add_argument("--disable-application-cache")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Function to handle ElementClickInterceptedException
def handle_intercepted_click(element, driver):
    try:
        element.click()
    except Exception as e:
        logger.warning(f"Exception: {e}. Clicking intercepted, scrolling and clicking again.")
        driver.execute_script("arguments[0].scrollIntoView();", element)
        driver.execute_script("arguments[0].click();", element)

# Function to scrape product URLs
def scrape_product_urls(driver):
    product_links = WebDriverWait(driver, 13).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'product__wrapper')))
    product_urls = [link.find_element(By.TAG_NAME, 'a').get_attribute('href') for link in product_links]
    return product_urls

def clear_browser_cache(driver):
    driver.delete_all_cookies()

# Function to extract data from HTML content
async def extract_data_from_html(html_content, url):
    soup = BeautifulSoup(html_content, 'html.parser')
    data = {}
    data["type"] = None
    data["brand"] = "Harry Winston"
    data["watch_URL"] = url

    # Extract image URL
    try:
        image_element = soup.select_one(locators["image_URL"]['css'])
        data["image_URL"] = image_element['src'] if image_element else None
    except:
        data["image_URL"] = None

    # Extract data based on labels
    for label, field in label_value_pairs.items():
        try:
            label_element = soup.find(text=label)
            if label_element:
                value_element = label_element.find_next()
                data[field] = value_element.text.strip() if value_element else None
            else:
                data[field] = None
        except:
            data[field] = None

    # Extract data based on predefined locators
    for field, locator in locators.items():
        if field not in label_value_pairs.values() and locator is not None:
            try:
                element = soup.select_one(locator['css'])
                data[field] = element.text.strip() if element else None
            except:
                data[field] = None

    # Extract water resistance value specifically
    try:
        elements = soup.find_all(text=lambda text: text and 'Water' in text)
        for element in elements:
            if "resistance" in element.lower():
                value_element = element.find_next()
                data["water_resistance"] = value_element.text.strip() if value_element else None
                break
        if "water_resistance" not in data:
            data["water_resistance"] = None
    except:
        data["water_resistance"] = None

    if "reference_number" in data and data["reference_number"]:
        ref_number = data["reference_number"]
        if "Product Reference:" in ref_number:
            data["reference_number"] = ref_number.split("Product Reference:")[1].strip()
    if "parent_model" in data and data["parent_model"]:
        parent_model = data["parent_model"]
        if "Harry Winston " in parent_model:
            data["parent_model"] = parent_model.split("Harry Winston ")[1].strip()
        else:
            data["parent_model"] = parent_model.strip()

    return data

async def fetch_product_page(session, url):
    try:
        async with session.get(url, timeout=15) as response:
            html_content = await response.text()
            return html_content
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return None

# Function to scrape product data asynchronously
async def scrape_product_data(url, sem, writer):
    async with sem:
        async with aiohttp.ClientSession() as session:
            html_content = await fetch_product_page(session, url)
            if html_content:
                product_data = await extract_data_from_html(html_content, url)
                writer.writerow(product_data)

# Function to scrape collection product URLs using a specific driver
async def scrape_collection_product_urls(collection_url, driver, sem):
    clear_browser_cache(driver)
    driver.get(collection_url)

    # Click the "LOAD MORE" button until it's not clickable anymore
    while True:
        try:
            load_more_button = WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.component.load-more input[type="button"]')))
            handle_intercepted_click(load_more_button, driver)
            await asyncio.sleep(7)  # Adjust sleep time as needed
        except Exception as e:
            logger.info(f"Exception or 'LOAD MORE' button not found: {e}")
            break

    # Scrape product URLs after loading all items
    product_urls = scrape_product_urls(driver)

    # If no product URLs found after loading, try scrolling down
    if not product_urls:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        await asyncio.sleep(3)  # Wait for lazy loading to complete, adjust sleep time as needed
        product_urls = scrape_product_urls(driver)

    return product_urls

# Function to scrape all products from a collection asynchronously
async def scrape_collection_products(collection_url, driver, sem, writer):
    product_urls = await scrape_collection_product_urls(collection_url, driver, sem)
    tasks = [scrape_product_data(product_url, sem, writer) for product_url in product_urls]
    await asyncio.gather(*tasks)

# Main function to scrape all URLs and write to CSV
async def main():
    sem = asyncio.Semaphore(30)  # Adjust this number as needed
    csv_file = "nyuyussxaasaryu.csv"
    drivers = [init_driver() for _ in range(len(urls))]
    
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=field_order)
        writer.writeheader()

        # Scrape each collection concurrently
        tasks = [scrape_collection_products(url, driver, sem, writer) for url, driver in zip(urls, drivers)]
        await asyncio.gather(*tasks)

    # Close all drivers
    for driver in drivers:
        driver.quit()

if __name__ == "__main__":
    now = time.time()
    asyncio.run(main())
    then = time.time()

    logger.info(f'Runtime: {then-now} seconds')
