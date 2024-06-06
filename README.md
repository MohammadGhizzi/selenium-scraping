# Web Scrapper for Watch Data

## Description

This project is designed to scrape watch data from predefined collection URLs using Selenium and BeautifulSoup. The data is then saved into a CSV file and cleaned using Pandas.

And it's a project for a Data Engineering bootcamp, I'll update the code from time to time.

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

### Local Setup

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd scrapper
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

### Docker Setup

You can also run the Scrapper using Docker, which ensures a consistent environment without the need for manual setup.

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd scrapper
    ```

2. Build the Docker image:
    ```bash
    docker build -t Scrapper-image .
    ```

3. Run the Docker container using Docker Compose:
    ```bash
    docker-compose up
    ```

This will set up a Docker container with all the necessary dependencies and run the Scrapper.

## Usage

1. Update the `urls` list in `Scrapper.py` with the collection URLs for Harry Winston, making sure it’s a watch collection.
2. Run the Scrapper:
    ```bash
    python Scrapper.py
    ```
   If you are using Docker, the Scrapper will automatically run when the container starts.
3. After scraping is complete, run the data cleaning script:
    ```bash
    python cleaning.py
    ```
4. The cleaned data will be saved in `cleaned_data.csv`.

## How the Code Works

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
