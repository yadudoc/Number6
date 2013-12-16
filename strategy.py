#!/usr/bin/env python
import datetime
import numpy as np

class Wallet ():
	def __init__ (self, usd, btc, fee, pair="BTC_USD"):
		self.pair   = pair
		self.usd    = float(usd)
		self.btc    = float(btc)
		self.fee    = float(fee)  # In percentage applied at buy and sell
		self.status = "short"

	def buy_all (self, price, timestamp):
		self.btc = self.usd*(1-(self.fee/100)) / price
		self.usd = 0.0
		print '[{0}] BUY:  {1:.5f}BTC AT PRICE:{2:.5f}'.format(
			   datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'),
			   self.btc, price)
		self.status = "long"

	def sell_all (self, price, timestamp):
		self.usd = self.btc*(1-(self.fee/100)) * price
		print '[{0}] SELL: {1:.5f}BTC AT PRICE:{2:.5f}'.format(
			   datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'),
			   self.btc, price)
		self.btc = 0
		self.status = "short"

	def get_balance (self, price, timestamp):
		if ( self.status == "long" ):
			print '[{0}] {1:.5f}BTC AT PRICE:{2:.5f} = ${3:.5f}'.format(
				datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'),
				self.btc, price , self.btc*(1-(self.fee/100)) * price)
		else:
			print '[{0}] HOLDING USD : ${1:.5f}'.format(
				datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'), self.usd)

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

class Moving_Average:
	def __init__ (self, periods):
		self.periods = periods
		self.last_n  = []
		self.ema     = 0

	def put (self, candle):
		if ( len(self.last_n) == periods ):
			self.last_n.pop(0)
		self.last_n.append(candle)
		


class Ichimoku:

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



"""
def EMA_Cross (candles, initial_USD):
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
		if   ( ema8-ema41 > candle[4]*buy_threshold ) and Status != "long" :
			Current_BTC = Current_USD*(1-0.0055)/candle[4]
			Current_USD = 0.0
			print '[Going long ] price:{0:.5f}   BTC:{1:.5f}   USD:{2:.5f}  <{3}> '.format(
				candle[4], Current_BTC, Current_USD, datetime.datetime.fromtimestamp(int(candle[0])).strftime('%Y-%m-%d %H:%M:%S'))
			Status = "long"
		elif ema32 > ema41 and ema41 > ema8 and ema32-ema8 > candle[4]*sell_threshold and Status == "long":
			Current_USD = Current_BTC*(1-0.0055)*candle[4]
			Current_BTC = 0.0
			print '[Going short ] price:{0:.5f}   BTC:{1:.5f}   USD:{2:.5f}  <{3}> '.format(
				candle[4], Current_BTC, Current_USD, datetime.datetime.fromtimestamp(int(candle[0])).strftime('%Y-%m-%d %H:%M:%S'))
			Status = "short"
		elif ema8-ema41 > candle[4]*buy_threshold and Status == "init" :
			Current_BTC = Current_USD*(1-0.0055)/candle[4]
			Current_USD = 0.0
			print '[Going long ] price:{0:.5f}   BTC:{1:.5f}   USD:{2:.5f}  <{3}> '.format(
				candle[4], Current_BTC, Current_USD, datetime.datetime.fromtimestamp(int(candle[0])).strftime('%Y-%m-%d %H:%M:%S'))
			Status = "long"

    print "Cashing out at  : {0:.5f} ".format(candles[-1][4])
    if ( Status == "long" ) :
        Current_USD = Current_BTC*(1-0.0055)/candles[-1][4]
    print "Final EMA_cross usd  : ${0:.5f} ".format(Current_USD)
    return Current_USD
"""


if __name__ == "__main__":
	ichi = Ichimoku(8,11)
	ichi.put([12312312, 12, 13, 8, 10])
	ichi.put([12312312, 12, 13, 8, 10])
	ichi.put([12312312, 12, 13, 8, 10])


	wallet = Wallet(5000, 0, 0.55)
	wallet.buy_all(100,1356994005)
	wallet.sell_all(150, 1356998005)
	wallet.get_balance(165, 1356999005)
	wallet.buy_all(150, 1376994005)
	wallet.get_balance(150, 1376994990)
