from bs4 import BeautifulSoup
import requests
import re


def clean_price(price_text):
    return ''.join([char.strip() for char in price_text if not re.search('[a-zA-Z]', char)])


def clean_price2(price_text):
    return float(''.join([char.strip() for char in price_text if not re.search('[^a-zA-Z0-9\s.]', char)]))

def scrape_stock_data(symbol, exchange):
    url = f"https://www.google.com/finance/quote/{symbol}:{exchange}"
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try: 
        response = requests.get(url, headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            current_price = soup.find("div", {"class", "kf1m0"}).get_text()
            stock_table = soup.find("div", {"class": "eYanAe"}) 
            stock_divs = stock_table.find_all("div")

            stocks = []
            
            for div in stock_divs:
                class_value = div.get("class")[0]
                if class_value == "gyFHrc":
                    stocks.append(div.find("div", class_="P6K39c").get_text())


            previous_close = clean_price(str(stocks[0]))
            daily_interval_high = clean_price(str(stocks[1])).split('-')[1]
            daily_interval_low = clean_price(str(stocks[1])).split('-')[0]
            week52_low = clean_price(str(stocks[2])).split('-')[0]
            week52_high = clean_price(str(stocks[2])).split('-')[1]
            market_cap = str(stocks[3])
            pe_ratio = clean_price(str(stocks[5]))
            
            if not len(pe_ratio):
                pe_ratio = "Na/Na"
            else:
                pass
            
            current_price, previous_close, daily_interval_high, daily_interval_low, week52_high, week52_low, market_cap, pe_ratio
            
            stock_response = {
                'current_price': current_price,
                'price_change': round(clean_price2(current_price) - clean_price2(previous_close) , 2),
                'percentage_change': round(((clean_price2(current_price)  - clean_price2(previous_close)) / clean_price2(previous_close)) * 100, 2),
                'previous_close':previous_close,
                'daily_interval_high':daily_interval_high,
                'daily_interval_low':daily_interval_low,
                'week52_high':week52_high,
                'week52_low':week52_low,
                'market_cap':market_cap,
                'pe_ratio':pe_ratio
            }
            
            return stock_response
    
    except Exception as e:
        # print(f'Error while scraping the data: {e}')
        return None