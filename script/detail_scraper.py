import time
import traceback
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from requests import Session

from pkg import config, io, request

def scrape_details(session, all_books: list[dict]):
    """for scraping book data other than url"""
    for i, book_dict in enumerate(all_books):
        if book_dict['is_scraped'] is True:
            continue
        print(i, end= ' ')
        resp = request.retriable_requests(
            book_dict['source_url'],
            session,
            config.delay,
            config.max_retries,
            **config.session_kwargs
            )
        soup = BeautifulSoup(resp.content, 'html.parser')
        book_dict['title_alt'] = (
            soup.select_one(
                '.work-title'
                ).text
            )
        book_dict['image_url_alt'] = (
            f"https:{soup.select_one('.bookCover img')['src']}"
            .replace('https:https','https')
            )
        try:
            book_dict['description'] = (
                soup.select_one(
                    '.read-more__content'
                    ).get_text('',True)
                .split('Read more ▾')[0]
                )
        except (AttributeError, TypeError):
            book_dict['description'] = None
        try:
            book_dict['rating'] = (
                soup.select_one(
                    'meta[itemprop=ratingValue]'
                    )['content']
            )
        except (AttributeError, TypeError):
            book_dict['rating'] = None
        try:
            book_dict['published_date'] = (
                soup.select_one(
                    '[itemprop=datePublished]')
                .text
            )
        except (AttributeError, TypeError):
            book_dict['published_date'] = None
        book_dict['tags'] = [
            tag.text 
            for tag 
            in soup.select('.subjects a')
            ]
        book_dict['is_scraped'] = True
        time.sleep(config.delay)

def main():
    try:
        session = Session()
        all_books: list[dict] = io.get_backup(config.output_path)
        if not config.skip_scraped:
            for book_dict in all_books:
                book_dict['is_scraped'] = False
        start: float = time.perf_counter()
        scrape_details(session, all_books)
    except (Exception, KeyboardInterrupt) as e:
        print(f'\nError: {e}\nTraceback: {traceback.format_exc()}')
    finally:
        print(f'finished in {(time.perf_counter() - start):.2f} seconds')
        io.save_to_csv(all_books, config.output_path)
        io.save_to_json(all_books, config.output_path)
        
if __name__ == "__main__":
    main()