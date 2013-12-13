#!/usr/bin/env python
import numpy as np
import datetime
import strategy


#FILE = "test_mtgoxUSD_Oct_Dec.csv";
#FILE = "mtgoxUSD.csv.1";
FILE = "mtgoxUSD.csv.2";

def pretty_print_candle (candle):
	print ("%d %5.8f %5.8f %5.8f %5.8f" % (candle[0], candle[1],
									   candle[2], candle[3], candle[4]))

def get_candles_from_history (time_frame):
	"""
	Gets candles and returns a list of all candles in the specified timeframe.
	candles are in the format [start_timestamp, open, high, low, close]
	"""
	All_candles = []
	current_candle_start = 0
	current_time   = 0
	with open(FILE) as trade_data:
		for trade in trade_data:
			candle_close = 0
			# Initial trade
			[s_timestamp, s_price, volume] = trade.split(',')
			price     = float(s_price)
			timestamp = int(s_timestamp)
			if ( current_candle_start == 0 ) :
				# This is the first candle
				current_candle_start = timestamp - timestamp%time_frame
				current_candle_close = current_candle_start + time_frame
				current_candle = [ current_candle_start, price, price, price, price ]
				#print "New candle : ", current_candle

			elif ( int(timestamp) >= current_candle_close ) :
				# Logging old candle, making a new one.
				#print "Closing candle : ", current_candle
				All_candles.append(current_candle)
				#pretty_print_candle(current_candle)
				current_candle_start = timestamp - timestamp%time_frame
				current_candle_close = current_candle_start + time_frame
				current_candle = [ current_candle_start, price, price, price, price ]

			else:
				if   ( price > current_candle[2] ):
					current_candle[2] = price
				elif ( price < current_candle[3] ):
					current_candle[3] = price
				current_candle[4] = price

		#print current_candle
		All_candles.append ( current_candle )
		return All_candles

def moving_average(x, n, type='simple'):
    """
    compute an n period moving average.
    type is 'simple' | 'exponential'
    """
    x = np.asarray(x)
    if type=='simple':
        weights = np.ones(n)
    else:
        weights = np.exp(np.linspace(-1., 0., n))
    weights /= weights.sum()

    a =  np.convolve(x, weights, mode='full')[:len(x)]
    a[:n] = a[n]
    return a

def Sim_Buy ( Total, Price ):
	MtGox_Fee = Total * (.55)
	Cost = Total - MtGox_Fee
	return (Cost / Price)

def Sim_Sell ( Total, Price ):
	MtGox_Fee = Total * (.55)
	Coins = Total - MtGox_Fee
	return (Coins * Price)

def BuyAndHold(candles, initial_USD):
	First_candle = candles[0];
	Last_candle  = candles[-1]
	#Coins        = Sim_Buy( initial_USD, First_candle[4])
	Coins        = initial_USD*(1-0.0055)/First_candle[4]
	print '[Buy N Hold] price:{0:.5f}   BTC:{1:.5f}   USD:{2:.5f}  <{3}> '.format(First_candle[4], Coins, 0.0, 
																				  datetime.datetime.fromtimestamp(int(First_candle[0])).strftime('%Y-%m-%d %H:%M:%S'))
	final_USD = Coins*(1-0.0055) * Last_candle[4]
	print '[Selling ] price:{0:.5f}   BTC:{1:.5f}   USD:{2:.5f}  <{3}> '.format(Last_candle[4], Coins, 0.0,
																				datetime.datetime.fromtimestamp(int(Last_candle[0])).strftime('%Y-%m-%d %H:%M:%S'))
	print "Buy and Hold "
	print "Inital = ", initial_USD
	print "Final  = ", final_USD

def Ruby (candles, initial_USD):
	# in percent
	buy_threshold = 0.01   # .3%
	sell_threshold = 0.03  # .5%

	Current_USD = initial_USD
	Current_BTC = 0
	Status = "init"

	for candle in candles:
		ema8  = candle[5]
		ema32 = candle[7]
		ema41 = candle[8]
