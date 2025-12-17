"""a central file for storing adjustable variables affecting runtime behavior"""

import os
from typing import Literal

Binary = Literal[0, 1, True, False]

# IO
output_folder: str = 'output'
html_folder: str = 'html'
os.makedirs(output_folder, exist_ok=True)
os.makedirs(html_folder, exist_ok=True)
test_prefix: str = '' # use no prefix when on production
# test_prefix: str = 'test_' # use any prefix for testing, comment if not testing
output_file: str = f'{test_prefix}books'
first_html: str = f'{test_prefix}first_page'
other_html: str = f'{test_prefix}other_page'
output_path: str = f'{output_folder}/{output_file}'
first_html_path: str = f'{html_folder}/{first_html}.html'
other_html_path: str = f'{html_folder}/{other_html}.html'

# run options
use_backup: Binary = 1 # 0 = False, 1 = True
skip_scraped: Binary = 1 # 0 = False, 1 = True
max_page: int = 40 # stop scraping until reaching this number. use very large number if you want to scrape all page
use_cookies: Binary = 0 # 0 = False, 1 = True
use_headers: Binary = 0 # 0 = False, 1 = True
use_proxies: Binary = 0 # 0 = False, 1 = True
use_timeout: Binary = 1 # 0 = False, 1 = True

# rate limit handling
delay: int | float = 3
max_retries: int = 5

# debug/test
save_html: Binary = 0 # 0 = False, 1 = True

# requests customization
cookies: dict = {}

headers: dict = {
    'sec-ch-ua-platform': '"Windows"',
    'Referer': 'https://openlibrary.org/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
}

proxies: dict = {}

timeout: int | float = 15

session_kwargs: dict = {}
if use_cookies:
    session_kwargs['cookies'] = cookies
if use_headers:
    session_kwargs['headers'] = headers
if use_proxies:
    session_kwargs['proxies'] = proxies
if use_timeout:
    session_kwargs['timeout'] = timeout