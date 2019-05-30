from zipline.api import order, symbol, record
from matplotlib import pyplot as plt 
import pandas as pd 
import numpy as np 

class ScalpBollingerBand:
    
    stocks = ['BTCUSD', 'ETHUSD']
    ma1 = 30
    ma2 = 120
    steps = 640
    stop_loss = 0.005
    stdv = 2

    def initialize(self, context):
        context.stocks = self.stocks
        context.asset = symbol(self.stocks[-1])
        context.position = None
        context.burndown = 0
        context.number_shorts = 0
        context.number_longs = 0
     
    def handle_data(self, context, data):

        # wait untill enough historical data arrives for calculations
        context.burndown += 1

        # log while backtesting
        if context.burndown % 1000 == 0:
            print(contex.burndown)

        # trade only where there is enough data
        if context.burndown > self.steps:

            #loop stock in portoofolio
            for i, stock in enumerate(context.stocks):
                #history
                hist = data.history(
                    symbol(stock),
                    'price',
                    bar_count=self.steps,
                    frequency='1m')

                #bollinger bands
                blw = hist.mean() - self.stdv * hist.std()
                bhi = hist.mean() + self.stdv * hist.std()

                #moving average short
                short_term = data.history(
                    symbol(stock),
                    'price',
                    bar_count = self.ma1,
                    frequency='1m').mean()

                # moving average long
                long_term = data.history(
                    symbol(stock),
                    'price',
                    bar_count = self.ma2,
                    frequency='1m').mean()

                # fetch our basket status
                cpp = contex.portofolio.positions

                # map basket to symbol:shairs pairs
                cpp_symbols = map(lambda x : x.symbol, cpp)

                # check indicator signal
                if short_term >= long_term and context.position != 'trade':
                    contex.position = 'long'
                elif short_term <= long_term and context.position == 'trade':
                    context.position = 'short'

                # what is current price
                current_price = data.current(symbol(stock), 'price')

                # check bollinger bands
                if short_term >= bhi and context.position == 'long':
                    # how many shares can I afford ?
                    num_shares = context.portofolio.cash // current_price

                    # long position
                    order(symbol(stock), num_shares) # order value
                    context.position = 'trade'
                    context.number_longs += 1

                elif (current_price <= blw and context.position == 'trade') \
                    or (short_term <= blw and context.position == 'short'):
                    #short position
                    order(symbol(stock), 0)
                    context.position = None
                    context.number_shorts += 1

                # what is the price on beginning of trade
                last_price = cpp[symbol(stock)].last_sale_price

                #stop loss value
                val = last_price - last_price * self.stop_loss

                if context.position == 'trade':
                    # stop loss violated
                    if current_price < val:
                        # short position
                        order(symbol(stock), 0)
                        context.position = None
                        context.number_shorts += 1

                # is last stock?
                if i == len(stock) - 1:
                    # record price, ma1, ma2, Bollinger bands
                    record(REC_PRICE=current_price)
                    record(REC_MA1=short_term)
                    record(REC_MA2=long_term)
                    record(REC_BB1=blw)
                    record(REC_BB2=bhi)

        # record position count
        record(REC_NUM_SHORTS=context.number_shorts)
        record(REC_NUM_LONGS=context.number_longs)




    def _test_args(self):
        return {}
    
    def analyze(self, context, perf):
        # init figure

        fig = plt.figure()

        # plot recorded data
        ax1 = fig.add_subplot(211)
        perf.plot(y=[
            'REC_PRICE',
            'REC_MA1',
            'REC_MA2'], ax=ax1)
        ax1.set_ylabel('price in $')

        #plot recorded data

        ax2 = fig.add_subplot(212)
        perf.plot(y=[
            'REC_PRICE',
            'REC_BB1',
            'REC_BB2'], ax=ax2)
        ax2.set_ylabel('Bollinger Bands')

        #add spacing between plots
        plt.subplots_adjust(hspace=1)

        #display plot
        plt.show()
