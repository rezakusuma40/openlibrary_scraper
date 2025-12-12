import os

# IO
output_folder = 'data'
html_folder = 'html'
os.makedirs(output_folder, exist_ok=True)
os.makedirs(html_folder, exist_ok=True)
output_file = 'books'
output_path = f'{output_folder}/{output_file}'

# run options
use_backup = 1 # 0 = False, 1 = True
skip_scraped = 1 # 0 = False, 1 = True
max_page = 80 # use any number lower than/not divisible by 20 if you want to scrape all page
use_cookies = 0 # 0 = False, 1 = True
use_headers = 0 # 0 = False, 1 = True
use_proxies = 0 # 0 = False, 1 = True
use_timeout = 1 # 0 = False, 1 = True

# rate limit handling
delay = 3
max_retries = 5

# debug/test
save_html = 0 # 0 = False, 1 = True

# requests customization
cookies = {}

headers = {
    'sec-ch-ua-platform': '"Windows"',
    'Referer': 'https://openlibrary.org/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
}

proxies = {}

timeout = 15