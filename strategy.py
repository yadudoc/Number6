#!/usr/bin/env python
import datetime
import numpy as np
import Wallet

class RSI:
	def __init__ (self, period ):
		self.period   = period
		self.candles  = []
		self.RSI      = -1

	def put (self, candle):
		""" Candle is of format [unixtimestamp, open, high, low, close]
		"""
		if ( len(self.candles) == self.period+1 ):
			self.candles.pop(0)
		self.candles.append(candle)
		return self.calc()

	def calc (self):
		if ( len(self.candles) == self.period+1 ):
			up   = 0.
			down = 0.
			for index in range(0, len(self.candles)-1):
				delta = self.candles[index+1][4] - self.candles[index][4]
				if delta > 0 :
					u = delta
					d = 0.
				else:
					u = 0.
					d = -delta
				up   = (up*(self.period-1) + u ) / self.period
				down = (down*(self.period-1) + d ) / self.period
			RS  = up/down
			RSI = 100. - (100. / (1. + RS))
#			print "RSI : ", RSI
			return RSI
		else:
			return -1


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


class SMA:
	def __init__ (self, periods):
		self.periods = periods
		self.last_n  = []
		self.ma      = 0

	def put (self, candle, close=True):
		if ( len(self.last_n) == periods ):
			self.last_n.pop(0)
		self.last_n.append(candle)
		result = sum(last_n)/len(last_n)

		# Remove last candle if it did not close
		if ( close == False ):
			self.last_n.pop()
		return result

class Ichimoku:
	''' Incomplete : Ichimoku trading strategy '''
	def __init__ (self, conf_tenkan=8, conf_kijun=11 ):
		self.tenkan   = [conf_tenkan, []]
		self.kijun    = [conf_kijun,  []]
		self.senkou_a = [conf_kijun*2,[]]
		self.senkou_b = [conf_kijun*2,[]]
		print "tenkan count : ", self.tenkan[0]
		print "kijun count  : ", self.kijun[0]

	def put (self, candle):
		""" Candle is of format [unixtimestamp, open, high, low, close]
		"""
		print "put : ", candle

		self.tenkan[1].append(candle)
		if ( len(self.tenkan[1]) > self.tenkan[0] ):
			self.tenkan[1].pop(0)
			# T O H L C

		self.kijun[1].append(candle)
		if ( len(self.kijun[1]) > self.kijun[0] ):
			self.kijun[1].pop(0)



	def push (self, instance, candle):
		count = instance[0]
		array = instance[1]
		if ( len(instance) == count ):
			print "hi"

	def insert (self, line, candle):
		count = line[0];
		if len(line[1]) == count :
			line[1].pop(0)
		line[1].append(candle)


def numpy_moving_average(x, n, type='simple'):
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

def Ruby_numpy (candles, initial_USD, ema1=8, ema2=32, ema3=41, buy_t=0.01, sell_t=0.03):
	"""
	candles: Expecting a list of lists, each candle being [unix_timestamp, Open,
	         High, Low, Close ]
	"""
	# in percent
	buy_threshold  = buy_t    #Default .3%
	sell_threshold = sell_t   #Defaul  .5%
	wallet = Wallet.sim_wallet(5000, 0, 0.55);
	np_candles = np.array(candles)

	# Generate the EMAs
	EMA1  = numpy_moving_average(np_candles[:,4].astype(float), ema1, type='exponential')
	EMA2  = numpy_moving_average(np_candles[:,4].astype(float), ema2, type='exponential')
	EMA3  = numpy_moving_average(np_candles[:,4].astype(float), ema3, type='exponential')

	np_candles_ema = np.column_stack ((np_candles, EMA1,  EMA2, EMA3 ))

	Current_USD = initial_USD
	Current_BTC = 0
	Status = "init"

	for candle in np_candles_ema:
		t_ema1  = candle[5]
		t_ema2  = candle[6]
		t_ema3  = candle[7]
		if  t_ema1 > t_ema3 and t_ema3 > t_ema2 and t_ema1-t_ema3 > candle[4]*buy_threshold and Status != "long" :

			#Current_BTC = Current_USD*(1-0.0055)/candle[4]
			#Current_USD = 0.0
			#print '[BUY BTC ] price:{0:.5f}   BTC:{1:.5f}   USD:{2:.5f}  <{3}> '.format(
			#	candle[4], Current_BTC, Current_USD, datetime.datetime.fromtimestamp(int(candle[0])).strftime('%Y-%m-%d %H:%M:%S'))
			wallet.buy_all(candle[4], candle[0]);
			Status = "long"

		elif t_ema2 > t_ema3 and t_ema3 > t_ema1 and t_ema2-t_ema1 > candle[4]*sell_threshold and Status == "long":

			#Current_USD = Current_BTC*(1-0.0055)*candle[4]
			#Current_BTC = 0.0
			#print '[SELL BTC] price:{0:.5f}   BTC:{1:.5f}   USD:{2:.5f}  <{3}> '.format(
			#	candle[4], Current_BTC, Current_USD, datetime.datetime.fromtimestamp(int(candle[0])).strftime('%Y-%m-%d %H:%M:%S'))
			wallet.sell_all(candle[4], candle[0]);
			Status = "short"

		elif t_ema1-t_ema3 > candle[4]*buy_threshold and Status == "init" :

			#Current_BTC = Current_USD*(1-0.0055)/candle[4]
			#Current_USD = 0.0
			#print '[BUY BTC ] price:{0:.5f}   BTC:{1:.5f}   USD:{2:.5f}  <{3}> '.format(
		    #  	candle[4], Current_BTC, Current_USD, datetime.datetime.fromtimestamp(int(candle[0])).strftime('%Y-%m-%d %H:%M:%S'))
			wallet.buy_all(candle[4], candle[0]);
			Status = "long"

	#if ( Status == "long" ) :
		#Current_USD = Current_BTC*(1-0.0055)*candles[-1][4]

	return wallet.get_balance(candles[-1][4], candles[-1][0]);
	#print "Final RUBY usd  : ${0:.5f}  [BTC Price : ${1:.5f}".format(Current_USD, candles[-1][4])
    #return Current_USD




if __name__ == "__main__":

	print "Hi"
	#ichi = Ichimoku(8,11)
	#ichi.put([12312312, 12, 13, 8, 10])
	#ichi.put([12312312, 12, 13, 8, 10])
	#ichi.put([12312312, 12, 13, 8, 10])


	#wallet = Wallet(5000, 0, 0.55)
	#wallet.buy_all(100,1356994005)
	#wallet.sell_all(150, 1356998005)
	#wallet.get_balance(165, 1356999005)
	#wallet.buy_all(150, 1376994005)
	#wallet.get_balance(150, 1376994990)

