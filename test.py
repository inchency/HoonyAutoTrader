# 연습용 TEST 코드입니다.
import time
import pyupbit
import read_coin_name
import about_price
import use_access_key
import detect_burst_coin
import datetime
import selling_strategy

if __name__ == '__main__':
    print(read_coin_name.get_coin_name_json())
    print(read_coin_name.get_tickers())

    krw_xrp = about_price.CurrentPrice("KRW-XRP")
    btc_pci = about_price.CurrentPrice("BTC-PCI")

    btc_pci_price = btc_pci.get_current_price()
    krw_pci_price = btc_pci.get_krw_current_price()
    print("페이코인 가격 (BTC) : {}\n페이코인 가격(KRW) : {}".format(btc_pci_price, krw_pci_price))

    # 여러 가상화폐의 현재가를 한번에 조회
    all_tickers = read_coin_name.get_tickers()
    # KRW, BTC 구분없이 가격 조회
    all_tickers_price = about_price.CurrentPrice.get_coins_current_price(all_tickers)
    # BTC -> KRW로 변환
    all_tickers_krw_price = about_price.CurrentPrice.get_coins_krw_current_price(all_tickers)
    all_tickers_price
    print(all_tickers_krw_price)

    # 잔고 조회
    (access_key, secret_key) = use_access_key.read_key(use_access_key.JSON_PATH)
    upbit = pyupbit.Upbit(access_key, secret_key)
    print(upbit.get_balances())

    # TEMP
    # selling_strategy.selling_strategy(upbit = upbit, ticker="KRW-XRP", volume=539.68682505,
    #                                   avg_price=926, total_price=499750,
    #                                   sleep_sec=5)

    # 과거 데이터 조회
    df = pyupbit.get_ohlcv(ticker="KRW-XRP", interval="minute1", count=10)  # 리플을 분봉으로 현재시간으로부터 5분전까지 조회
    print(df)

    # 호가 조회
    orderbook = pyupbit.get_orderbook("KRW-XRP")
    print(orderbook)

    # 사자 (시장가 매수)
    # have_krw = upbit.get_balance("KRW")
    # upbit.buy_market_order("KRW-IQ", have_krw * 0.001)

    # 팔자 (시장가 매도)
    # coin_volume = upbit.get_balance("KRW-IQ") # 갖고 있는 수량 구하기
    # upbit.sell_market_order("KRW-IQ", coin_volume)

    # 급등주 찾기
    current_time = datetime.datetime.now()
    print("시작 시간 :", current_time)
    while True:
        try:
            # 30초 동안 1% 이상 오른 코인 검색
            detect_burst_coin_dict, detect_burst_coin_percent = detect_burst_coin.detect_brust_krw_coin(6, 5)
            # 현재 갖고 있는 코인 제외하기
            if "KRW-XRP" in detect_burst_coin_dict:
                detect_burst_coin_dict.pop("KRW-XRP")
            if "KRW-DOGE" in detect_burst_coin_dict:
                detect_burst_coin_dict.pop("KRW-DOGE")
            print(detect_burst_coin_dict)
            if (len(detect_burst_coin_dict) >= 1):
                print("급등주 발견!! 현재시각 : \n", datetime.datetime.now())
                print(detect_burst_coin_dict.keys())
                print(detect_burst_coin_dict)
                print(detect_burst_coin_percent)
                # 가장 등락률이 높은 코인 찾기
                sorted_dict = sorted(detect_burst_coin_percent.items(), reverse=True)
                buy_coin_ticker = sorted_dict[0][0]
                print("내가 매수한 코인 이름 :", buy_coin_ticker)
                try:
                    have_krw = upbit.get_balance("KRW")
                    total_buy_cost = have_krw * 0.3  # 현재 보유 KRW에서 매수 비중을 결정한다. ex) 100만원 보유시 0.01 은 1만원
                    if total_buy_cost > 5000:
                        upbit.buy_market_order(buy_coin_ticker, total_buy_cost)  # 매수 완료
                        # 매수한 코인 개수 구하기
                        buy_coin_cnt = upbit.get_balance(buy_coin_ticker)
                        # 매수 평단가 구하기
                        buy_avg_price = upbit.get_avg_buy_price(buy_coin_ticker)
                        # 매수 총 금액 구하기
                        buy_total_cost = upbit.get_amount(buy_coin_ticker)

                        selling_strategy.selling_strategy(upbit=upbit, ticker=buy_coin_ticker, volume=buy_coin_cnt,
                                                          avg_price=buy_avg_price, total_price=buy_total_cost,
                                                          sleep_sec=5)
                except Exception as e:
                    print(e)
                    time.sleep(1)
            else:
                print("현재 급등주가 발견되고 있지 않습니다.")
                print("경과시간 : ", datetime.datetime.now() - current_time)
            time.sleep(1)
        except Exception as e:
            print(e)
            time.sleep(1)