from playwright.sync_api import sync_playwright
import csv

url_template = "https://www.flipkart.com/boat-rockerz-110-40-hrs-playback-enx-technology-beast-mode-asap-charge-bluetooth/product-reviews/itm1707c9f88f559?pid=ACCGS9ZMGQZH4FZF&marketplace=FLIPKART&page={}"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    all_data = []

    for page_num in range(1, 11):
        url = url_template.format(page_num)
        page.goto(url)
        page.wait_for_timeout(3000)
        review_elements = page.locator(
            "xpath=//div[text()='Review for: Color Black • Microphone Yes']/following-sibling::div//span"
        )

        count = review_elements.count()

        for i in range(count):
            text = review_elements.nth(i).text_content()
            if text:
                all_data.append(["Color Black • Microphone Yes", text.strip()])

    browser.close()

# write CSV
with open("reviews.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["product_name", "review"])
    writer.writerows(all_data)

print("Total reviews:", len(all_data))