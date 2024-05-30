# Web Scraper for Watch Data

## Description

This project is designed to scrape watch data from predefined collection URLs using Selenium and BeautifulSoup. The data is then saved into a CSV file and cleaned using Pandas.

And its a project for Data Engineering bootcamp, ill update the code time to time.

## Features

- Scrapes data from multiple URLs asynchronously.
- Extracts specific details about watches such as reference number, brand, model, price, and more.
- Handles dynamic content loading by clicking 'LOAD MORE' buttons and scrolling.
- Cleans special characters and handles null values in the scraped data.

## Prerequisites

- Python 3.7+
- Google Chrome
- ChromeDriver

## Installation

1. Clone the repository:
    ```bash
    git clone 
    cd scrapper
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Update the `urls` list in `Scraper.py` with the collection URLs in Harry Winston, make sure its watches collection.
2. Run the scraper:
3. After scraping is complete, run the data cleaning script:
4. The cleaned data will be saved in `cleaned_data.csv`.

## How the Code Works
.
### URL Collection

The code collects product URLs from each collection page asynchronously to speed up the scraping process. It does this by:

1. **Initializing Multiple Drivers**: Multiple instances of Selenium WebDriver are created to handle different collection URLs simultaneously.
2. **Loading Collection Pages**: Each driver loads a collection page and clicks the "LOAD MORE" button until all products are visible.
3. **Extracting Product URLs**: The product URLs are collected and added to a list for further processing.

### Data Collection

Once the URLs are collected, the code:

1. **Asynchronously Fetches Product Pages**: Using `aiohttp`, the code fetches the HTML content of each product page concurrently.
2. **Extracts Data**: BeautifulSoup is used to parse the HTML and extract relevant data such as reference number, brand, model, price, etc.
3. **Writes Data to CSV**: The extracted data is written to a CSV file using the `csv` module.

### Data Cleaning

After data collection, the `cleaning.py` script:

1. **Reads the CSV File**: Loads the scraped data into a Pandas DataFrame.
2. **Cleans Special Characters**: Removes or replaces special characters from the data.
3. **Handles Null Values**: Fills null values with "N/A".
4. **Saves Cleaned Data**: Writes the cleaned data to a new CSV file.

## Logging

Logging is implemented to track the scraping process and handle exceptions. Adjust the logging level as needed.
