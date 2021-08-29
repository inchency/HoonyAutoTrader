# 연습용 TEST 코드입니다.
import time
import pyupbit
import read_coin_name
import about_price
import use_access_key
import detect_burst_coin
import datetime
import selling_strategy

(access_key, secret_key) = use_access_key.read_key(use_access_key.JSON_PATH)
upbit = pyupbit.Upbit(access_key, secret_key)
buy_coin_ticker = "KRW-IQ"
print("내가 매수한 코인 이름 :", buy_coin_ticker)

# 매수한 코인 개수 구하기
buy_coin_cnt = upbit.get_balance(buy_coin_ticker)
# 매수 평단가 구하기
buy_avg_price = upbit.get_avg_buy_price(buy_coin_ticker)
# 매수 총 금액 구하기
buy_total_cost = upbit.get_amount(buy_coin_ticker)
selling_strategy.selling_strategy(upbit=upbit, ticker=buy_coin_ticker, volume=buy_coin_cnt,
                                  avg_price=buy_avg_price, total_price=buy_total_cost,
                                  sleep_sec=5)