#		if   ( ema8-ema41 > candle[4]*buy_threshold ) and Status != "long" :
		if  ema8 > ema41 and ema41 > ema32 and ema8-ema41 > candle[4]*buy_threshold and Status != "long" :
			#Current_BTC = Sim_Buy ( Current_USD, candle[4] )
			Current_BTC = Current_USD*(1-0.0055)/candle[4]
			Current_USD = 0.0
			print '[BUY BTC ] price:{0:.5f}   BTC:{1:.5f}   USD:{2:.5f}  <{3}> '.format(
				candle[4], Current_BTC, Current_USD, datetime.datetime.fromtimestamp(int(candle[0])).strftime('%Y-%m-%d %H:%M:%S'))
			Status = "long"
		elif ema32 > ema41 and ema41 > ema8 and ema32-ema8 > candle[4]*sell_threshold and Status == "long":
			#Current_USD = Sim_Sell ( Current_BTC, candle[4] )
			Current_USD = Current_BTC*(1-0.0055)*candle[4]
			Current_BTC = 0.0
			print '[SELL BTC] price:{0:.5f}   BTC:{1:.5f}   USD:{2:.5f}  <{3}> '.format(
				candle[4], Current_BTC, Current_USD, datetime.datetime.fromtimestamp(int(candle[0])).strftime('%Y-%m-%d %H:%M:%S'))
			Status = "short"
		elif ema8-ema41 > candle[4]*buy_threshold and Status == "init" :
			Current_BTC = Current_USD*(1-0.0055)/candle[4]
			Current_USD = 0.0
			print '[BUY BTC ] price:{0:.5f}   BTC:{1:.5f}   USD:{2:.5f}  <{3}> '.format(
				candle[4], Current_BTC, Current_USD, datetime.datetime.fromtimestamp(int(candle[0])).strftime('%Y-%m-%d %H:%M:%S'))
			Status = "long"

	if ( Status == "long" ) :
		Current_USD = Current_BTC*(1-0.0055)*candles[-1][4]
	print "Final RUBY usd  : ${0:.5f}  [BTC Price : ${1:.5f}".format(Current_USD, candles[-1][4])
	return Current_USD

def ichimoku ():
	print "ichi"


def ApplyStrategy( candles, initial_USD, strategy ):
	if (strategy == "Ruby"):
		result =  Ruby(candles, initial_USD)
	elif (strategy == "BuyAndHold"):
		result =  BuyAndHold(candles, inital_USD)
	return result

if __name__ == "__main__":

	All_candles = get_candles_from_history (60*60)

#	rsi = strategy.RSI(14)
#	for candle in All_candles:
#		print candle, " RSI : ", rsi.put(candle)

#	exit (0)
	print "Starting date : ", (datetime.datetime.fromtimestamp(int(All_candles[0][0])).strftime('%Y-%m-%d %H:%M:%S'))
	print "Ending date   : ", (datetime.datetime.fromtimestamp(int(All_candles[-1][0])).strftime('%Y-%m-%d %H:%M:%S'))

	np_history = np.array(All_candles)
	BuyAndHold(All_candles, 5000)


	print "Ruby Strategy at 60min candles"
	print "Buy threshold  : 1%"
	print "Sell threshold : 3%"
	print "Simulation start :"
#	exit (0)
#	np_history = np.array(All_candles, dtype=['f8','f8','f8','f8','f8' ])
#	print np_history.shape

	EMA8  = moving_average( np_history[:,4].astype(float),   8, type='exponential' )
#	print "EMA8.shape :  ", EMA8.shape
	EMA13 = moving_average( np_history[:,4].astype(float),  13, type='exponential' )
	EMA32 = moving_average( np_history[:,4].astype(float),  32, type='exponential' )
	EMA41 = moving_average( np_history[:,4].astype(float),  41, type='exponential' )
	candles_with_EMAs = np.column_stack ((np_history, EMA8, EMA13, EMA32, EMA41))

	Ruby ( candles_with_EMAs , 5000.0 )
	print "Simulation end"
	exit (0)
	Ruby_result = ApplyStrategy(candles_with_EMAs, 5000, strategy="Ruby" )
	BAH_result  = ApplyStrategy(np_history, 5000, strategy="BuyAndHold")
#
#	print EMA8
