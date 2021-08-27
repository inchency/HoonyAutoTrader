import requests
import pyupbit

URL = "https://api.upbit.com/v1/market/all"

def get_coin_name_json():
    res = requests.get(URL)
    return res.json()

def get_tickers():
    tickers = pyupbit.get_tickers()
    return tickers