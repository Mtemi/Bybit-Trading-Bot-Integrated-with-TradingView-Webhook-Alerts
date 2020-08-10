# Bybit-Auto-Trading-Bot-Ordes-placed-via-TradingView-Webhook
Python based Bybit.com Trading Bot using TradingView.com alerts via webhooks as a trigger to buy/sell/close/manage positions

User is able to set TradingView alerts and decide what will happen when each one fires.

Options available are as follows

For opening a trade :

Provided
---------
side - Buy, Sell
qty - Which will be the number of contracts - Ideally the user could set a percentage. eg. 10 would mean it would calculate how many contracts 10% of the users balance can get at the current leverage.
symbol - BTCUSD, ETHUSD, XRPUSD, EOSUSD

Others that can be added/ Some like SL/TS are available: 
--------
take profit
stop loss / trailing stop

Before opening a trade it checks to see if the trader is already in a position.

If trader is already in a trade of the same direction it will add to the position automatically. 

If trader is in a trade of the opposite direction it automatically closes that position before opening the new one.

For closing a position the bot provides an option to either exit a certain amount of contracts to take partial profits or the close whole position.


In terms of giving these commands/variables that decide what action to take,the botgoes into two routes.

1. Trading Variables are added inside the webhook as a message that is sent from TradingView. JSON message. 

2. As a trader, you addd the variables to the end of the URL that points to our script and use that as the URL for the webhook to be sent to.

