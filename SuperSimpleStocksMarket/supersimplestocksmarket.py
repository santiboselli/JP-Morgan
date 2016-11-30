# Santiago Boselli
# Super Simple Stock Market
# JP Morgan & Chase Example Assignment
# https://github.com/santiboselli/JP-Morgan/SuperSimpleStocksMarket

# ------------------------------------ *** IMPORTS *** ------------------------------------

import sys
import os
import csv
import datetime
import random
import uuid


# ------------------------------------ *** USER DEFINED FUNCTIONS *** ------------------------------------

def load_csv():
    # Path to the CSV File
    csv_path = os.path.abspath(__file__)
    csv_path = os.path.dirname(csv_path)
    csv_path = os.path.join(csv_path, 'test_data/data.csv')
    csv_path = os.path.abspath(csv_path)

    return csv_path


def load_dividend_data(csv_path):
    with open(os.path.abspath(csv_path), 'r') as csvfile:
        for index, stock in enumerate(csv.reader(csvfile, delimiter=';')):
            if index > 0:
                record_dividend_data(*stock[:5])
    print(dividends)


def record_dividend_data(symbol, type, last, fixed, value):
    # If it's like 2% or 0.02
    if fixed is not None and fixed.endswith('%'):
        fixed = float(fixed[:-1]) / 100.0
    elif fixed is not None and len(fixed) > 0:
        fixed = float(fixed)
    else:
        fixed = None

    value = int(value)
    last = float(last)

    if value < 0:
        raise ValueError('Par value should be >= 0, not %d' % value)
    if last < 0:
        raise ValueError('Last dividend should be >= 0, not %f' % last)

    dividends.append({
        'Symbol': symbol,
        'Type': type,
        'Last Dividend': last,
        'Fixed Dividend': fixed,
        'Par Value': value
    })


def dividend_yield(symbol, price=None):
    if price is not None:
        s_price = price
    else:
        s_price = 0

    if symbol == "TEA":
        index = 0
    elif symbol == "POP":
        index = 1
    elif symbol == "ALE":
        index = 2
    elif symbol == "GIN":
        index = 3
    elif symbol == "JOE":
        index = 4
    else:
        return None

    if s_price is None or s_price == 0:
        return None
    elif dividends[index]['Type'] == 'Preferred':
        return float(dividends[index]['Fixed Dividend']) * float(dividends[index]['Par Value']) / s_price
    else:
        return float(dividends[index]['Last Dividend']) / s_price


def p_e_ratio(symbol, price):
    s_price = price
    d_yield = dividend_yield(symbol, price=s_price)
    if d_yield is None or d_yield == 0 or s_price is None:
        return None
    else:
        return s_price / d_yield


def record_trade(timestamp, symbol, type, quantity, price, mode):
    price = float(price)
    quantity = int(quantity)

    if price < 0.0:
        raise ValueError('Price should be >= 0, not %f' % price)
    if quantity < 0:
        raise ValueError('Quantity should be >= 0, not %d' % quantity)

    trade = {
        'ID': str(uuid.uuid4()),
        'Timestamp': timestamp,
        'Symbol': symbol,
        'Type': type,
        'Quantity': quantity,
        'Price': price,
        'Mode': mode
    }

    # Record the Trade
    trades.append(trade)


def volume_weighted_stock_price(symbol, timedelta):
    index = 0
    numerator = 0
    denominator = 0
    while index < len(trades):
        if trades[index]['Symbol'] == symbol:
            time_diff = now - (trades[index]['Timestamp'] + datetime.timedelta(minutes=timedelta))
            td = time_diff.total_seconds()

            if td <= 0:     # If the Time Difference is lower or equal to Timedelta
                numerator += trades[index]['Price'] * trades[index]['Quantity']
                denominator += trades[index]['Quantity']
        index += 1

    if denominator > 0:
        return float(numerator / denominator)
    else:
        return None


def gbce(total, n):
    return total**(1/float(n))


# ------------------------------------ *** TEST CASES *** ------------------------------------

def test_dividend_yield(test_price=None):
    for symbol in symbols:
        print('  Dividend yield for %s:' % symbol, dividend_yield(symbol, test_price))


def test_p_e_ratio(test_price=None):
    for symbol in symbols:
        print('  P/E Ratio for %s:' % symbol, p_e_ratio(symbol, test_price))


def test_record_trades():
    print("- Randomly Generated Trades")
    for i in range(20):     # Randomly Generated Trades = 20
        parameters = [
            random.choice(timestamps),
            random.choice(symbols),
            random.choice(types),
            random.choice(quantities),
            random.choice(prices),
            random.choice(modes)
        ]

        record_trade(*parameters)
        print('    TIMESTAMP:', parameters[0], '| SYMBOL:', parameters[1], '| TYPE:', parameters[2],
              '| QUANTITY:', parameters[3], '| PRICE:', parameters[4], '| MODE:', parameters[5])

    print("\n")
    print("- Stored Trades")
    print(trades)


def test_vw_stock_price(test_timedelta):
    print("  (Execution Datetime: %s)" % str(now))
    print("  (Randomly Generated Stocks: %d)" % len(trades))
    print("  (Time Delta: %d minutes)" % test_timedelta)

    for symbol in symbols:
        print("     Volume Weighted Stock Price for %s:" % symbol, volume_weighted_stock_price(symbol, test_timedelta))


def test_gbce(test_timedelta):
    n = 0
    vwsp = 1
    for symbol in symbols:
        if volume_weighted_stock_price(symbol, test_timedelta) is not None and volume_weighted_stock_price(symbol, test_timedelta) > 0:
            vwsp *= volume_weighted_stock_price(symbol, test_timedelta)
            n += 1

    print('     ~ GBCE:', gbce(vwsp, n))

# ------------------------------------ *** RUNTIME *** ------------------------------------

# Empty Lists
dividends = []
trades = []

# Random Timestamps for Trades
now = datetime.datetime.now()
timestamps = [now - datetime.timedelta(minutes=x) for x in range(0, 10)]

# Global Lists
symbols = ['TEA', 'POP', 'ALE', 'GIN', 'JOE']
types = ['Common', 'Preferred']
modes = ['SELL', 'BUY']
quantities = range(0, 100, 2)
prices = [1, 10, 100, 1000]

# EXECUTION
try:
    # LOAD CSV FILE
    print("LOAD DATA FROM CSV FILE")
    load_dividend_data(load_csv())

    # DIVIDEND YIELD CALCULATION
    print('\n')
    print("DIVIDEND YIELD CALCULATION")
    test_dividend_yield(10)  # Test Price for all Stocks = 10

    # P/E RATIO CALCULATION
    print('\n')
    print("P/E RATIO CALCULATION")
    test_p_e_ratio(10)  # Test Price for all Stocks = 10

    # RECORD TRADES
    print('\n')
    print("TRADE RECORDS")
    test_record_trades()

    # VOLUME WEIGHTED STOCK PRICE
    print('\n')
    print("COMPUTE VOLUME WEIGHTED STOCK PRICE")
    test_vw_stock_price(5)  # Test Time Delta = 5

    # GBCE ALL SHARE INDEX
    print('\n')
    print("COMPUTE GBCE ALL SHARE INDEX")
    test_gbce(5)  # Test Time Delta = 5

except StopIteration:
    sys.exit()
