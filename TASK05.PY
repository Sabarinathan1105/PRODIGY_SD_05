import csv
import requests
from bs4 import BeautifulSoup

def scrape_amazon_best_sellers():
    url = "https://www.amazon.com/Best-Sellers/zgbs"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    products = []

    for item in soup.find_all("div", {"class": "a-section a-spacing-none p13n-asin"}):
        name = item.find("span", {"class": "p13n-sc-truncate"}).text.strip()
        price = item.find("span", {"class": "p13n-sc-price"}).text.strip()
        rating = item.find("span", {"class": "a-icon-alt"}).text.strip()

        products.append({"Name": name, "Price": price, "Rating": rating})

    return products

def save_to_csv(products):
    with open("amazon_best_sellers.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Name", "Price", "Rating"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for product in products:
            writer.writerow(product)

if __name__ == "__main__":
    products = scrape_amazon_best_sellers()
    save_to_csv(products)
    print("Scraping and saving completed.")
