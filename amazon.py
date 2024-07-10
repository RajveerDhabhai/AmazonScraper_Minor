import requests
from bs4 import BeautifulSoup
import pandas as pd

def search_amazon(product_name, num_pages=3):
    base_url = f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    all_products = []
    for page in range(1, num_pages + 1):
        url = base_url + f"&page={page}"
        print(f"Fetching page {page}...")
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        products = soup.find_all('div', {'data-component-type': 's-search-result'})

        for product in products:
            # Extracting product name
            name_tag = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'})
            if name_tag:
                name = name_tag.text.strip()
            else:
                name = 'Product name not found'

            # Extracting product price
            price_tag = product.find('span', {'class': 'a-price-whole'})
            if price_tag:
                price = price_tag.text.strip()
            else:
                price = 'Price not found'

            all_products.append({
                "name": name,
                "price": price
            })

    return all_products

def save_to_excel(products, file_name):
    df = pd.DataFrame(products)
    df.to_excel(file_name, index=False)
    print(f"Results saved to {file_name}")

if __name__ == "__main__":
    product_name = input("Enter the product you want to search on Amazon: ")
    num_pages_input = input("Enter the number of pages to fetch (default is 3): ")
    num_pages = int(num_pages_input) if num_pages_input.isdigit() else 3

    products = search_amazon(product_name, num_pages)
    file_name = f"{product_name.replace(' ', '_')}_results.xlsx"
    save_to_excel(products, file_name)
