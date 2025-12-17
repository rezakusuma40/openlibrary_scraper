"""contains functions for input/output tasks"""

import json

import pandas as pd

def get_backup(output_path: str) -> list[dict]:
    """open output data as backup if available"""
    try:
        with open(f"{output_path}.json", "r", encoding="utf-8") as f:
            data: list[dict] = json.load(f)
        unscraped_count = sum(
            1 for data_dict in data 
            if not data_dict.get("is_scraped")
        )
        print(f"loaded {len(data)} books, {unscraped_count} books has not yet been scraped")
    except Exception:
        data: list[dict] = []
    return data

def save_to_csv(data: list[dict], output_path: str):
    """save scraped data to csv"""
    df = pd.DataFrame(data)
    df.to_csv(f'{output_path}.csv', index=False)
    
def save_to_json(data: list[dict], output_path: str):
    """save scraped data to json"""
    with open(f'{output_path}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
def save_to_html(html: str, output_path: str):
    """save an html object locally for easy testing/debugging"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
