import time
import about_price
import os
import use_access_key
import datetime


# avg_price : 평균단가
# total_price : 총 매수 금액
# sleep_sec : 몇 초마다 현재 가격을 check 할것인지
def selling_strategy(upbit, ticker, volume, avg_price, total_price, sleep_sec):
    try:
        sell_full_log = ""
        total_sell_price = 0  # 총 매도 금액
        sell_coin = about_price.CurrentPrice(ticker)
        break_flag = False
        while True:
            if break_flag:
                break
            time.sleep(sleep_sec)
            sell_coin_current_price1 = sell_coin.get_current_price()
            yield_price1 = sell_coin_current_price1 / avg_price  # 수익률 구하기
            print("({}) 코인\n판매 알고리즘 동작중 현재 수익률 0.98 초과 1.02 미만 현재 수익률 : {}\n 현재시각 : {}".format(ticker, yield_price1,
                                                                                               datetime.datetime.now()))
            if yield_price1 <= 0.985:  # -1.5퍼 이상이면 바로 손절하기
                res = upbit.sell_market_order(ticker, volume)
                while res is None:
                    time.sleep(1)
                    res = upbit.sell_market_order(ticker, volume)
                sell_coin_cur_price = sell_coin.get_current_price()
                total_sell_price = total_sell_price + sell_coin_cur_price * volume
                sell_full_log = sell_full_log + "현재가격 : {}, 수량 : {}, 총 {} 금액을 매도하였습니다.\n".format(sell_coin_cur_price,
                                                                                                 volume,
                                                                                                 total_sell_price)
                break
            elif yield_price1 >= 1.02:  # 수익률이 2프로가 넘어가면 시장가로 매수 수량의 1/3 익절
                res = upbit.sell_market_order(ticker, volume / 3)
                while res is None:
                    time.sleep(1)
                    res = upbit.sell_market_order(ticker, volume / 3)
                sell_coin_cur_price = sell_coin.get_current_price()
                total_sell_price = total_sell_price + sell_coin_cur_price * (volume / 3)
                cur_volume1 = upbit.get_balance(ticker)  # 남아있는 코인 수량 구하기
                print(res)
                print("2프로 수익나서 익절!!")
                sell_full_log = sell_full_log + "현재가격 : {}, 수량 : {}, 총 {} 금액을 매도하였습니다.\n".format(sell_coin_cur_price,
                                                                                                 volume,
                                                                                                 total_sell_price)
                while True:
                    if break_flag:
                        break
                    time.sleep(sleep_sec)
                    sell_coin_current_price2 = sell_coin.get_current_price()
                    yield_price2 = sell_coin_current_price2 / avg_price  # 수익률 구하기
                    print("({}) 코인\n판매 알고리즘 동작중 현재 수익률 1.01 초과 1.05 미만 현재 수익률 : {}\n 현재시각 : {}".format(ticker,
                                                                                                       yield_price2,
                                                                                                       datetime.datetime.now()))
                    if yield_price2 <= 1.01:  # 수익률이 1프로로 떨어지면 전량 매도
                        res = upbit.sell_market_order(ticker, cur_volume1)
                        while res is None:
                            time.sleep(1)
                            res = upbit.sell_market_order(ticker, cur_volume1)
                        sell_coin_cur_price = sell_coin.get_current_price()
                        total_sell_price = total_sell_price + sell_coin_cur_price * cur_volume1
                        sell_full_log = sell_full_log + "현재가격 : {}, 수량 : {}, 총 {} 금액을 매도하였습니다.\n".format(
                            sell_coin_cur_price, cur_volume1, total_sell_price)
                        break_flag = True
                        break
                    elif yield_price2 >= 1.05:  # 수익률이 5프로가 되면 현재 가지고 있는 수량의 1/2 익절
                        res = upbit.sell_market_order(ticker, cur_volume1 / 2)
                        while res is None:
                            time.sleep(1)
                            res = upbit.sell_market_order(ticker, cur_volume1 / 2)
                        cur_volume2 = upbit.get_balance(ticker)  # 남아있는 코인 수량 구하기
                        sell_coin_cur_price = sell_coin.get_current_price()
                        total_sell_price = total_sell_price + sell_coin_cur_price * (cur_volume1 / 2)
                        sell_full_log = sell_full_log + "현재가격 : {}, 수량 : {}, 총 {} 금액을 매도하였습니다.\n".format(
                            sell_coin_cur_price, cur_volume1, total_sell_price)
                        while True:
                            if break_flag:
                                break
                            time.sleep(sleep_sec)
                            sell_coin_current_price3 = sell_coin.get_current_price()
                            yield_price3 = sell_coin_current_price3 / avg_price  # 수익률 구하기
                            print("({}) 코인\n판매 알고리즘 동작중 현재 수익률 1.03 초과 1.1 미만 현재 수익률 : {}\n 현재시각 : {}".format(ticker,
                                                                                                              yield_price3,
                                                                                                              datetime.datetime.now()))
                            if yield_price3 <= 1.03:  # 수익률이 3프로로 떨어지면 전량 매도
                                res = upbit.sell_market_order(ticker, cur_volume2)
                                while res is None:
                                    time.sleep(1)
                                    res = upbit.sell_market_order(ticker, cur_volume2)
                                sell_coin_cur_price = sell_coin.get_current_price()
                                total_sell_price = total_sell_price + sell_coin_cur_price * cur_volume2
                                sell_full_log = sell_full_log + "현재가격 : {}, 수량 : {}, 총 {} 금액을 매도하였습니다.\n".format(
                                    sell_coin_cur_price, cur_volume2, total_sell_price)
                                break_flag = True
                                break
                            elif yield_price3 >= 1.1:  # 수익률이 10프로 넘어가면
                                while True:
                                    if break_flag:
                                        break
                                    time.sleep(sleep_sec)
                                    sell_coin_current_price4 = sell_coin.get_current_price()
                                    yield_price4 = sell_coin_current_price4 / avg_price  # 수익률 구하기
                                    print("({}) 코인\n판매 알고리즘 동작중 현재 수익률 1.05 초과 1.2 미만 현재 수익률 : {}\n 현재시각 : {}".format(
                                        ticker, yield_price4, datetime.datetime.now()))
                                    if yield_price4 <= 1.05:  # 수익률이 5프로로 떨어지면 전량 매도
                                        res = upbit.sell_market_order(ticker, cur_volume2)
                                        while res is None:
                                            time.sleep(1)
                                            res = upbit.sell_market_order(ticker, cur_volume2)
                                        sell_coin_cur_price = sell_coin.get_current_price()
                                        total_sell_price = total_sell_price + sell_coin_cur_price * cur_volume2
                                        sell_full_log = sell_full_log + "현재가격 : {}, 수량 : {}, 총 {} 금액을 매도하였습니다.\n".format(
                                            sell_coin_cur_price, cur_volume2, total_sell_price)
                                        break_flag = True
                                        break
                                    elif yield_price4 >= 1.2:  # 수익률이 20프로 넘어가면
                                        while True:
                                            if break_flag:
                                                break
                                            time.sleep(sleep_sec)
                                            sell_coin_current_price5 = sell_coin.get_current_price()
                                            yield_price5 = sell_coin_current_price5 / avg_price  # 수익률 구하기
                                            print(
                                                "({}) 코인\n판매 알고리즘 동작중 현재 수익률 1.1 초과 1.3 미만 현재 수익률 : {}\n 현재시각 : {}".format(
                                                    ticker, yield_price5, datetime.datetime.now()))
                                            if yield_price5 <= 1.1:  # 수익률이 10프로로 떨어지면 전량 매도
                                                res = upbit.sell_market_order(ticker, cur_volume2)
                                                while res is None:
                                                    time.sleep(1)
                                                    res = upbit.sell_market_order(ticker, cur_volume2)
                                                sell_coin_cur_price = sell_coin.get_current_price()
                                                total_sell_price = total_sell_price + sell_coin_cur_price * cur_volume2
                                                sell_full_log = sell_full_log + "현재가격 : {}, 수량 : {}, 총 {} 금액을 매도하였습니다.\n".format(
                                                    sell_coin_cur_price, cur_volume2, total_sell_price)
                                                break_flag = True
                                                break
                                            elif yield_price5 >= 1.3:  # 수익률이 30프로 넘어가면
                                                while True:
                                                    if break_flag:
                                                        break
                                                    time.sleep(sleep_sec)
                                                    sell_coin_current_price6 = sell_coin.get_current_price()
                                                    yield_price6 = sell_coin_current_price6 / avg_price  # 수익률 구하기
                                                    print(
                                                        "({}) 코인\n판매 알고리즘 동작중 현재 수익률 1.2 초과 1.5 미만 현재 수익률 : {}\n 현재시각 : {}".format(
                                                            ticker, yield_price6, datetime.datetime.now()))
                                                    if yield_price6 <= 1.2:  # 수익률이 20프로로 떨어지면 전량 매도
                                                        res = upbit.sell_market_order(ticker, cur_volume2)
                                                        while res is None:
                                                            time.sleep(1)
                                                            res = upbit.sell_market_order(ticker, cur_volume2)
                                                        sell_coin_cur_price = sell_coin.get_current_price()
                                                        total_sell_price = total_sell_price + sell_coin_cur_price * cur_volume2
                                                        sell_full_log = sell_full_log + "현재가격 : {}, 수량 : {}, 총 {} 금액을 매도하였습니다.\n".format(
                                                            sell_coin_cur_price, cur_volume2, total_sell_price)
                                                        break_flag = True
                                                        break
                                                    elif yield_price6 >= 1.5:  # 수익률이 50프로 넘어가면
                                                        while True:
                                                            if break_flag:
                                                                break
                                                            time.sleep(sleep_sec)
                                                            sell_coin_current_price7 = sell_coin.get_current_price()
                                                            yield_price7 = sell_coin_current_price7 / avg_price  # 수익률 구하기
                                                            print(
                                                                "({}) 코인\n판매 알고리즘 동작중 현재 수익률 1.35 초과 1.8 미만 현재 수익률 : {}\n 현재시각 : {}".format(
                                                                    ticker, yield_price7, datetime.datetime.now()))
                                                            if yield_price7 <= 1.35:  # 수익률이 35프로로 떨어지면 전량 매도
                                                                res = upbit.sell_market_order(ticker, cur_volume2)
                                                                while res is None:
                                                                    time.sleep(1)
                                                                    res = upbit.sell_market_order(ticker, cur_volume2)
                                                                sell_coin_cur_price = sell_coin.get_current_price()
                                                                total_sell_price = total_sell_price + sell_coin_cur_price * cur_volume2
                                                                sell_full_log = sell_full_log + "현재가격 : {}, 수량 : {}, 총 {} 금액을 매도하였습니다.\n".format(
                                                                    sell_coin_cur_price, cur_volume2, total_sell_price)
                                                                break_flag = True
                                                                break
                                                            elif yield_price7 >= 1.8:  # 수익률이 50프로 넘어가면
                                                                while True:
                                                                    if break_flag:
                                                                        break
                                                                    time.sleep(sleep_sec)
                                                                    sell_coin_current_price8 = sell_coin.get_current_price()
                                                                    yield_price8 = sell_coin_current_price8 / avg_price  # 수익률 구하기
                                                                    print(
                                                                        "({}) 코인\n판매 알고리즘 동작중 현재 수익률 1.6 초과 2.0 미만 현재 수익률 : {}\n 현재시각 : {}".format(
                                                                            ticker, yield_price8,
                                                                            datetime.datetime.now()))
                                                                    if yield_price8 <= 1.6:  # 수익률이 60프로로 떨어지면 전량 매도
                                                                        res = upbit.sell_market_order(ticker,
                                                                                                      cur_volume2)
                                                                        while res is None:
                                                                            time.sleep(1)
                                                                            res = upbit.sell_market_order(ticker,
                                                                                                          cur_volume2)
                                                                        sell_coin_cur_price = sell_coin.get_current_price()
                                                                        total_sell_price = total_sell_price + sell_coin_cur_price * cur_volume2
                                                                        sell_full_log = sell_full_log + "현재가격 : {}, 수량 : {}, 총 {} 금액을 매도하였습니다.\n".format(
                                                                            sell_coin_cur_price, cur_volume2,
                                                                            total_sell_price)
                                                                        break_flag = True
                                                                        break
                                                                    elif yield_price8 >= 2.0:  # 수익률이 100프로 넘어가면
                                                                        time.sleep(sleep_sec)
                                                                        sell_coin_current_price9 = sell_coin.get_current_price()
                                                                        yield_price9 = sell_coin_current_price9 / avg_price  # 수익률 구하기
                                                                        if yield_price9 <= 1.8:  # 수익률이 80프로로 떨어지면 전량 매도
                                                                            res = upbit.sell_market_order(ticker,
                                                                                                          cur_volume2)
                                                                            while res is None:
                                                                                time.sleep(1)
                                                                                res = upbit.sell_market_order(ticker,
                                                                                                              cur_volume2)
                                                                            sell_coin_cur_price = sell_coin.get_current_price()
                                                                            total_sell_price = total_sell_price + sell_coin_cur_price * cur_volume2
                                                                            sell_full_log = sell_full_log + "현재가격 : {}, 수량 : {}, 총 {} 금액을 매도하였습니다.\n".format(
                                                                                sell_coin_cur_price, cur_volume2,
                                                                                total_sell_price)
                                                                            break_flag = True
                                                                            break
                                                                        elif yield_price9 >= 2.5:  # 수익률이 150프로 넘어가면 전량 매도
                                                                            res = upbit.sell_market_order(ticker,
                                                                                                          cur_volume2)
                                                                            while res is None:
                                                                                time.sleep(1)
                                                                                res = upbit.sell_market_order(ticker,
                                                                                                              cur_volume2)
                                                                            sell_coin_cur_price = sell_coin.get_current_price()
                                                                            total_sell_price = total_sell_price + sell_coin_cur_price * cur_volume2
                                                                            sell_full_log = sell_full_log + "현재가격 : {}, 수량 : {}, 총 {} 금액을 매도하였습니다.\n".format(
                                                                                sell_coin_cur_price, cur_volume2,
                                                                                total_sell_price)
                                                                            break_flag = True
                                                                            break
                                                                        else:
                                                                            continue
                                                                    else:
                                                                        continue
                                                            else:
                                                                continue
                                                    else:
                                                        continue
                                            else:
                                                continue
                                    else:
                                        continue
                            else:  # 계속 존버
                                continue
                    else:  # 계속 존버
                        continue
            else:  # 계속 존버
                continue
        log_str = "정상 매도 완료! 코인명 : {}, 총 매수금액 : {}, 총 매도 금액 : {}, 수익률 : {}, 현재시간 : {}\n".format(ticker, total_price,
                                                                                                total_sell_price,
                                                                                                total_sell_price / total_price,
                                                                                                datetime.datetime.now())
        write_log = sell_full_log + log_str
        write_path = os.path.join(use_access_key.BASE_DIR, "sell_log.txt")
        print(log_str)
        with open(write_path, "at") as wtf:
            wtf.write(write_log)

    except Exception as e:  # 예외 발생하면 전량 매도
        print("error in selling_strategy")
        print(e)
        upbit.sell_market_order(ticker, volume)
        total_sell_price = total_sell_price + sell_coin.get_current_price() * volume
        log_str = "중간에 에러나서 매도 종료! 코인명 : {}, 총 매수금액 : {}, 총 매도 금액 : {}, 수익률 : {}, 현재시간 : {}\n".format(ticker,
                                                                                                      total_price,
                                                                                                      total_sell_price,
                                                                                                      total_sell_price / total_price,
                                                                                                      datetime.datetime.now())
        write_log = sell_full_log + log_str
        write_path = os.path.join(use_access_key.BASE_DIR, "sell_log.txt")
        print(log_str)
        with open(write_path, "at") as wtf:
            wtf.write(write_log)
