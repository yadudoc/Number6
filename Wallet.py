#!/usr/bin/env python
import datetime

class sim_wallet ():
	""" Simulated wallet """
	def __init__ (self, usd, btc, fee):
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
		USD = 0
		if ( self.status == "long" ):
			print '[{0}] {1:.5f}BTC AT PRICE:{2:.5f} = ${3:.5f}'.format(
				datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'),
				self.btc, price, self.btc*(1-(self.fee/100)) * price)
			USD = self.btc*(1-(self.fee/100)) * price
		else:
			print '[{0}] HOLDING USD : ${1:.5f}'.format(
				datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'), self.usd)
			USD = self.usd
		return USD

if __name__ == "__main__" :
	wallet = Wallet(5000, 0, 0.55);
	wallet.buy_all(40, 12312312);

