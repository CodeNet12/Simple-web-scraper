import requests
from bs4 import BeautifulSoup
import pandas as pd

# Target URL (Change 'laptop' to any keyword you want)
url = "https://www.amazon.com/s?k=laptop"

# User-Agent header to mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# List to hold extracted product data
products = []

# Send HTTP request to the URL
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# Find all product containers
items = soup.find_all("div", {"data-component-type": "s-search-result"})

# Loop through each product item
for item in items:
    try:
        # Extract product name
        title = item.h2.text.strip()

        # Extract product link
        link = "https://www.amazon.com" + item.h2.a["href"]

        # Extract price (whole and fraction)
        price_whole = item.find("span", class_="a-price-whole")
        price_fraction = item.find("span", class_="a-price-fraction")
        price = f"{price_whole.text}.{price_fraction.text}" if price_whole and price_fraction else "N/A"

        # Extract rating
        rating_tag = item.find("span", class_="a-icon-alt")
        rating = rating_tag.text if rating_tag else "No rating"

        # Extract image URL
        image_tag = item.find("img", class_="s-image")
        image_url = image_tag["src"] if image_tag else "No image"

        # Append to product list
        products.append({
            "Product Name": title,
            "Price": price,
            "Rating": rating,
            "Product Link": link,
            "Image URL": image_url
        })

    except Exception as e:
        print(f"Error while processing a product: {e}")
        continue

# Create a DataFrame and export to Excel
df = pd.DataFrame(products)
df.to_excel("products.xlsx", index=False)
print("Product data saved to 'products.xlsx'")

