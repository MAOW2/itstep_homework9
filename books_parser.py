import csv
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


base_url = "http://books.toscrape.com/"
page_url = base_url
books = []

while page_url is not None:
    print("Завантажую сторінку:", page_url)

    response = requests.get(page_url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    book_cards = soup.select(".product_pod")

    for card in book_cards:
        title_tag = card.select_one("h3 a")
        price_tag = card.select_one(".price_color")
        availability_tag = card.select_one(".availability")

        if title_tag is None or price_tag is None or availability_tag is None:
            continue

        title = title_tag.get("title", "Без назви")
        price = price_tag.get_text(strip=True)
        availability = availability_tag.get_text(strip=True)

        books.append({
            "title": title,
            "price": price,
            "availability": availability
        })

    next_button = soup.select_one(".next a")

    if next_button is not None:
        next_href = next_button.get("href")

        if next_href is not None:
            page_url = urljoin(page_url, next_href)
        else:
            page_url = None
    else:
        page_url = None

for book in books:
    print("Назва:", book["title"])
    print("Ціна:", book["price"])
    print("Наявність:", book["availability"])
    print()

with open("books.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["title", "price", "availability"])
    writer.writeheader()
    writer.writerows(books)

print("Усього книг:", len(books))
print("Дані збережено у файл books.csv")