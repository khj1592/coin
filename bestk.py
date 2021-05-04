import pyupbit
import numpy as np


def get_ror(k=0.5):
    df = pyupbit.get_ohlcv("KRW-BTC", count = 7)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    fee = 0.0005
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'] - fee,
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror

def opt_k():
    k_m = 0
    ror_m = 0

    for k in np.arange(0.1, 1.0, 0.1):
        ror = get_ror(k)
        if ror_m < ror:
            ror_m = ror
            k_m = k
    
    return k
        
    
print(opt_k())