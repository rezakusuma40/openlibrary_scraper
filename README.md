# OpenLibrary Web Scraper

## 1. Chosen Website & Scraping Eligibility

This project scrapes publicly accessible book data from
`openlibrary.org`.\
The website is eligible for scraping because:

-   It does not require authentication for standard browsing.
-   Its [robots.txt]('https://openlibrary.org/robots.txt') file does not disallow scraping of any URL under https://openlibrary.org/books/, except for https://openlibrary.org/books/add, which is not scraped in this project.
- Additionally, the scraper applies sufficient delay between requests to avoid overloading the service.

## 2. Setup Instructions

1.  Install Python 3.11 or newer. (lesser versions are not yet tested)

2.  Clone the repository:

    ``` bash
    git clone <your-repo-url>
    cd <project-folder>
    ```

3.  Install dependencies:

    ``` bash
    pip install -r requirements.txt
    ```

No API keys or environment configuration are required.

## 3. Execution Command

Run the scraper through the module interface to ensure clean imports:

``` bash
python -m script.url_scraper
```

``` bash
python -m script.url_scraper
```

## 4. Dependencies

All required packages are listed in `requirements.txt`. This project
uses:

-   requests
-   beautifulsoup4
-   lxml (optional but faster)
-   python-dotenv (optional for configuration)

## 5. Notes on Challenges and Limitations

- Certain OpenLibrary pages omit fields such as publication dates, descriptions, or ratings. The scrapers handles these cases using safe fallbacks to avoid failures.

- The scrapers have only been tested on a limited set of pages; unusual or irregular page structures may still trigger parsing errors.

- The site does not seem to enforce strict rate-limiting (no 429 responses observed), but it does occasionally return 503 errors. This could stem from several factors including temporary server downtime or high traffic, especially since OpenLibrary is a popular target for web-scraping practice.