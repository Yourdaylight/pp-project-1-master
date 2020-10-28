# Functions to implement our trading strategy.
import numpy as np
import trading.process as proc
from trading.indicators import moving_average,oscillator
def random(stock_prices, period=7, amount=5000, fees=20, ledger='ledger_random.txt'):
    '''
    Randomly decide, every period, which stocks to purchase,
    do nothing, or sell (with equal probability).
    Spend a maximum of amount on every purchase.

    Input:
        stock_prices (ndarray): the stock price data
        period (int, default 7): how often we buy/sell (days)
        amount (float, default 5000): how much we spend on each purchase
            (must cover fees)
        fees (float, default 20): transaction fees
        ledger (str): path to the ledger file

    Output: None
    '''
    decision=['purchase','nothing','sell']
    stock_list=stock_prices[0,]
    portfolio=proc.create_portfolio([5000]*stock_prices.shape[1],stock_prices,fees)
    day=0
    while day<stock_prices.shape[0]:
        if day!=0 and (portfolio==np.zeros(len(portfolio))).all():
            break
        action = np.random.choice(decision)
        if action=="purchase":
            for stock in range(len(stock_list)):
                proc.buy(day,stock,amount,stock_prices,fees,portfolio,ledger)
        elif action=="nothing":
            continue
        elif action=="sell":
            for stock in range(len(stock_list)):
                proc.sell(day,stock,stock_prices,fees,portfolio,ledger)
        day+=1


def crossing_averages(stock_prices, n=50,m=200, amount=5000, fees=20, ledger='ledger_crossing_averages.txt'):
    '''
    When the FMA crosses the SMA from below, then the share price is starting to rise significantly, and it's a good time to buy shares.
    When the FMA crosses the SMA from above, then the share price is starting to lower significantly, and it's a good time to sell shares before the price gets too low.

    Input:
        stock_prices (ndarray): the stock price data
        n (int, default 50): FMA with period  𝑛
        m (int, default 200): SMA with period  m
        amount (float, default 5000): how much we spend on each purchase
            (must cover fees)
        fees (float, default 20): transaction fees
        ledger (str): path to the ledger file

    Output: None
    '''
    day = m
    portfolio = proc.create_portfolio([5000] * stock_prices.shape[1], stock_prices, fees)
    stock_list = stock_prices[0,]
    SMA=np.array([moving_average(stock_prices[:,i],m) for i in range(len(stock_list))])
    FMA=np.array([moving_average(stock_prices[:, i], n) for i in range(len(stock_list))])
    while day<(stock_prices.shape[0]-m):
        if day != 0 and (portfolio == np.zeros(len(portfolio))).all():
            break
        for stock in range(len(stock_list)):
            #When the FMA crosses the SMA from below,buy
            if FMA[stock][day]<SMA[stock][day]:
                proc.buy(day, stock, amount, stock_prices, fees, portfolio, ledger)
            else:
                proc.sell(day, stock, stock_prices, fees, portfolio, ledger)

        day += 1


def momentum(stock_prices,period=7,osc_type='stochastic',amount=5000, fees=20, ledger='ledger_momentum.txt'):
    '''
    Oscillators can help us guess if the price of a share is currently overvalued (overbought) or undervalued (oversold). Generally:

    the price is considered overvalued when the oscillator is above a threshold of 0.7 to 0.8 (good time to sell).
    the price is considered undervalued when the oscillator is below a threshold of 0.2 to 0.3 (good time to buy).

    '''
    day = period
    portfolio = proc.create_portfolio([5000] * stock_prices.shape[1], stock_prices, fees)
    stock_list = stock_prices[0,]

    valued= np.array([oscillator(stock_prices[:, i], period,osc_type) for i in range(len(stock_list))])
    while day < (stock_prices.shape[0] - period):
        if day != 0 and (portfolio == np.zeros(len(portfolio))).all():
            break
        for stock in range(len(stock_list)):
            # When the FMA crosses the SMA from below,buy
            if valued[stock][day]>0.2 and valued[stock][day]<0.3:
                proc.buy(day, stock, amount, stock_prices, fees, portfolio, ledger)
            elif valued[stock][day]>0.7 and valued[stock][day]<0.8:
                proc.sell(day, stock, stock_prices, fees, portfolio, ledger)
        day += 1
# from trading.data import get_data
# sim_data=get_data("read")[1:,]
# # test1=crossing_averages(sim_data)
# sd=sim_data[:,0][-1]
# test2=momentum(sim_data)





