import pyupbit

class CurrentPrice:
    def __init__(self, ticker):
        self.ticker = ticker

    def get_current_price(self):
        current_price = pyupbit.get_current_price(self.ticker)
        return current_price

    def get_krw_current_price(self):
        current_krw_btc = pyupbit.get_current_price("KRW-BTC")
        current_price = pyupbit.get_current_price(self.ticker)
        krw_current_price = current_krw_btc * current_price
        return krw_current_price

    # 여러 가상화폐의 현재가를 한번에 조회 (KRW, BTC 포함)
    def get_coins_current_price(coin_list):
       coins_price = pyupbit.get_current_price(coin_list)
       return coins_price

    # 여러 가상화폐의 현재가를 한번에 조회 (무조건 KRW로 변환)
    def get_coins_krw_current_price(coin_list):
        coins_price = pyupbit.get_current_price(coin_list)
        current_krw_btc = pyupbit.get_current_price("KRW-BTC")
        for ticker, price in coins_price.items():
            if ticker.startswith("BTC"):
                coins_price[ticker] = current_krw_btc * price
        return coins_price