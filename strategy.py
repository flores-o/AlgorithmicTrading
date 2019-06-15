class strategy():
    def __init__(self):
        self.stocks = 0
    
    def take_action(self, today_real_price, tomorrow_forcasted_price):
        """
         At day t, an investor buys one share of INTC stock if the predicted price 
         is higher than the current actual adjusted closing price.
         Otherwise, he or she sells one share of INTC stock"""
        if tomorrow_forcasted_price > today_real_price:
            self.stocks += 1
        else:
            self.stocks -= 1
    
    def compute_daily_return(self, today_real_price, tomorrow_real_price):
        """
         Using the
        indicator variable st
        , we can calculate a daily return of
        the strategy at day t + 1:
        rt+1 = st × log 
        yt+1
        yt
        
        −
        """
        import math
        daily_return = self.stocks * math.log(tomorrow_real_price, today_real_price)
        return daily_return


    def execute_strategy(strategy, predicted_data, real_data, verbose=True):
        """
        args: strategy to execute
        """
        cumulative_return = 0
        for day, today_real_price in enumerate(real_data[:-1]):
            # day by day and execute my strategy
            today_predicted_price = predicted_data[day]
            if verbose: print(day, today_real_price, today_predicted_price)
            
            strategy.take_action(today_real_price, predicted_data[day + 1])
            today_return = strategy.compute_daily_return(today_real_price, real_data[day + 1])
            # metric: cumulative return
            # sum of all the returns
            cumulative_return += today_return
        return cumulative_return