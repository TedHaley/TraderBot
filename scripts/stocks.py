import requests
import pandas as pd
import datetime
import logging
from pprint import pprint
import plotly.graph_objects as go
from datetime import datetime
import os
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

logger = logging.getLogger(__name__)

os.environ["STOCK_TOKEN"] = "pk_165010d1ca4443b2b7bdd81f4d610844"
token = os.environ["STOCK_TOKEN"]


class _IEXBase(object):
    _OLD_URL = 'https://api.iextrading.com/1.0/'
    _NEW_URL = 'https://cloud.iexapis.com/stable/'
    _OLD_STOCK_URL = f'{_OLD_URL}stock/'
    _OLD_SYMBOLS_URL = f'{_OLD_URL}ref-data/symbols/'
    _NEW_STOCK_URL = f'{_NEW_URL}stock/'
    _TOKEN_URL = f'?token={token}'

    def _validate_response(self, response):
        if response.text == "Unknown symbol":
            raise ValueError(response.text)

        if response.status_code != 200:
            self._handle_error(response)

        return response.json()

    @staticmethod
    def _handle_error(response):

        auth_msg = "The query could not be completed. Invalid auth token."

        status_code = response.status_code
        if 400 <= status_code < 500:
            if status_code == 400:
                logger.warning(auth_msg)
            else:
                logger.warning("The query could not be completed. "
                               "There was a client-side error with your "
                               "request.")
        elif 500 <= status_code < 600:
            logger.warning("The query could not be completed. "
                           "There was a server-side error with "
                           "your request.")
        else:
            logger.warning("The query could not be completed.")

    def _get_symbols(self):
        symbols_request = requests.get(self._OLD_SYMBOLS_URL)
        symbols_json = symbols_request.json()

        symbol_list = []

        for symbol_metadata in symbols_json:
            symbol = symbol_metadata['symbol']
            symbol_list.append(symbol)

        return symbol_list

    def _get_metadata(self):
        symbols_request = requests.get(self._OLD_SYMBOLS_URL)
        symbols_json = symbols_request.json()

        symbol_dict = {}

        for symbol_metadata in symbols_json:
            symbol = symbol_metadata['symbol']
            symbol_dict[symbol] = symbol_metadata

        return symbol_dict


class Stock(_IEXBase):

    def __init__(self, ticker=''):

        self.quote = None
        self.historical = {}

        # Checks to see if the ticker input is string
        if isinstance(ticker, str):
            symbols = self._get_symbols()

            # Checks to see if the ticker is in the list of valid symbols
            if ticker in symbols:
                self.ticker = ticker

            elif ticker == '':
                self.symbols = symbols

            else:
                print('Invalid Ticker Symbol')

    def get_quote(self):
        response = requests.get(f'{self._NEW_STOCK_URL}{self.ticker}/quote/{self._TOKEN_URL}')
        validated_response = _IEXBase._validate_response(self=self, response=response)
        self.quote = validated_response
        return self

    def get_historical(self, range):
        response = requests.get(f'{self._NEW_STOCK_URL}{self.ticker}/chart/{range}/{self._TOKEN_URL}')
        validated_response = _IEXBase._validate_response(self=self, response=response)
        self.historical[range] = validated_response
        return self

    def get_stock_names(self):
        return self._get_metadata()


def stock_symbols():
    stock_instance = Stock()
    symbols = stock_instance.get_stock_names()
    return symbols


if __name__ == '__main__':

    symbol_list = Stock().symbols
    # print(symbol_list)

    lm_coeff_dict = {}

    symbol = symbol_list[50]
    # print(symbol)

    try:
        stock = Stock(ticker=symbol)
        # print(stock.__dict__)
        #
        # quote = stock.get_quote()
        # print(quote.__dict__)

        quote = stock.get_historical(range='6m')
        # pprint(quote.__dict__)
        # print(len(quote.__dict__['historical']['1d']))

        subset = quote.__dict__['historical']['6m']
        df = pd.DataFrame(subset)

        print(df)

        # plt.plot(df['date'], df['changePercent'])
        # plt.show()
        #
        # plt.plot(df['date'], df['uVolume'])
        # plt.show()



    except Exception as e:
        print(e)
