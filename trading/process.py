# Functions to process transactions.
import numpy as np

def log_transaction(transaction_type, date, stock, number_of_shares, price, fees, ledger_file):
    '''
    Record a transaction in the file ledger_file. If the file doesn't exist, create it.
    
    Input:
        transaction_type (str): 'buy' or 'sell'
        date (int): the date of the transaction (nb of days since day 0)
        stock (int): the stock we buy or sell (the column index in the data array)
        number_of_shares (int): the number of shares bought or sold
        price (float): the price of a share at the time of the transaction
        fees (float): transaction fees (fixed amount per transaction, independent of the number of shares)
        ledger_file (str): path to the ledger file
    
    Output: returns None.
        Writes one line in the ledger file to record a transaction with the input information.
        This should also include the total amount of money spent (negative) or earned (positive)
        in the transaction, including fees, at the end of the line.
        All amounts should be reported with 2 decimal digits.

    Example:
        Log a purchase of 10 shares for stock number 2, on day 5. Share price is 100, fees are 50.
        Writes the following line in 'ledger.txt':
        buy,5,2,10,100.00,-1050.00
            >>> log_transaction('buy', 5, 2, 10, 100, 50, 'ledger.txt')
    '''
    total = number_of_shares * price
    print("shares:",number_of_shares,"price:",price)

    log_info="{},{},{},{},{},".format(transaction_type,date,stock,number_of_shares,price)

    if transaction_type=="buy":
        total+=fees
        log_info=log_info+str(-total)+"\n"
    elif transaction_type=="sell":
        total-=fees
        if total<0:
            log_info = log_info + str(-total) + "\n"
        else:
            log_info=log_info+"+"+str(total)+"\n"
    with open(ledger_file,'a+') as f:
        f.write(log_info)
        f.close()



def buy(date, stock, available_capital, stock_prices, fees, portfolio, ledger_file):
    '''
    Buy shares of a given stock, with a certain amount of money available.
    Updates portfolio in-place, logs transaction in ledger.
    
    Input:
        date (int): the date of the transaction (nb of days since day 0)
        stock (int): the stock we want to buy
        available_capital (float): the total (maximum) amount to spend,
            this must also cover fees
        stock_prices (ndarray): the stock price data
        fees (float): total transaction fees (fixed amount per transaction)
        portfolio (list): our current portfolio
        ledger_file (str): path to the ledger file
    
    Output: None

    Example:
        Spend at most 1000 to buy shares of stock 7 on day 21, with fees 30:
            >>> buy(21, 7, 1000, sim_data, 30, portfolio)
    '''
    #calculate the price today
    price=stock_prices[date][stock]
    if np.isnan(price):
        return
    #calculate the shares we would buy
    shares=int((available_capital-fees)/price)
    portfolio[stock]+=shares
    #record the transaction
    log_transaction("buy",date,stock,shares,price,fees,ledger_file)



def sell(date, stock, stock_prices, fees, portfolio, ledger_file):
    '''
    Sell all shares of a given stock.
    Updates portfolio in-place, logs transaction in ledger.
    
    Input:
        date (int): the date of the transaction (nb of days since day 0)
        stock (int): the stock we want to sell
        stock_prices (ndarray): the stock price data
        fees (float): transaction fees (fixed amount per transaction)
        portfolio (list): our current portfolio
        ledger_file (str): path to the ledger file
    
    Output: None

    Example:
        To sell all our shares of stock 1 on day 8, with fees 20:
            >>> sell(8, 1, sim_data, 20, portfolio)
    '''
    # calculate  price of the stock today
    price = stock_prices[date][stock]
    if np.isnan(price):
        return
    # calculate the shares we would sell
    shares = portfolio[stock]
    portfolio[stock]=0
    # record the transaction
    log_transaction("sell", date, stock, shares, price, fees, ledger_file)


def create_portfolio(available_amounts, stock_prices, fees):
    '''
    Create a portfolio by buying a given number of shares of each stock.
    
    Input:
        available_amounts (list): how much money we allocate to the initial
            purchase for each stock (this should cover fees)
        stock_prices (ndarray): the stock price data
        fees (float): transaction fees (fixed amount per transaction)
    
    Output:
        portfolio (list): our initial portfolio

    Example:
        Spend 1000 for each stock (including 40 fees for each purchase):
        >>> N = sim_data.shape[1]
        >>> portfolio = create_portfolio([1000] * N, sim_data, 40)
    '''
    portfolio=[0 for i in range(len(available_amounts))]
    stock_nb=0
    for amount in available_amounts:
        buy(0, stock_nb, amount, stock_prices, fees, portfolio, "ledger.txt")
        stock_nb += 1
    return portfolio



if __name__=='__main__':
    from trading.data import get_data
    read=get_data("read")
    generate=get_data("generate")
    stock_data=read[1:,]
    initial_prices=stock_data[0]
    closet=[100, 120, 400, 250,300]
    stock_index=[]
    for price in closet:
        stock_nb=np.abs(initial_prices-price)
        stock_index.append(np.argmin(stock_nb))
    sim_data=stock_data[:,stock_index]
    N=sim_data.shape[1]
    portfolio= create_portfolio([5000]*N,sim_data,20)








