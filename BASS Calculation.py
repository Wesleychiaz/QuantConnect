#Questions: Caclulate BASS - Beta, Alpha, Sharpe Ratio, Standard Dev
#1. Calculate daily returns of TSLA and S&P500
#2. Abs returns of TSLA and S&P500
#3. Calculate Mean, Correlation, Variance, Std Dev
#4. Calulate BASS


# Load Libraries
import numpy as np
import pandas as pd
class MultipleBASSCalulations(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2021, 1, 1) # Set Start Date
        self.stocks = ["SPY", "FB", "AMZN", "AAPL", "NFLX", "GOOGL"]
        self.market = "SPY"
        
        for stocks in self.stocks:
            self.AddEquity(stocks, Resolution.Daily)
        
            
    def OnEndOfAlgorithm(self): #Today
    
        # call historical data from QC database
        history_market = self.History(self.Symbol(self.market), 30, Resolution.Daily)
        history_market = history_market["close"].tolist()
        market_abs_return = (history_market[-1]-history_market[0]) / history_market[0]
    
        for item in self.stocks[1:]:
            
            # for item
            history = self.History(self.Symbol(item), 30, Resolution.Daily)
            history = history["close"].tolist()
            abs_return = (history[-1]-history[0]) / history [0]
            
            self.Debug("{} abs return is".format(self.market) + str(market_abs_return))
            self.Debug("{} abs return is:".format(item) + str(abs_return))
            
            
            # dataframe
            df = pd.DataFrame()
            df["price"] = history
            df["market_price"] = history_market
            
            # calculate percentage change and store in same database
            df["returns"] = df["price"].pct_change()
            df["market_returns"] = df["market_price"].pct_change()
            
            #self.Debug(df)
            
            ### Values for BAS Calculations ###
            
            # mean of daily returns
            daily_return = df["returns"].mean()
            market_daily_ret = df["market_returns"].mean()
            #self.Debug('{} mean of daily returns:'.format(self.market) + str(market_daily_ret))
            #self.Debug('{} mean of daily returns:'.format(item) + str(daily_return))
            
            
            # variance
            var = df["returns"].var()
            market_var = df["market_returns"].var()
            
            # covariance
            covariance = df["market_returns"].cov(df["returns"])
            #self.Debug("{} covariance against {}: ".format(item,self.market) + str(covariance))
            
            # correlation
            correlation = df["market_returns"].corr(df["returns"])
            #self.Debug("{} correlation against {}: ".format(item,self.market) + str(correlation))
            
            ### BASS Calculation ###
            
            # standard deviation
            market_std = df["market_returns"].std()
            std = df["returns"].std()
            self.Debug('Standard Deviation of {}: '.format(self.market) + str(market_std))
            self.Debug('Standard Deviation of {}: '.format(item) + str(std))
            
            # beta
            beta = covariance / market_var
            self.Debug('Beta of {}: '.format(item) + str(beta))
            
            #alpha
            alpha = abs_return - beta * market_abs_return
            self.Debug('Alpha of {}: '.format(item) + str(alpha))
            
            #Sharpe Ratio
            
            sr = daily_return/ std * (252**0.5)  # Square root, making use of mean returns
            self.Debug('Sharpe Ratio of {}: '.format(item) + str(sr))
            
            
