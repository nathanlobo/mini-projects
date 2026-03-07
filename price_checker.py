import requests
from bs4 import BeautifulSoup
from collections import Counter
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_google_search_results(query):
    query = query.replace(' ', '+')
    url = f"https://www.google.com/search?q={query}&tbm=shop"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        return response.text
    return None

def parse_product_price(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Adjust the selector based on Google's actual structure
    prices = [price.get_text() for price in soup.find_all('span', class_='a8Pemb OFFNJ')]
    
    return prices

def check_product_price(product_name):
    html_content = get_google_search_results(product_name)
    if html_content:
        return parse_product_price(html_content)
    return []

def top_3_prices(prices):
    return Counter(prices).most_common(3)

def save_to_google_sheet(product, top_prices):
    # Use credentials to create a client to interact with the Google Drive API
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("price-checker-432510-4e7a46f841af.json", scope)
    client = gspread.authorize(creds)
    
    # Open the Google Sheet (create a new one if it doesn't exist)
    spreadsheet_name = "Top Prices"
    try:
        sheet = client.open(spreadsheet_name).sheet1
    except gspread.SpreadsheetNotFound:
        sheet = client.create(spreadsheet_name).sheet1

    # Find the next empty row
    next_row = len(sheet.get_all_values()) + 1
    
    # Write the data to the sheet
    sheet.update_cell(next_row, 1, product)
    for idx, (price, frequency) in enumerate(top_prices, start=1):
        sheet.update_cell(next_row, idx + 1, f'Price: {price}, Frequency: {frequency}')

def save_to_computer(product, top_3_prices_list):
    with open("Top Prices.txt", 'a', encoding='utf-8') as file:
        file.write(f"\nTop 3 common prices for {product}:\n")
        for price, frequency in top_3_prices_list:
            file.write(f'Price: {price}, Frequency: {frequency}\n')

def main():
    products = (
                # "100 gm amul butter",
                # "1 ltr amul milk",
                # "1 kg all-purpose flour",
                # "500 gm unsweetened natural cocoa powder",
                "1 kg sugar",
                # "100 gm baking soda",
                # "100 gm baking powder",
                # "1 kg salt",
                # "1 ltr vegetable oil",
                # "12 eggs",
                # "vanilla extract",
                # "buttermilk",
                )

    for product in products:
        print(f"Finding price for {product}...")
        prices = check_product_price(product)
        top_3_prices_list = top_3_prices(prices)
        # save_to_google_sheet(product, top_3_prices_list)
        save_to_computer(product, top_3_prices_list)
        print(f"Top 3 common prices for {product} have been saved")

main()