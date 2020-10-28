import numpy as np

def moving_average(stock_price, n=7, weights=[]):
    '''
    Calculates the n-day (possibly weighted) moving average for a given stock over time.

    Input:
        stock_price (ndarray): single column with the share prices over time for one stock,
            up to the current day.
        n (int, default 7): period of the moving average (in days).
        weights (list, default []): must be of length n if specified. Indicates the weights
            to use for the weighted average. If empty, return a non-weighted average.

    Output:
        ma (ndarray): the n-day (possibly weighted) moving average of the share price over time.
    '''
    if weights ==[]:
        weights=np.ones(n)/n
    ma=np.convolve(weights,stock_price)[n-1:-n+1]
    return ma

def oscillator(stock_price, n=7, osc_type='stochastic'):
    '''
    Calculates the level of the stochastic or RSI oscillator with a period of n days.

    Input:
        stock_price (ndarray): single column with the share prices over time for one stock,
            up to the current day.
        n (int, default 7): period of the moving average (in days).
        osc_type (str, default 'stochastic'): either 'stochastic' or 'RSI' to choose an oscillator.

    Output:
        osc (ndarray): the oscillator level with period $n$ for the stock over time.
    '''
    res=[]
    count = n
    if osc_type=="stochastic":
        for stock in stock_price[n:]:
            period=stock_price[count-n:count]
            max_price=max(period)
            min_price=min(period)
            delta=stock-min_price
            delta_max=max_price-min_price
            stochastic=delta/delta_max
            res.append(stochastic)
            count+=1

    if osc_type=="RSI":
        for stock in stock_price[n:]:
            #Calculate all the price differences on consecutive days over the past  𝑛  days.
            period=stock_price[count-n:count]
            period=np.diff(period)
            #Separate the positive differences from the negative differences.
            positive=period[np.where(period>0)]
            negative=period[np.where(period<0)]
            #Calculate the average of all the positive differences, and the absolute value of the average of all the negative differences.
            pos_ave=np.average(positive)
            neg_ave=abs(np.average(negative))
            #Calculate the ratio between these 2 averages (positive/negative)
            RS=pos_ave/neg_ave
            RSI=1-(1/(1+RS))
            res.append(RSI)
            count+=1
    return np.array(res)
if __name__=="__main__":
    data=np.loadtxt("./stock_data_5y.txt")
    look=data[:,0]
    ma=moving_average(look,250)
    sto=oscillator(look,osc_type="stochastic")
    rsi=oscillator(look,osc_type="RSI")
    decision=['purchase','nothing','sell']
    action=np.random.choice(decision)
    judge=np.array([0,0,0,0,0])
    test=np.zeros(len(judge))
    print((judge==test).all())





