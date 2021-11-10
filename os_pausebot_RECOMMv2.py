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
SYMBOLS = ['BTCUSDT', 'ETHUSDT']

MY_FIRST_INTERVAL = Interval.INTERVAL_1_MINUTE
MY_SECOND_INTERVAL = Interval.INTERVAL_5_MINUTES
MY_THIRD_INTERVAL = Interval.INTERVAL_15_MINUTES


TIME_TO_WAIT = 1 # Minutes to wait between analysis
FULL_LOG = True # List anylysis result to console

SIGNAL_NAME = 'os_pausebot_RECOMMv2'
SIGNAL_FILE = 'signals/pausebot.pause'


def analyze():
    taMax = 0
    taMaxCoin = 'none'
    signal_coins = {}
    first_analysis = {}
    second_analysis = {}
    third_analysis = {}
    first_handler = {}
    second_handler = {}
    third_handler = {}

    paused = 0
    retPaused = False

    for symbol in SYMBOLS:
        first_handler[symbol] = TA_Handler(
            symbol=symbol,
            exchange=MY_EXCHANGE,
            screener=MY_SCREENER,
            interval=MY_FIRST_INTERVAL,
            timeout= 10
        )
        second_handler[symbol] = TA_Handler(
            symbol=symbol,
            exchange=MY_EXCHANGE,
            screener=MY_SCREENER,
            interval=MY_SECOND_INTERVAL,
            timeout= 10
        )
        third_handler[symbol] = TA_Handler(
            symbol=symbol,
            exchange=MY_EXCHANGE,
            screener=MY_SCREENER,
            interval=MY_THIRD_INTERVAL,
            timeout= 10
        )

    for symbol in SYMBOLS:
       
        try:
            first_analysis = first_handler[symbol].get_analysis()
            second_analysis = second_handler[symbol].get_analysis()
            third_analysis = third_handler[symbol].get_analysis()

        except Exception as e:
            print(f'{SIGNAL_NAME}')
            print("Exception:")
            print(e)
            print (f'Coin: {symbol}')
            print (f'First handler: {first_handler[symbol]}')
            print (f'Second handler: {second_handler[symbol]}')
            print (f'Second handler: {third_handler[symbol]}')
            continue
               
        first_recommendation = first_analysis.summary['RECOMMENDATION']
        second_recommendation = second_analysis.summary['RECOMMENDATION']
        third_recommendation = third_analysis.summary['RECOMMENDATION']
        
        #if FULL_LOG:
            #print(f'|{SIGNAL_NAME}| <{symbol}> |First: {first_recommendation}| |Second: {second_recommendation}| Third: {third_recommendation}| Four: {four_recommendation}| Five: {five_recommendation}| Six: {six_recommendation}|')
            #print(f'|{SIGNAL_NAME}| <{symbol}> |First: {first_recommendation}| |Second: {second_recommendation}| Third: {third_recommendation}|')    
        if  (first_recommendation == "SELL" or first_recommendation == "STRONG_SELL") and \
            (second_recommendation == "SELL" or second_recommendation == "STRONG_SELL"): #and \
            #(third_recommendation == "SELL" or third_recommendation == "STRONG_SELL"): #and \
            #(four_recommendation == "BUY" or four_recommendation == "STRONG_BUY") and \
            #(five_recommendation == "BUY" or five_recommendation == "STRON_BUY"): #and \
            #(six_recommendation == "BUY" or five_recommendation == "STRONG_BUY"):
            paused = paused + 1
        if FULL_LOG:
            #print(f'|{SIGNAL_NAME}| <{symbol}> |First: {first_recommendation}| |Second: {second_recommendation}| Third: {third_recommendation}| Four: {four_recommendation}| Five: {five_recommendation}| Six: {six_recommendation}|')
            print(f'|{SIGNAL_NAME}| <{symbol}> |First: {first_recommendation}| |Second: {second_recommendation}|')

            #print(f'{txcolors.YELLOW}|{SIGNAL_NAME}|: Buy Signal Detected On <{symbol}>{txcolors.DEFAULT}')
    
    if paused > 0:
        print(f'|{SIGNAL_NAME}| Market Alert: <PAUSED BUYING> [{TIME_TO_WAIT}] Minutes For Next Checkup')
        retPaused = True
    else:
        print(f'|{SIGNAL_NAME}| Market OK: <WORKING> [{TIME_TO_WAIT}] Minutes For Next Checkup')
        retPaused = False

    return retPaused

def do_work():
    while True:
        try:
            if not threading.main_thread().is_alive(): exit()
            paused = analyze()
            if paused:
                with open(SIGNAL_FILE,'a') as f:
                    f.write('yes')
            else:
                if os.path.isfile(SIGNAL_FILE):
                    os.remove(SIGNAL_FILE)

            time.sleep((TIME_TO_WAIT*60))
        #except Exception as e:
        #    print(f'{SIGNAL_NAME}: Exception do_work() 1: {e}')
        #    continue
        except KeyboardInterrupt as ki:
            continue