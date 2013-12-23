Number6
=======

Number6* - Trading scripts, back-testing, tickers

Strategy : The strategy used is Ruby from the awesome folks over at TradingView. This is a stacking of
EMAs with line crosses as trading signals. Once the basics are coded, I plan to add enhancements to improve
performance in down-trends.

Using 4 hr, timeframes, as on cryptotrader is severely limiting in a volatile instrument such as bitcoin.
The current implementation will focus one getting to-the minute accurate data, resolved to a suitable
timeframe, such as the 19min charts, for application of trading strategies.

Plotting -> I haven't considered doing this yet, but this would definitely be an interesting exercise
and would help visualise the trading strategy in action.

Live trading -> 


Currently all data is downloaded from bitcoincharts:
wget http://api.bitcoincharts.com/v1/csv/mtgoxUSD.csv
This is a complete trade data list, in the format unixtimestamp, price, volume


* http://en.wikipedia.org/wiki/Number_Six_(Battlestar_Galactica)

Update from last simulation on Dec 16, 2013.

```python
yadu@multivacs:~/src/Number6$ ./candles.py 
Starting date :  2012-12-31 16:00:00
Ending date   :  2013-12-16 05:00:00
[Buy N Hold] price:13.50000   BTC:368.33333   USD:0.00000  <2012-12-31 16:00:00> 
[Selling ] price:857.01130   BTC:368.33333   USD:0.00000  <2013-12-16 05:00:00> 
Buy and Hold 
Inital =  5000
Final  =  313929.666775
Ruby Strategy at 60min candles
Buy threshold  : 1%
Sell threshold : 3%
Simulation start :
[BUY BTC ] price:13.62355   BTC:364.99297   USD:0.00000  <2013-01-07 23:00:00> 
[SELL BTC] price:16.00999   BTC:0.00000   USD:5811.39439  <2013-01-24 19:00:00> 
[BUY BTC ] price:17.54325   BTC:329.43906   USD:0.00000  <2013-01-26 20:00:00> 
[SELL BTC] price:29.49798   BTC:0.00000   USD:9664.33886  <2013-02-23 03:00:00> 
[BUY BTC ] price:30.37498   BTC:316.41782   USD:0.00000  <2013-02-24 11:00:00> 
[SELL BTC] price:40.40000   BTC:0.00000   USD:12712.97195  <2013-03-06 22:00:00> 
[BUY BTC ] price:43.97000   BTC:287.53811   USD:0.00000  <2013-03-08 16:00:00> 
[SELL BTC] price:45.50000   BTC:0.00000   USD:13011.02750  <2013-03-12 01:00:00> 
[BUY BTC ] price:46.37593   BTC:279.01256   USD:0.00000  <2013-03-13 07:00:00> 
[SELL BTC] price:69.00000   BTC:0.00000   USD:19145.98122  <2013-03-22 22:00:00> 
[BUY BTC ] price:67.76500   BTC:280.98101   USD:0.00000  <2013-03-24 07:00:00> 
[SELL BTC] price:89.99901   BTC:0.00000   USD:25148.92889  <2013-03-28 21:00:00> 
[BUY BTC ] price:92.48530   BTC:270.42795   USD:0.00000  <2013-03-30 19:00:00> 
[SELL BTC] price:184.94000   BTC:0.00000   USD:49737.87328  <2013-04-10 15:00:00> 
[BUY BTC ] price:116.00000   BTC:426.41651   USD:0.00000  <2013-04-13 05:00:00> 
[SELL BTC] price:105.71999   BTC:0.00000   USD:44832.80488  <2013-04-13 23:00:00> 
[BUY BTC ] price:80.29997   BTC:555.24584   USD:0.00000  <2013-04-17 03:00:00> 
[SELL BTC] price:139.98700   BTC:0.00000   USD:77299.70009  <2013-04-25 16:00:00> 
[BUY BTC ] price:136.14373   BTC:564.65731   USD:0.00000  <2013-04-27 06:00:00> 
[SELL BTC] price:127.00000   BTC:0.00000   USD:71317.06467  <2013-04-27 16:00:00> 
[BUY BTC ] price:134.00000   BTC:529.28971   USD:0.00000  <2013-04-28 15:00:00> 
[SELL BTC] price:138.47000   BTC:0.00000   USD:72887.64670  <2013-04-30 16:00:00> 
[BUY BTC ] price:101.49999   BTC:714.15539   USD:0.00000  <2013-05-04 05:00:00> 
[SELL BTC] price:108.00000   BTC:0.00000   USD:76704.57350  <2013-05-06 20:00:00> 
[BUY BTC ] price:114.70000   BTC:665.06276   USD:0.00000  <2013-05-08 02:00:00> 
[SELL BTC] price:89.00000   BTC:0.00000   USD:58865.03725  <2013-07-01 13:00:00> 
[BUY BTC ] price:71.64450   BTC:817.10780   USD:0.00000  <2013-07-07 15:00:00> 
[SELL BTC] price:91.70490   BTC:0.00000   USD:74520.65845  <2013-07-13 00:00:00> 
[BUY BTC ] price:95.96710   BTC:772.25210   USD:0.00000  <2013-07-13 20:00:00> 
[SELL BTC] price:89.99500   BTC:0.00000   USD:69116.58449  <2013-07-18 04:00:00> 
[BUY BTC ] price:93.09699   BTC:738.33153   USD:0.00000  <2013-07-19 14:00:00> 
[SELL BTC] price:152.11001   BTC:0.00000   USD:111689.92486  <2013-10-16 21:00:00> 
[BUY BTC ] price:157.40000   BTC:705.69015   USD:0.00000  <2013-10-17 19:00:00> 
[SELL BTC] price:209.00002   BTC:0.00000   USD:146678.06543  <2013-10-24 06:00:00> 
[BUY BTC ] price:193.00000   BTC:755.81003   USD:0.00000  <2013-10-26 09:00:00> 
[SELL BTC] price:320.00000   BTC:0.00000   USD:240528.98441  <2013-11-09 22:00:00> 
[BUY BTC ] price:346.00000   BTC:691.34704   USD:0.00000  <2013-11-11 06:00:00> 
[SELL BTC] price:623.25760   BTC:0.00000   USD:428517.41527  <2013-11-19 19:00:00> 
[BUY BTC ] price:644.99104   BTC:660.72324   USD:0.00000  <2013-11-20 23:00:00> 
[SELL BTC] price:816.00000   BTC:0.00000   USD:536184.83765  <2013-11-24 00:00:00> 
[BUY BTC ] price:867.95000   BTC:614.36237   USD:0.00000  <2013-11-25 23:00:00> 
[SELL BTC] price:1170.00000   BTC:0.00000   USD:714850.55373  <2013-12-01 02:00:00> 
[BUY BTC ] price:1067.00000   BTC:666.27823   USD:0.00000  <2013-12-02 20:00:00> 
[SELL BTC] price:995.00000   BTC:0.00000   USD:659300.63520  <2013-12-05 05:00:00> 
[BUY BTC ] price:699.89999   BTC:936.81167   USD:0.00000  <2013-12-08 09:00:00> 
[SELL BTC] price:926.25310   BTC:0.00000   USD:862952.23179  <2013-12-11 10:00:00> 
[BUY BTC ] price:962.96000   BTC:891.21666   USD:0.00000  <2013-12-13 00:00:00> 
[SELL BTC] price:862.00000   BTC:0.00000   USD:764003.50238  <2013-12-15 00:00:00> 
[BUY BTC ] price:900.00000   BTC:844.22387   USD:0.00000  <2013-12-15 19:00:00> 
Final RUBY usd  : $719530.09475  [BTC Price : $857.01130
Simulation end

```