import requests, os
from dotenv import load_dotenv

def get_stock_price(ticker):
    url = f"https://api.twelvedata.com/price?symbol={ticker}&apikey={os.getenv('stock_key')}"
    result = requests.get(url).json()
    
    return result

load_dotenv()