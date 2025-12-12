import json

import pandas as pd

from pkg import config

def get_backup():
    """open output data as backup if available"""
    try:
        with open(f"{config.output_path}.json", "r", encoding="utf-8") as f:
            all_books = json.load(f)
        print(f"loaded {len(all_books)} books")
    except Exception:
        all_books = []
    return all_books

def save_to_csv(all_books):
    """save scraped data to csv"""
    df = pd.DataFrame(all_books)
    df.to_csv(f'{config.output_path}.csv', index=False)
    
def save_to_json(all_books):
    """save scraped data to json"""
    with open(f'{config.output_path}.json', 'w', encoding='utf-8') as f:
        json.dump(all_books, f, ensure_ascii=False, indent=4)