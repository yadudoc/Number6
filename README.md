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