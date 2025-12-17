# OpenLibrary Book Scraper

This project consists of two modular web scrapers designed to extract book data from [OpenLibrary.org](https://openlibrary.org/).

## Eligibility of Scraping

-   The site does not require authentication for standard browsing.  
-   Its [robots.txt](https://openlibrary.org/robots.txt) file does not disallow scraping of any URL under `https://openlibrary.org/books/`, except for `https://openlibrary.org/books/add`, which is not included in this project.  
-   Additionally, The scrapers apply sufficient delay between requests to avoid overloading the service.

## Project Structure

```
.
├── html/
│   ├── first_page.html       # saved HTML from first page's API requests, to ease debugging
│   └── other_page.html       # saved HTML from other page's API requests, to ease debugging
│
├── output/
│   ├── books.csv             # Final scraped results
│   └── books.json            # Final scraped results / backup
│
├── pkg/
│   ├── __pycache__
│   ├── request.py            # Contains functions that add extra functionalities to basic requests
│   ├── io.py                 # Contains functions for input/output tasks
│   └── config.py             # Adjustable business logic / settings
│
├── script/
│   ├── __pycache__
│   ├── url_scraper.py        # Collects book URLs
│   └── detail_scraper.py     # Scrapes details from each book URL
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Dependencies

- Python 3.11 or newer (older versions have not been tested, should work if not too old)
- All required libraries are listed in `requirements.txt`

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/rezakusuma40/openlibrary_scraper.git
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   ```
   **Windows**
   ```bash
   venv\Scripts\activate
   ```
   **macOS / Linux**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Setup configuration
   Before running any scraper, review and adjust config.py as needed.\
   The following variables may require additional explanation:
   - use_backup (applies to url_scraper.py only)\
     True: reuse an existing backup file if available; otherwise start from scratch.\
     False: always start a new scraping session and overwrite any existing backup.
   - skip_scraped (applies to detail_scraper.py only)\
     True: skip records where is_scraped = True, indicating the book has already been processed.\
     False: reset all is_scraped values to False and rescrape all book details from the beginning. Existing detail data is preserved until each book is reprocessed. Records with is_scraped = False indicate outdated data that may need to be refreshed.
   - use_cookies, use_headers, use_proxies, use_timeout\
     True: use user-defined values specified in config.py.\
     False: fall back to the default values provided by requests.Session().
   - save_html\
     True: saves the HTML fragments returned by the hidden API requests locally for debugging and inspection.

## Execution Commands

### 1. URL Scraper
Collects trending book URLs from [OpenLibrary](https://openlibrary.org/) pages and stores them in a JSON backup file.

```bash
python script/url_scraper.py
```

### 2. Detail Scraper
Reads the saved URLs, requests the URL to scrape book details, and outputs them to CSV and JSON.

```bash
python script/detail_scraper.py
```

These scripts rely on shared modules under `pkg/`:
- `request.py` — custom request wrapper + retry mechanism  
- `io.py` — file loading and saving utilities  
- `config.py` — central configuration hub  

## Challenges & Limitations

-   Some OpenLibrary pages lack fields such as publication dates, descriptions, or ratings. The scraper uses null-safe parsing to handle missing fields gracefully.
-   Only a small sample of pages was used for development; unusual or malformed pages may still trigger errors.
-   While the website does not appear to enforce strict rate-limiting (no 429 responses observed), it occasionally returns 503 errors. This can indicate temporary downtime or high traffic, which is expected since OpenLibrary is widely used for scraping practice.