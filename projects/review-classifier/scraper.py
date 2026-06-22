"""Scrape product reviews from a Flipkart product page into a CSV.

Run directly to scrape:  ``python scraper.py``
The scraping logic is wrapped in functions so the module can be imported
(e.g. by tests) without launching a browser.
"""

import csv

from playwright.sync_api import sync_playwright

URL_TEMPLATE = (
    "https://www.flipkart.com/boat-rockerz-110-40-hrs-playback-enx-technology-beast-mode-"
    "asap-charge-bluetooth/product-reviews/itm1707c9f88f559"
    "?pid=ACCGS9ZMGQZH4FZF&marketplace=FLIPKART&page={}"
)
PRODUCT_NAME = "Color Black • Microphone Yes"
REVIEW_XPATH = f"xpath=//div[text()='Review for: {PRODUCT_NAME}']/following-sibling::div//span"


def review_url(page_num: int) -> str:
    """Build the reviews URL for a given (1-based) page number."""
    return URL_TEMPLATE.format(page_num)


def scrape_reviews(pages: int = 10, timeout_ms: int = 3000) -> list[list[str]]:
    """Scrape `[product_name, review]` rows across the first `pages` pages."""
    rows: list[list[str]] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            for page_num in range(1, pages + 1):
                page.goto(review_url(page_num))
                page.wait_for_timeout(timeout_ms)
                review_elements = page.locator(REVIEW_XPATH)
                for i in range(review_elements.count()):
                    text = review_elements.nth(i).text_content()
                    if text:
                        rows.append([PRODUCT_NAME, text.strip()])
        finally:
            browser.close()
    return rows


def write_csv(rows: list[list[str]], path: str = "reviews.csv") -> None:
    """Write scraped rows to `path` with a header."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["product_name", "review"])
        writer.writerows(rows)


def main() -> None:
    rows = scrape_reviews()
    write_csv(rows)
    print("Total reviews:", len(rows))


if __name__ == "__main__":
    main()
