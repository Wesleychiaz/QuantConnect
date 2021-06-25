#Questions: Caclulate BASS - Beta, Alpha, Sharpe Ratio, Standard Dev
#1. Calculate daily returns of TSLA and S&P500
#2. Abs returns of TSLA and S&P500
#3. Calculate Mean, Correlation, Variance, Std Dev
#4. Calulate BASS


# Load Libraries
import numpy as np
import pandas as pd
class SingleVariableBASSCalulations(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2021, 1, 1) # Set Start Date
        
        self.market = "SPY"
        self.stock = "ETH"
        
        self.AddEquity(self.stock, Resolution.Daily) # Initialize Tesla
        self.AddEquity(self.market, Resolution.Daily) # Initialize SPY as a reference for S&P
        
    def OnEndOfAlgorithm(self): #Today
    
        # call historical data from QC database
        # History parameters (Symbol, days, Resolution), E.g (TSLA, 30, Daily)
        history_market = self.History(self.Symbol(self.market), 30, Resolution.Daily)
        # take out the close price and convert it to a list for later using in datframe
        history_market = history_market["close"].tolist()
        # calculate absolute return
        market_abs_return = (history_market[-1]-history_market[0]) / history_market[0]
        
        #same for TSLA
        history_stock = self.History(self.Symbol(self.stock), 30, Resolution.Daily)
        history_stock = history_stock["close"].tolist()
        stock_abs_return = (history_stock[-1]-history_stock[0]) / history_stock[0]
    
        #self.Debug("{} abs return is {}".format(self.market,market_abs_return))
        #self.Debug("{} abs return is {}".format(self.stock,stock_abs_return))
        
        
        # make dataframe for easier visual and calculation
        df = pd.DataFrame()
        #store previously obtained spy and tsla prices in dataframe
        df["market_price"] = history_market
        df["stock_price"] = history_stock
        
        # calculate percentage change ad store in the same database
        df["market_returns"] = df['market_price'].pct_change()
        df["stock_returns"] = df['stock_price'].pct_change()
        
        self.Debug(df)
        
        
        ################## Value for BAS Calculations ################
        
        # mean of daily returns (Not to be confused by abs returns)
        market_daily_ret = df["market_returns"].mean()
        stock_daily_ret = df["stock_returns"].mean()
        self.Debug('{} mean return is: {}'.format(self.market,market_daily_ret))
        self.Debug('{} mean return is: {}'.format(self.stock,stock_daily_ret))
        
        # variance
        market_var = df["market_returns"].var()
        stock_var = df["stock_returns"].var()
        self.Debug('{} variance: {}'.format(self.market,market_var))
        self.Debug('{} variance: {}'.format(self.stock,stock_var))
        
        # covariance
        covariance = df["market_returns"].cov(df["stock_returns"])
        self.Debug('covariance: {}'.format(covariance))
        
        # correlation
        correlation = df["market_returns"].corr(df["stock_returns"])
        self.Debug('correlation: {}'.format(correlation))
        
        ################### BASS CALCULATION ##########################
        
        
        # Standard Deviation
        market_std = df["market_returns"].std()
        stock_std = df["stock_returns"].std()
        self.Debug('Std deviation of {}: {}'.format(self.market,market_std))
        self.Debug('Std deviation of {}: {}'.format(self.stock,stock_std))
        
        # TSLA Beta
        stock_beta = covariance / market_var
        self.Debug('{} beta: {}'.format(self.stock,stock_beta))
        
        stock_alpha = stock_abs_return - stock_beta * market_abs_return # making use of annualised mean returns
        self.Debug('{} alpha: {}'.format(self.stock,stock_alpha))
        
        #tsla_monthly_std = tsla_std * (20**0.5)
        #TSLA_SR = tsla_abs_return/ tsla_monthly_std
        stock_sr = stock_daily_ret/ stock_std * (252**0.5)  # Square root, making use of mean returns
        self.Debug('{} Sharpe Ratio: {}'.format(self.stock,stock_sr))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
