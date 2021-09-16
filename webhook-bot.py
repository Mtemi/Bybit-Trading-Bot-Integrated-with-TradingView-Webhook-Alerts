"""
Bybit a python bot that works with tradingview's webhook alerts!
This bot is not affiliated with tradingview and was created by https://www.freelancer.com/u/Beannsofts

I expect to update this as much as possible to add features as they become available!
Until then, if you run into any bugs let me know!

"""
import sys
from actions import send_order, parse_webhook, parse__price_webhook
from auth import get_token
from flask import Flask, request, abort
from loguru import logger
import threading, time
import json

# Create Flask object called app.
app = Flask(__name__)


# Create root to easily let us know its on/working.
@app.route('/')
def root():
    return 'Online.'

@logger.catch
@app.route('/price_webhook', methods=['POST'])
def price_webhook():
    if request.method == 'POST':
        # Parse the string data from tradingview into a python dict
        price_data = parse__price_webhook(request.get_data(as_text=True))
        price_data = json.loads(price_data)
        return '', 200
    else:
        abort(400)  

        
@logger.catch
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # Parse the string data from tradingview into a python dict
        
        # datas = parse_webhook(request.get_data(as_text=True))
        # print(datas)
        datas = request.get_data(as_text=True)
        datas = json.loads(datas)
        print(datas)
        # Check that the key is correct
        if get_token() == datas['key']:
            print(' [Alert Received] ')
            print('POST Received/Updated Data:', datas)
            try:
                send_order(datas)
                return '', 200
            except Exception as e:
                print("Error placing your order:\n{0}".format(e))
                return "Error placing your order:\n{0}".format(e)
        else:
            logger.error("Incoming Signal From Unauthorized User.")
            abort(403)

    else:
        abort(400)
        
if __name__ == '__main__' :
  app.run()

"""
if __name__ == '__main__':
    app.run(debug=True)
    app.run(host="212.49.95.112:5055")

#if __name__ == "__main__":
    #from waitress import serve
    #serve(app, host="212.49.95.112", port=80)
"""
