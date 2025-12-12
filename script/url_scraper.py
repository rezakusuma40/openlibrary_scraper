import json
import time
import traceback
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bs4 import BeautifulSoup

from pkg import config, io, request

def scrape_url(book_tag, page, page_books):
    """for scraping book urls, with 2 other helper columns useful for webscraping process"""
    book_dict = {}
    book_dict['page'] = page
    book_dict['is_scraped'] = False
    book_dict['source_url'] = f"https://openlibrary.org{book_tag.a['href']}"
    # book_dict['title'] = book_tag.img['title']
    # book_dict['image_url'] = f"https:{book_tag.img['src']}"
    page_books.append(book_dict)    

def scrape_books(all_books):
    """for looping over pages. colllecting url via scrape_url()"""
    page = all_books[-1]['page'] + 20 if all_books else 0
    while page <= config.max_page:
        if page != 0:
            page_books = []
            page_url = 'https://openlibrary.org/partials.json?_component=CarouselLoadMore&queryType=SEARCH&q=trending_score_hourly_sum%3A%5B1+TO+*%5D+readinglog_count%3A%5B4+TO+*%5D+language%3Aeng+-subject%3A%22content_warning%3Acover%22+-subject%3A%22content_warning%3Acover%22&limit=20&page={page}&sorts=trending&subject=&pageMode=offset&hasFulltextOnly=false&secondaryAction=false&key=trending'
            # page_url = 'https://openlibrary.org/partials.json?_component=CarouselLoadMore&queryType=SEARCH&q=trending_score_hourly_sum%3A%5B1+TO+*%5D+readinglog_count%3A%5B4+TO+*%5D+language%3Aeng+-subject%3A%22content_warning%3Acover%22+-subject%3A%22content_warning%3Acover%22&limit=20&page=20&sorts=trending&subject=&pageMode=offset&hasFulltextOnly=false&secondaryAction=false&key=trending' # example, change page number to debug
            resp = request.retriable_requests(page_url.format(page=page))
            books = json.loads(resp.text)['partials']
            for book in books:
                if config.save_html:
                    with open(f'{config.html_folder}/next_page.html', 'w', encoding='utf-8') as f:
                        f.write(book)
                    config.save_html = False
                soup = BeautifulSoup(book, 'lxml')
                scrape_url(soup, page, page_books)
            all_books.extend(page_books)
            if len(books) < 20:
                break # < 20 books indicates last page
        else:
            page_books = []
            page_url = 'https://openlibrary.org/partials.json?_component=LazyCarousel&query=trending_score_hourly_sum%3A%5B1+TO+*%5D+readinglog_count%3A%5B4+TO+*%5D+language%3Aeng+-subject%3A%22content_warning%3Acover%22&sort=trending&key=trending&limit=20&search=false&has_fulltext_only=false&layout=carousel&fallback=false&title=Trending+Books'
            resp = request.retriable_requests(page_url)
            resp = json.loads(resp.text)['partials']
            if config.save_html:
                with open(f'{config.html_folder}/first_page.html', 'w', encoding='utf-8') as f:
                    f.write(resp)
            soup = BeautifulSoup(resp, 'lxml')
            books = soup.select('.book-cover')
            for book in books:
                scrape_url(book, 0, page_books)
            all_books.extend(page_books)
        time.sleep(config.delay)
        page += 20

if __name__ == "__main__":
    try:
        all_books = io.get_backup() if config.use_backup else []
        start = time.perf_counter()
        scrape_books(all_books)
    except (Exception, KeyboardInterrupt) as e:
        print(f'\nError: {e}\nTraceback: {traceback.format_exc()}')
    finally:
        print(f'finished in {(time.perf_counter() - start):.2f} seconds')
        io.save_to_json(all_books)