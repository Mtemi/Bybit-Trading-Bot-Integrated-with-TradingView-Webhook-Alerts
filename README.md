Bybit-Auto-Trading-Bot-Ordes-placed-via-TradingView-Webhook . 

After setting up this bot, which is an easy version, you can also get a more advanced version here: ###https://github.com/Mtemi/BybitTelegramBot   for free. 

# Setup of this Bot: 
You can setup a free version of this bot with the instructions below !!!! 

The code provided here may need some development intuition because it may not necessarily work since Bybit keep updating their REST API endpoints and their websockets. Incase of issues installing the code join our discord here:  https://discord.gg/XKNBAGtmuB and ask the questions you may have. 

Access Bybit Documentation here:  https://bybit-exchange.github.io/docs/inverse/#t-introduction

Join our Discord Server https://discord.gg/bwCJTVDbRr for Assistance and Updates

Upgrade with Telegram integration is available as per your requirements. 

# ..: 

Python based Bybit.com Trading Bot using TradingView.com alerts via webhooks as a trigger to buy/sell/close/manage positions Importantly make sure you create an account on Bybit as well as TradingView: Have knowledge in preparing a python environment, then normal procedures of running python code applies. A web app of this app is in the making. Where you can set your private and public Bybit keys. The parameters are set from TradingView webhooks. several webhooks can be applied. User is able to set TradingView alerts and decide what will happen when each one fires.

Options available are as follows
For opening a trade:
Provided are

side - Buy, Sell qty - Which will be the number of contracts - Ideally the user could set a percentage. eg. 10 would mean it would calculate how many contracts 10% of the users balance can get at the current leverage. symbol - BTCUSD, ETHUSD, XRPUSD, EOSUSD
Others that can be added/ Some like SL/TS are available:
take profit(TP) stop loss(SL) / trailing stop(TS)
Before opening a trade it checks to see if the trader is already in a position.
If trader is already in a trade of the same direction it will add to the position automatically.
If trader is in a trade of the opposite direction it automatically closes that position before opening the new one.
For closing a position the bot provides an option to either exit a certain amount of contracts to take partial profits or the close whole position.
In terms of giving these commands/variables that decide what action to take,the bot goes into two routes.
1.	Trading Variables are added inside the webhook as a message that is sent from TradingView as a JSON message.
2.	As a trader, you addd the variables to the end of the URL that points to our script and use that as the URL for the webhook to be sent to.

# .

Bybit bot is an automated cryptocurrency trading bot that will place orders on Bybit which is not affiliated with TradingView
This is a python bot that works with tradingview's webhook alerts! You need a server with a public IP such as 212.49.95.112 which you have to add to TradingView Webhook section. The server ip need to be configured like below: Lines:  43-46 of webhook-bot.py however more requests and responses can be handled here in future. 
if __name__ == '__main__':
    app.debug = True
    app.run()
    #app.run(host = '212.49.95.112',port=80)
Note: Lines 45 and 46 cannot be active at same time.  Line 45 runs local server ip which is then tunneled to Ngrok.  Line 46 is important if you have public IP and thus you don’t need Ngrok for tunneling. 
Line 46 is commended with # sign so that it’s inactive since line 45 is active for the server to run locally.  In my code I have used Ngrok to tunnel my local server ip: 127.0.0.7:80 to a random temporary public address assigned to me by Ngrok. This is the address I placed on TradingView webhook section. This was I was able to make TradingView requests and responses; see lines 21 – 41 of webhook-bot.py file.   
On the message section, place a JSON formatted message as below: 
 {"type": "Market", "side": "Buy", "amount": "10", "symbol": "BTCUSD", "stopLoss": "1", "leverage": "3", "key": "f7dea65b1c167651e830756a94f13d07f0b8c26b6a46f76f2afed966"}

## Add your Bybit API key and Secret 
Navigate to config.py file and edit the below configurations
```
API_KEY = "Enter your api key here"
API_SECRET = "Enter your api secret here"
IS_TEST = False #set to True if you  are using testnet


```

