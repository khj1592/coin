import time
import pyupbit
import datetime
import numpy as np
import pandas as pd

secret = "jQpxoBJ8A6icKwv3e7dp1CDJuC8dVtZcRmLIOpSJ"          # 본인 값으로 변경
access = "LMotvxRJzCQH5XYc07fHrfWxRBy5xx52xcQ5TH1X"          # 본인 값으로 변경

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=3)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_Coins_money(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return (b['balance'] * b['avg_buy_price'])
            else:
                return 0
    return 0

def get_per(ticker):
    """수익률 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            avg_p = b['avg_buy_price']
            now_p = get_current_price("KRW-"+target[4:])
            return float(avg_p) / now_p

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

def get_ror(target, k):
    df = pyupbit.get_ohlcv(target, count = 7)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    fee = 0.0005
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'] - fee,
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
krw = get_balance("KRW")



# 자동매매 시작
while True:
    try:
        k_m = 0
        ror_m = 0
        coin_list = ["KRW-ETH", "KRW-DOGE", "KRW-ETC", "KRW-BTT", "KRW-WAVES", "KRW-SXP", "KRW-VET", "KRW-SRM", "KRW-TRX", "KRW-LINK", "KRW-ZRX"]
        
        for target in coin_list:
            # for k in np.arange(0.1, 1.0, 0.1):
            #     ror = get_ror(target, k)
            #     if ror_m < ror:
            #         ror_m = ror
            #         k_m = k
            k_m = 0.5
            now = datetime.datetime.now()
            start_time = get_start_time(target)
            end_time = start_time + datetime.timedelta(days=1)
            btc = get_balance(target[4:])

            if start_time < now < end_time - datetime.timedelta(seconds=120):
                target_price = get_target_price(target, k_m)
                ma15 = get_ma15(target)
                current_price = get_current_price(target)
                if target_price < current_price and ma15 < current_price and btc < 5000:
                    if krw > 5000:
                        upbit.buy_market_order(target, krw*0.1995)
            else:
                if btc != 0:
                    upbit.sell_market_order(target, btc*0.9995)
            
            if btc != 0:
                per = get_per(target[4:])
                if per <= 0.95 or per >= 1.05:
                    upbit.sell_market_order(target, btc*0.9995)

            time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)