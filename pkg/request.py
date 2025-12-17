"""contains functions that add extra functionalities to basic requests"""

import time

def retriable_requests(url, session, delay: int | float=3, max_retries: int =5, **session_kwargs):
    """wrapper for retrying failed requests, with incrementing delay for every consecutive failure"""
    for i in range(max_retries):
        try:
            print(url)
            return session.get(url, **session_kwargs)
        except Exception as e:
            print(f"scrape_url failed ({i+1}/{max_retries}): {e}")
            time.sleep(delay*(i+1)) # backoff
    raise Exception(f"failed after {max_retries} retries")