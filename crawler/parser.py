from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re



def normalize_rating(raw: str) -> int:
    # on the site rating classes like "star-rating Three"
    mapping = {'One':1,'Two':2,'Three':3,'Four':4,'Five':5}
    return mapping.get(raw, 0)



def parse_book_page(html: str, base_url: str) -> dict:
    soup = BeautifulSoup(html, "lxml")
    title = soup.select_one("div.product_main > h1").text.strip()
    desc_el = soup.select_one("#product_description ~ p")
    description = desc_el.text.strip() if desc_el else ""
    category = soup.select_one("ul.breadcrumb li:nth-of-type(3) a").text.strip()
    # price table
    table = {th.text.strip(): td.text.strip() for th,td in 
             [(row.select_one("th"), row.select_one("td")) for row in soup.select("table.table.table-striped tr")]}
    def parse_price(p):
        if p:
            return float(re.sub(r'[£$,]', '', p))
        return 0.0
    price_excl = parse_price(table.get("Price (excl. tax)"))
    price_incl = parse_price(table.get("Price (incl. tax)"))
    availability = table.get("Availability") or ""
    num_reviews = int(table.get("Number of reviews", "0"))
    image_rel = soup.select_one("div.carousel-inner img") or soup.select_one("div.item.active img")
    image_url = urljoin(base_url, image_rel.get('src')) if image_rel else None
    rating_class = soup.select_one("p.star-rating")
    rating = 0
    if rating_class:
        classes = rating_class.get('class', [])
        for c in classes:
            if c != 'star-rating':
                rating = normalize_rating(c)
                break
    return {
        "source_url": base_url,
        "title": title,
        "description": description,
        "category": category,
        "price_excl_tax": price_excl,
        "price_incl_tax": price_incl,
        "availability": availability,
        "num_reviews": num_reviews,
        "image_url": image_url,
        "rating": rating
    }



def list_book_urls_from_listing(html: str):
    soup = BeautifulSoup(html, "lxml")
    anchors = soup.select("article.product_pod h3 a")
    urls = [urljoin("https://books.toscrape.com/catalogue/", a.get('href')) for a in anchors]

    return urls