## TradingView message config
```
{
    "type": "Market",
    "side": "Buy",
    "amount": "10",
    "symbol": "BTCUSD",
    "stopLoss": 3,
    "leverage": "3",
    "trailingStop":"None",
    "takeProfit":1,
    "key": "f7dea65b1c167651e830756a94f13d07f0b8c26b6a46f76f2afed966"
}
```
The symbols vary and here is a list extracted form a function:  print(list(exchange.markets.keys())) found in line 57 of the project file actions.py. 
['.EVOL7D', '.BADAXBT', '.BADAXBT30M', '.BBCHXBT', '.BBCHXBT30M', '.BEOSXBT', '.BEOSXBT30M', '.BXRPXBT', '.BXRPXBT30M', '.BTRXXBT', '.BTRXXBT30M', '.BADAXBT_NEXT', '.BBCHXBT_NEXT', '.BEOSXBT_NEXT', '.BTRXXBT_NEXT', '.BXRPXBT_NEXT', '.BXRP_NEXT', '.BXRP', '.XRPBON', '.XRPBON2H', '.XRPBON8H', '.XRPUSDPI', '.XRPUSDPI2H', '.XRPUSDPI8H', 'XRPH20', 'BCHH20', 'ADAH20', 'EOSH20', 'TRXH20', 'XRP/USD', '.XBT', '.XBT30M', '.XBTBON', '.XBTBON8H', '.XBTUSDPI', '.XBTUSDPI8H', '.XBTBON2H', '.XBTUSDPI2H', '.BXBT', '.BXBT30M', '.BXBT_NEXT', '.BVOL', '.BVOL24H', '.BVOL7D', '.ETHBON', '.ETHBON2H', '.ETHBON8H', '.ETHUSDPI', '.ETHUSDPI2H', '.ETHUSDPI8H', '.BETH', '.BETH30M', '.BETHXBT', '.BETHXBT30M', '.BETH_NEXT', '.BETHXBT_NEXT', '.BLTCXBT', '.BLTCXBT30M', '.BLTCXBT_NEXT', '.USDBON', '.USDBON8H', '.USDBON2H', 'BTC/USD', 'XBTH20', 'XBTM20', 'ETH/USD', 'ETHH20', 'LTCH20']
In our case:  we picked the BTC/USD pair.  You can pick any other coin pair against usdt. I have commended out the function:  print(list(exchange.markets.keys())) found in line 57 of the project file actions.py since I only used it during development to generate markey keys/pais above.  We don’t need it now. 
You will need an Account with Bybiy Platform so that you can generate an API key and secret. 
You will need to open the actions.py file with any text editor and add your API key and secret codes as in below snip. Lines:  15 – 16. 
Next you need to familiarize yourself with basic python syntax and how to setup the environment for various Oss:  Linux, Windows, macOS. Know a bit of pip command as you may use it a lot in setting up the environment. You also need know a bit of OS commands for both linux, windows.  You need some python libraries: Flask, CCXT. 
Install pipenv and initiate virtual environment: (You need start CMD for Windows as here, is where to run commands);
Assume you have pasted the project on this path:  C:\Users\ICT\Documents\projects\Bybitpy). ICT is name of my computer. Then on CMD prompt type: CD C:\Users\ICT\Documents\projects\Bybitpy and Bybitpy will be your active directory. Then proceed with below commands. 
1.	Install pipenv sudo apt install pipenv
2.	Once pipenv is installed, I recommend that you get familiar with it.
3.	Navigate to the folder where you cloned the repo. You should see Pipfile and Pipfile.lock files.
4.	Run command pipenv install
5.	The dependencies required to get started should now be installed. Check by running command pipenv graph - You should see flask and ccxt.
6.	If you want to install any other dependencies, or if you get an error that you're missing a depedency, simply use command pipenv install <dependency>
7.	Starting the virtual environment: pipenv shell
8.	Starting the flask app: python webhook-bot.py
9.	The Pipfile contains required packages, libraries to run the script. They will be considered when running webhook-bot.py. 
On cmd run pip install ccxt then;
pip install flask then; python webhook-bot.py 
Starting a Server
10.	First, we need to start the server that will listen for tradingview's webhooks.
11.	To do that, we're going to use ngrok and flask (python)
12.	Open a new CMD propmpt and navigate to example:  C:\Users\ICT\Documents\projects\Bybitpy; in your case it might be different. 
13.	Start the flask server by running webhook-bot.py
14.	This will create a server on your device, running on the port 5000.
15.	Next, run ngrok http 5000 with the command line. This creates a public address for your app (in this case our webhooks bot). Copy the address ngrok gives you in the console (should look like randomnumbers.ngrok.io). Paste it into your browser and verify that everything is working; you should see "online" in the browser.
Sending Trades
16.	Once the server is displaying "online" you can now start sending trades via tradingview's webhooks. To do this, first copy the script in the pinescript_test.txt file. This is a simple script that will send an alert every minute.
17.	Paste the pinescript in the pinescript editor and add it to your chart. Next, create a new alert. Set the alert to trigger once per minute. Check "webhooks" at the bottom of the new alert window and paste in your ngrok URL. Be sure to add /webhook at the end of it! i.e. random.ngrok.io/webhook
18.	In your ngrok console, you should start seeing POST requests made to the server from tradingview, this means its working!
19.	Now, we can send alerts with the order information (in the body of the alert message)
20.	The data for the alert will look like json, here is an example as we indicated previously.
21.	{"type": "Market", "side": "Buy", "amount": "10", "symbol": "BTCUSD", "stopLoss": "1", "leverage": "3", "key": "f7dea65b1c167651e830756a94f13d07f0b8c26b6a46f76f2afed966"} 
One thing to note, the key is generated by the get_token function in the auth.py script. I feel this adds just a bit of extra security, better safe than sorry! I would recommend changing the pin to something else. The key from the alert has to match the key on your server or the order won't go through.
22.	Note that the json script is generated by the bot. Edit the auth.py file and replace line 8: PIN; 1234 with a passcode of your choice. Go to command prompt and execute the generate_alert_message.py and follow the propmpts on screen to fill details of your JSON taking note of the market symbols we generated previously. Copy the json file generated and paste in the message section of TradingView alerts.  If market symbols are wrong, Bybit will execute an error. 
23.	Other than that, it should be good to go! If you have any questions just ask or create an issue here or on https://freelancer.com/u/Beannsofts
24.	Sample Exchange Results:  
Exchange Response: {'info': {'orderID': '12f8e778-63ab-66d2-12e5-09f0b2b060fa', 'clOrdID': '', 'clOrdLinkID': '', 'account': 815918, 'symbol': 'XBTUSD', 'side': 'Buy', 'simpleOrderQty': None, 'orderQty': 10, 'price': 9690, 'displayQty': None, 'stopPx': None, 'pegOffsetValue': None, 'pegPriceType': '', 'currency': 'USD', 'settlCurrency': 'XBt', 'ordType': 'Limit', 'timeInForce': 'GoodTillCancel', 'execInst': '', 'contingencyType': '', 'exDestination': 'XBME', 'ordStatus': 'New', 'triggered': '', 'workingIndicator': True, 'ordRejReason': '', 'simpleLeavesQty': None, 'leavesQty': 10, 'simpleCumQty': None, 'cumQty': 0, 'avgPx': None, 'multiLegReportingType': 'SingleSecurity', 'text': 'Submitted via API.', 'transactTime': '2020-02-23T15:14:13.498Z', 'timestamp': '2020-02-23T15:14:13.498Z'}, 'id': '12f8e778-63ab-66d2-12e5-09f0b2b060fa', 'timestamp': 1582470853498, 'datetime': '2020-02-23T15:14:13.498Z', 'lastTradeTimestamp': 1582470853498, 'symbol': 'BTC/USD', 'type': 'limit', 'side': 'buy', 'price': 9690.0, 'amount': 10.0, 'cost': 0.0, 'average': None, 'filled': 0.0, 'remaining': 10.0, 'status': 'open', 'fee': None}
    
# Telegram @mutemia or Whatsapp:  +254795557216 !

