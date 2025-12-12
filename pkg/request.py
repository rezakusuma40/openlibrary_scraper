import time

from requests import Session

from pkg import config

session = Session()

def modified_requests(url, session):
    """requests with modifiable parameter via config.py for easy testing"""
    print(url)
    resp = session.get(
        url,
        cookies = config.cookies if config.use_cookies else session.cookies,
        headers = config.headers if config.use_headers else session.headers,
        proxies = config.proxies if config.use_proxies else session.proxies,
        timeout = config.timeout if config.use_timeout else session.timeout,
        )
    return resp

def retriable_requests(url):
    """for retrying failed requests, with incrementing delay for every consecutive failure"""
    for i in range(config.max_retries):
        try:
            return modified_requests(url, session)
        except Exception as e:
            print(f"scrape_url failed ({i+1}/{config.max_retries}): {e}")
            time.sleep(config.delay*(i+1)) # backoff
    raise Exception(f"failed after {config.max_retries} retries")