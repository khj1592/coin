import time
import pyupbit
import datetime
import numpy as np
import pandas as pd

secret = "jQpxoBJ8A6icKwv3e7dp1CDJuC8dVtZcRmLIOpSJ"          # 본인 값으로 변경
access = "LMotvxRJzCQH5XYc07fHrfWxRBy5xx52xcQ5TH1X"          # 본인 값으로 변경

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=3)
    time.sleep(0.1)
    target_price = df.iloc[2]['close'] + (df.iloc[2]['high'] - df.iloc[2]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    time.sleep(0.1)
    start_time = df.index[0]
    return start_time

def get_ma5_min5(ticker):
    """5분간격 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=5)
    time.sleep(0.1)
    ma5 = df['close'].rolling(5, min_periods=1).mean().iloc[4]
    return ma5

def get_ma5_min5_before(ticker):
    """5분간격 이전 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=6)
    time.sleep(0.1)
    ma5 = df['close'].rolling(5, min_periods=1).mean().iloc[4]
    return ma5

def get_ma5_min1(ticker):
    """10분간격 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=5)
    time.sleep(0.1)
    ma5 = df['close'].rolling(5, min_periods=1).mean().iloc[4]
    return ma5

def get_ma5_min1_before(ticker):
    """10분간격 이전 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=6)
    time.sleep(0.1)
    ma5 = df['close'].rolling(5, min_periods=1).mean().iloc[4]
    return ma5

def get_ma5_min3(ticker):
    """3분간격 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute3", count=5)
    time.sleep(0.1)
    ma5 = df['close'].rolling(5, min_periods=1).mean().iloc[4]
    return ma5

def get_ma5_min3_before(ticker):
    """3분간격 이전 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute3", count=6)
    time.sleep(0.1)
    ma5 = df['close'].rolling(5, min_periods=1).mean().iloc[4]
    return ma5


def get_balance(ticker):
    """해당 코인 몇개샀는지 조회 ex 0.37코인"""
    balances = upbit.get_balances()
    time.sleep(0.1)
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_Coins_money(ticker):
    """해당 코인 잔고 조회"""
    balances = upbit.get_balances()
    time.sleep(0.1)
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return (float(b['balance']) * float(b['avg_buy_price']))
            else:
                return 0
    return 0

def get_per(ticker):
    """수익률 조회"""
    balances = upbit.get_balances()
    time.sleep(0.1)
    for b in balances:
        if b['currency'] == ticker:
            avg_p = b['avg_buy_price']
            now_p = get_current_price("KRW-"+target[4:])
            return  now_p / float(avg_p)

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# def get_ror(target, k):
#     """가장 좋은 k값"""
#     df = pyupbit.get_ohlcv(target, interval="minute5", count=24)
#     df['range'] = (df['high'] - df['low']) * k
#     df['target'] = df['open'] + df['range'].shift(1)

#     fee = 0.0005
#     df['ror'] = np.where(df['high'] > df['target'],
#                          df['close'] / df['target'] - fee,
#                          1)

#     ror = df['ror'].cumprod()[-2]
#     return ror

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
coin_list = ["KRW-LINK", "KRW-NEO", "KRW-QTUM"]
coin_list2 = ["KRW-ZRX", "KRW-XRP", "KRW-BTG", "KRW-DAWN", "KRW-EOS", "KRW-FLOW", "KRW-BCH", "KRW-LTC", "KRW-NEO", "KRW-CHZ", "KRW-STPT", "KRW-QTUM", "KRW-STRK", "KRW-ADA", "KRW-BAT", "KRW-POLY"]

# 자동매매 시작
while True:
    try:
        k_m = 0
        ror_m = 0
        
        for target in coin_list:
            # for k in np.arange(0.1, 1.0, 0.1):
            #     ror = get_ror(target, k)
            #     if ror_m < ror:
            #         ror_m = ror
            #         k_m = k
            now = datetime.datetime.now()
            start_time = get_start_time(target)
            end_time = start_time + datetime.timedelta(days=1)
            btc = get_Coins_money(target[4:])
            ma5_3 = get_ma5_min3(target)
            ma5_3_before = get_ma5_min3_before(target)
            ma5_5 = get_ma5_min5(target)
            ma5_5_before = get_ma5_min5_before(target)
            ma5_1 = get_ma5_min1(target)
            ma5_1_before = get_ma5_min1_before(target)
            current_price = get_current_price(target)
            sell_val = get_balance(target[4:])
            print(target)

            if start_time < now < end_time - datetime.timedelta(seconds=120):
                target_price = get_target_price(target, 0.01)
                if target_price < current_price and ma5_1 < current_price and btc < 5000 and ma5_1 > ma5_1_before and current_price < target_price * 1.05 and ma5_3 < current_price and ma5_3 > ma5_3_before:
                    krw = get_balance("KRW")
                    if krw > 250000:
                        upbit.buy_market_order(target, 100000)
                    elif krw > 120000:
                        upbit.buy_market_order(target, 60000)
                    else:
                        upbit.buy_market_order(target, krw*0.9995)
            else:
                if sell_val != 0:
                    upbit.sell_market_order(target, sell_val)
                    krw = get_balance("KRW")
            
            if sell_val != 0 and btc >= 5000:
                per = get_per(target[4:])
                if per <= 0.90 or (ma5_1 <= ma5_1_before and ma5_1 > current_price):
                    print(target)
                    upbit.sell_market_order(target, sell_val)
                    krw = get_balance("KRW")

            time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)