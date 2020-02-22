'''
1. Calculate stocks expected price
    Get expected gain as percent

2. Calculate stocks STD (assume normal distribution)
    Get risk (high variance == high risk) -- relative variance (variance / price)

3. Maximize (expected gain / (risk * risk coefficient))


4. Minimize loss


'''

import pandas as pd
import numpy as np
import datetime


def percent_gain(buy_price, current_price):
    return (current_price / buy_price) - 1


class Holding:
    def __init__(
            self,
            ticker,
            buy_price,
            buy_datetime,
            sell_price,
            sell_datetime,
            gain_cash
    ):
        self.ticker = ticker
        self.buy_price = buy_price
        self.buy_datetime = buy_datetime
        self.sell_price = sell_price
        self.sell_datetime = sell_datetime
        self.gain_cash = gain_cash


class Trader:
    def __init__(
            self,
            cash,
            simulate=True
    ):
        self.cash = cash
        self.simulate = simulate
        self.holdings = []

        pass

    def evaluate(self):
        '''

        :return:
        '''
        pass

    def buy(self):
        '''Buy a quantity of a stock

        :return:
        '''
        pass

    def sell(self):
        '''Sell a quantity of a holding

        :return:
        '''
        pass

    def hold(self):
        '''Place no action

        :return:
        '''
        pass

    def statement(self):
        '''Save the current holdings into a JSON

        :return:
        '''
        pass

    def start(self):
        pass

    def stop(self):
        pass


def main():
    trader = Trader(cash=1000)

    while trader.cash > 0:

        trader.evaluate()


if __name__ == "__main__":
    pass
