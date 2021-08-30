import about_price
import read_coin_name
import time


# total_count은 몇번 볼 것인지 sleep_sec은 몇 초간 쉴것인지
# total_count * sleep_sec 시간 동안 기다려야함
# ex total_count = 10, sleep_sec = 3 이라면 총 30초동안 10번의 거래 가격을 보게 됨
def detect_brust_krw_coin(total_count, sleep_sec):
    try:
        print("---detecting_burst_krw_coin---")
        all_tickers = read_coin_name.get_tickers()
        all_tickers_krw_price = dict()
        for i in range(0, total_count, 1):
            temp_dic = about_price.CurrentPrice.get_coins_current_price(all_tickers)
            while temp_dic is None:
                temp_dic = about_price.CurrentPrice.get_coins_current_price(all_tickers)
                time.sleep(1)
            new_dic = dict()
            # BTC는 제거하고 KRW로 살수 있는 코인만 남기기
            for ticker, price in temp_dic.items():
                if ticker.startswith("KRW"):
                    new_dic[ticker] = price
            for ticker, price in new_dic.items():
                if ticker in all_tickers_krw_price:
                    append_price_list = all_tickers_krw_price[ticker]
                    append_price_list.append(price)
                    all_tickers_krw_price[ticker] = append_price_list
                else:
                    all_tickers_krw_price[ticker] = [price]
            time.sleep(sleep_sec)
        # 계속 증가를 하는지 확인
        # candidate_burst_coin = dict()
        # for ticker, price_list in all_tickers_krw_price.items():
        #     fall_cnt = 0
        #     for i in range(0, len(price_list) - 1, 1):
        #         if price_list[i + 1] - price_list[i] < 0:
        #             fall_cnt = fall_cnt + 1
        #             if fall_cnt >= len(price_list) // 3: # 하락이 범위내의 1/3 이상을 차지하는지 확인
        #                 break
        #     else:  # for문을 정상적으로 다 돌면
        #         candidate_burst_coin[ticker] = price_list
        candidate_burst_coin = all_tickers_krw_price
        res_burst_coin = dict()
        res_burst_coin_percent = dict() # 등락률
        # 처음시작 가격과 마지막 가격의 등락률이 1.5% 이상일 경우
        for ticker, price_list in candidate_burst_coin.items():
            if (price_list[len(price_list) - 1] / price_list[0]) >= 1.0125:
                res_burst_coin[ticker] = price_list
                res_burst_coin_percent[ticker] = price_list[len(price_list) - 1] / price_list[0]
        return (res_burst_coin, res_burst_coin_percent)
    except Exception as e:
        print("error in selling_strategy")
        print(e)
        time.sleep(1)
