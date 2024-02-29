import pandas as pd 
import matplotlib.pyplot  as plt
import bt
import numpy as np
from datetime import datetime, timedelta

price_data = pd.read_csv('./data/SOL-USD.csv', index_col='Date', parse_dates=True)

sol_price = price_data[['Close']].rename(columns={"Close":"SOL"})

short_sma = sol_price.rolling(12).mean()
long_sma = sol_price.rolling(24).mean()

signal = long_sma.copy()
signal[long_sma.isnull()] = 0
signal[short_sma > long_sma] = 0
signal[long_sma > short_sma] = -1

strategy = bt.Strategy('Strategy',
                          [bt.algos.WeighTarget(signal),
                           bt.algos.Rebalance()])

benchmark = bt.Strategy('Buy and Hold',
                          [bt.algos.RunOnce(),
                           bt.algos.SelectAll(),
                           bt.algos.WeighEqually(),
                           bt.algos.Rebalance()])

bt_strategy = bt.Backtest(strategy, sol_price)
bt_benchmark = bt.Backtest(benchmark, sol_price)

bt_res = bt.run(bt_strategy, bt_benchmark)

bt_res.display()
bt_res.plot()
plt.show()

