# Based off Firewatch custsignalmod.py

from tradingview_ta import TA_Handler, Interval, Exchange
# use for environment variables
import os
# use if needed to pass args to external modules
import sys
# used for directory handling
import glob

import threading
import time

# my helper utils
from helpers.os_utils import(rchop)
from vyacheslav_signalbuy_VolScan import txcolors

MY_EXCHANGE = 'BINANCE'
MY_SCREENER = 'CRYPTO'
MY_FIRST_INTERVAL = Interval.INTERVAL_1_MINUTE
MY_SECOND_INTERVAL = Interval.INTERVAL_5_MINUTES
MY_THIRD_INTERVAL = Interval.INTERVAL_15_MINUTES
MY_FOUR_INTERVAL = Interval.INTERVAL_1_HOUR
MY_FIVE_INTERVAL = Interval.INTERVAL_4_HOURS
MY_SIX_INTERVAL = Interval.INTERVAL_1_DAY

PAIR_WITH = 'USDT'

TIME_TO_WAIT =  # Minutes to wait between analysis
FULL_LOG = False # List anylysis result to console

SIGNAL_NAME = 'os_signalbuy_RECOMM'
SIGNAL_FILE = 'signals/' + SIGNAL_NAME + '.buy'

TICKERS = 'tickers_top72.txt'
TICKERS_OVERRIDE = 'tickers_signalbuy.txt'

if os.path.exists(TICKERS_OVERRIDE):
    TICKERS = TICKERS_OVERRIDE


TRADINGVIEW_EX_FILE = 'tradingview_ta_unknown'

def analyze(pairs):
    taMax = 0
    taMaxCoin = 'none'
    signal_coins = {}
    first_analysis = {}
    second_analysis = {}
    third_analysis = {}
    four_analysis = {}
    five_analysis = {}
    six_analysis = {}
    first_handler = {}
    second_handler = {}
    third_handler = {}
    four_handler = {}
    five_handler = {}
    six_handler = {}
    
    if os.path.exists(SIGNAL_FILE):
        os.remove(SIGNAL_FILE)

    if os.path.exists(TRADINGVIEW_EX_FILE):
        os.remove(TRADINGVIEW_EX_FILE)

    for pair in pairs:
        first_handler[pair] = TA_Handler(
            symbol=pair,
            exchange=MY_EXCHANGE,
            screener=MY_SCREENER,
            interval=MY_FIRST_INTERVAL,
            timeout= 10
        )
        second_handler[pair] = TA_Handler(
            symbol=pair,
            exchange=MY_EXCHANGE,
            screener=MY_SCREENER,
            interval=MY_SECOND_INTERVAL,
            timeout= 10
        )
        third_handler[pair] = TA_Handler(
            symbol=pair,
            exchange=MY_EXCHANGE,
            screener=MY_SCREENER,
            interval=MY_THIRD_INTERVAL,
            timeout= 10
        )
        four_handler[pair] = TA_Handler(
            symbol=pair,
            exchange=MY_EXCHANGE,
            screener=MY_SCREENER,
            interval=MY_FOUR_INTERVAL,
            timeout= 10
        )
        five_handler[pair] = TA_Handler(
            symbol=pair,
            exchange=MY_EXCHANGE,
            screener=MY_SCREENER,
            interval=MY_FIVE_INTERVAL,
            timeout= 10
        )
        six_handler[pair] = TA_Handler(
            symbol=pair,
            exchange=MY_EXCHANGE,
            screener=MY_SCREENER,
            interval=MY_SIX_INTERVAL,
            timeout= 10
        )

    for pair in pairs:
       
        try:
            first_analysis = first_handler[pair].get_analysis()
            second_analysis = second_handler[pair].get_analysis()
            third_analysis = third_handler[pair].get_analysis()
            four_analysis = four_handler[pair].get_analysis()
            five_analysis = five_handler[pair].get_analysis()
            six_analysis = six_handler[pair].get_analysis()
        except Exception as e:
            print(f'{SIGNAL_NAME}')
            print("Exception:")
            print(e)
            print (f'Coin: {pair}')
            print (f'First handler: {first_handler[pair]}')
            print (f'Second handler: {second_handler[pair]}')
            print (f'Second handler: {third_handler[pair]}')
            print(f'Four handler: {four_handler[pair]}')
            print(f'Five handler: {five_handler[pair]}')
            print(f'Six handler: {six_handler[pair]}')
            with open(TRADINGVIEW_EX_FILE,'a+') as f:
                    #f.write(pair.removesuffix(PAIR_WITH) + '\n')
                    f.write(rchop(pair, PAIR_WITH) + '\n')
            continue
               
        first_recommendation = first_analysis.summary['RECOMMENDATION']
        second_recommendation = second_analysis.summary['RECOMMENDATION']
        third_recommendation = third_analysis.summary['RECOMMENDATION']
        four_recommendation = four_analysis.summary['RECOMMENDATION']
        five_recommendation = five_analysis.summary['RECOMMENDATION']
        six_recommendation = six_analysis.summary['RECOMMENDATION']
        
        if FULL_LOG:
            print(f'|{SIGNAL_NAME}| <{pair}> |First: {first_recommendation}| |Second: {second_recommendation}| Third: {third_recommendation}| Four: {four_recommendation}| Five: {five_recommendation}| Six: {six_recommendation}|')
                
        if  (first_recommendation == "BUY" or first_recommendation == "STRONG_BUY") and \
            (second_recommendation == "BUY" or second_recommendation == "STRONG_BUY") and \
            (third_recommendation == "BUY" or third_recommendation == "STRONG_BUY") and \
            (four_recommendation == "BUY" or four_recommendation == "STRONG_BUY") and \
            (five_recommendation == "BUY" or five_recommendation == "STRON_BUY") and \
            (six_recommendation == "BUY" or five_recommendation == "STRONG_BUY"):
            print(f'{txcolors.YELLOW}|{SIGNAL_NAME}|: Buy Signal Detected On <{pair}>{txcolors.DEFAULT}')

            signal_coins[pair] = pair
            
            with open(SIGNAL_FILE,'a+') as f:
                f.write(pair + '\n')

    return signal_coins

def do_work():
    while True:
        try:
            if not os.path.exists(TICKERS):
                time.sleep((TIME_TO_WAIT*60))
                continue

            signal_coins = {}
            pairs = {}

            pairs=[line.strip() for line in open(TICKERS)]
            for line in open(TICKERS):
                pairs=[line.strip() + PAIR_WITH for line in open(TICKERS)] 
            
            if not threading.main_thread().is_alive(): exit()
            print(f'|{SIGNAL_NAME}|: Analyzing <{len(pairs)}> Coins')
            signal_coins = analyze(pairs)
            print(f'|{SIGNAL_NAME}|: <{len(signal_coins)}> Coins With Buy Signals. Waiting [{TIME_TO_WAIT}] Minutes For Next Analysis')

            time.sleep((TIME_TO_WAIT*60))
        #except Exception as e:
        #    print(f'{SIGNAL_NAME}: Exception do_work() 1: {e}')
        #    continue
        except KeyboardInterrupt as ki:
            continue