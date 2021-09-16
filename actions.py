import logging
from time import sleep
from pybybit import Bybit
import time
import json
import ccxt
import ast
import bybit
from config import Config
# ----- set your configuratins here Configurations ---
bybit_api_key = Config.API_KEY
bybit_api_secret = Config.API_SECRET
is_test = Config.IS_TEST  #set to True if you  are using testnet

def parse__price_webhook(price_webhook_data):

      
    bybit1 = Bybit(api_key=bybit_api_key,
                 secret=bybit_api_secret, symbol=data['symbol'], ws=True, test=is_test)
 

    bybit1.cancel_all_active_orders(symbol=data['symbol'])
    bybit1.cancel_all_conditional_orders(symbol=data['symbol'])
    
    position = bybit1.get_position_http()
    position_result  = position['result']
    json.dumps(position_result, indent=2)
    
    position_side = position_result[0]['side']
    position_size = position_result[0]['size']
    
    if position_side == 'Sell':
        
        position_side = 'Buy'
        bybit1.place_active_order(side='Buy', order_type='Market', qty=position_size,
                                  time_in_force='PostOnly', reduce_only='False')
        position_side = 'Sell'
    if position_side == 'Buy':
        
        position_side = 'Sell'
        bybit1.place_active_order(side='Sell', order_type='Market', qty=position_size,
                                  time_in_force='PostOnly', reduce_only='False')
        position_side == 'Buy'
        
    else: 
        
        print('End of Cancel of All Active, Conditional Orders and Positions')
"""
{"type": "Null",
"side": "Null",
"amount": "Null",
"symbol": "Null",
"takeProfit": " Null",
"stopLoss": "Null",
"trailingStop": "Null",
"leverage": "Null",
"key": "Null"}
"""

def parse_webhook(webhook_data):
    
    data = ast.literal_eval(webhook_data)
    print('Data as Literal', data)
    
    """
    jsonFile = open("data.txt", "r") # Open the JSON file for reading
    datasa = json.load(jsonFile) # Read the JSON into the buffer
    print('Data Read From File', datasa)
    """
    
    with open('data.json', 'r+') as json_file:
        datasa = json.load(json_file)
        print('Data Read From File', datasa)
        datasa.update(data)
        print('Updated Data', datasa)
        #json_file.seek(0)
        #json.dump(datasa,data)
    return datasa

def send_order(data):
  
    #Client API Keys
    bybit1 = Bybit(api_key=bybit_api_key,
                 secret=bybit_api_secret, symbol=data['symbol'], ws=True, test=is_test)
    
    # Send the order to the exchange, using the values from the tradingview alert.
    print('Sending:', data['symbol'], data['type'], data['side'], data['amount'])
    print('Trading Amount:', data['amount'])
    print('Side:', data['side'])
    print('Type:', data['type'])
    wallet_balance = bybit1.get_wallet_balance('BTC')
    print('Wallet Balance ----------------------------------------------------------')
    
    print("Wallet Balance------------------------------------------------((((",wallet_balance)
    if wallet_balance['ret_msg'] !="OK":
        print("Wallet balance fetch error\n", wallet_balance['ret_msg'])
        return "terminate"

    print(wallet_balance['result']['BTC']['available_balance'])
    print('Place Order Amount')
    intamountpercentage  = float(data['amount'])/100
    print('Int Amount Percentage', intamountpercentage)
    intwalletbalance = wallet_balance['result']['BTC']['available_balance']
    print('Wallet Balance', intwalletbalance)

    leverage = bybit1.get_leverage()
    print('Leverage ----------------------------------------------------------')
    print(json.dumps(leverage, indent=2))
    leverages = leverage["result"][data['symbol']]['leverage']
    print("Leverage Value", leverages)
    
    time.sleep(5.0)

    position = bybit1.get_position_http()
    print('Position ----------------------------------------------------------')
    position_result  = position['result']
    print('Position Result Value',position_result)
    json.dumps(position_result, indent=2)
    print('Position Result', position_result[0]['data']['side'])
    position_side = position_result[0]['data']['side']
    position_take_profit = position_result[0]['data']['take_profit']
    print('Position Take Profit', position_take_profit)
    position_stop_loss = position_result[0]['data']['stop_loss']
    print('Position Stop Loss', position_stop_loss)
    print('Order ID ----------------------------------------------------------')
    order_idss = position_result[0]['data']['id']
    print('Example Order ID',order_idss)
    #print(position['entry_price'])

    ticker = bybit1.get_tickers(data['symbol'])
    print(json.dumps(ticker, indent=2))
    tickers = ticker["result"]
    print("Tickers ",tickers)
    tick = tickers[0]
    print("Last Price", tick['last_price'])
    last_price = float(tick['bid_price'])
    #print("Bid Price Value Two", last_price)

    #The Position Entry Price Irrespective of where position or not
    print("Position Entry Price", position_result[0]['data']['entry_price']) 
    entry_price = float(position_result[0]['data']['entry_price'])
    print("Bid Price Value Two", entry_price)

    orderamounts = intwalletbalance*last_price
    print("Order Amount", orderamounts)
    orderamount  = orderamounts*intamountpercentage
    print('Order Amount in USD', orderamount)

    #Get Active Order Real Time
    real_time_active_order = bybit1.get_active_order(data['symbol'])
    print('Active Order Real Time ----------------------------------------------------------')
    real_time_active_order_result  = real_time_active_order['result']
    print('Real time active order result',real_time_active_order_result)
    json.dumps(real_time_active_order_result, indent=2)
    print('Real time active order result Intented Results',real_time_active_order_result)


    global nonebuy
    global nonesell 
    global oldqty
    global oldprice
    global oldqtysell
    global oldpricesell


    if position_side == 'None' and data['side']=='Buy' and data['trailingStop']=='None':


        print('Stop Loss by 100 ----------------------------------------------------------')
        sLoss = float(data['stopLoss'])
        print(sLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        stopLossby100 = sLoss/100
        print(stopLossby100*last_price)
        stoploss = last_price-(stopLossby100*last_price)
        print('Stop Loss Margin----------------------------------------------------------')
        print(stoploss)
        
        # print('Trailing Stop by 100 ----------------------------------------------------------')
        # tsLoss = float(data['trailingStop'])
        # print(tsLoss/100)
        # print('Multiply By Entry Price ----------------------------------------------------------')
        # tstopLossby100 = tsLoss/100
        # print(tstopLossby100*last_price)
        # tstoploss = tstopLossby100*last_price
        # print('Trailing Stop ----------------------------------------------------------')
        # print(tstoploss)

        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        stop_loss=stoploss,time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
 

        data['type'] = 'Limit'
        data['side'] = 'Sell'
        #We want to Add TP to the Market Order
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = orderamount,time_in_force='PostOnly', reduce_only='True')
        print(json.dumps(order_resp, indent=2))
        nonebuy = order_resp['result']['order_id'] if order_resp['result'] else None
        oldqty = orderamount
        nonebuy = nonebuy
        

        print('Order ID for this Sale', nonebuy)


        """
        order_resp = bybit1.replace_active_order(order_id = nonebuy, symbol = data['symbol'],
        p_r_qty = position_value, p_r_price = takeprofit)
        """

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")

        data['side']='Buy'
        
    if position_side == 'None' and data['side']=='Sell' and data['takeProfit']!='None' and data['stopLoss']!='None' and data['trailingStop']=='None':  
        # if there is no order Position at All
        # and we have a new Sell Order
        print("None   Sell order being executed")
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = last_price - (takeProfitby100*last_price)
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)

        print('Stop Loss by 100 ----------------------------------------------------------')
        sLoss = float(data['stopLoss'])
        print(sLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        stopLossby100 = sLoss/100
        print(stopLossby100*last_price)
        stoploss = (stopLossby100*last_price) + last_price
        print('Stop Loss Margin----------------------------------------------------------')
        print(stoploss)

        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        stop_loss=stoploss,time_in_force='PostOnly', reduce_only='False')
        #print(json.dumps(order_resp, indent=2))
        order_idss = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_idss)


        data['type'] = 'Limit'
        data['side'] = 'Buy'
        #We want to Add TP to the Market Order
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = orderamount, price=takeprofit,time_in_force='PostOnly', reduce_only='True')
        print(json.dumps(order_resp, indent=2))
        nonesell = order_resp['result']['order_id'] if order_resp['result'] else None
        oldqtysell = orderamount
        oldpricesell = stoploss
        nonesell = nonesell

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")  

        data['side']='Sell'

    if position_side == 'Buy' and data['side']=='Buy' and data['takeProfit']!='None' and data['stopLoss']!='None' and data['trailingStop']=='None':  
        # if there is no order Position at All
        
        data['side'] = 'Sell'
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')
        
        data['side'] = 'Buy'
        # and we have a new Buy Order
        print("Buy  Buy order being executed" )
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = (takeProfitby100*last_price)+last_price
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)

        print('Stop Loss by 100 ----------------------------------------------------------')
        sLoss = float(data['stopLoss'])
        print(sLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        stopLossby100 = sLoss/100
        print(stopLossby100*last_price)
        stoploss = last_price-(stopLossby100*last_price)
        print('Stop Loss Margin----------------------------------------------------------')
        print(stoploss)
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount+position_value,
        stop_loss=stoploss,time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else 'None'
        print(order_ids)
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        data['type'] = 'Limit'
        data['side'] = 'Sell'
        #We want to Add TP to the Market Order
                #We want to Add TP to the Market Order
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        tprofit = float(data['takeProfit'])
        takeProfitby100 = tprofit/100
        takeprofit = (takeProfitby100*entry_price)+entry_price
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position')
        #,p_r_qty = int(orderamount), p_r_price = int(entry_price)
        #order_resp = bybit1.replace_active_order(order_id = nonebuy, symbol = data['symbol'], 
        #p_r_qty = position_value, p_r_price = int(takeprofit)) 
        
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value, price=int(takeprofit),time_in_force='PostOnly', reduce_only='True')
        
        print(json.dumps(order_resp, indent=2))
        nonebuy = order_resp['result']['order_id'] if order_resp['result'] else None
        

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")


        data['side']='Buy'

    if position_side == 'Sell' and data['side']=='Sell'and data['takeProfit']!='None' and data['stopLoss']!='None' and data['trailingStop']=='None':  # if there is no order Position at All
        # and we have a new Sell Order
        data['side'] = 'Buy'
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')
        
        data['side'] = 'Sell'
        print("None Sell order being executed")
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = last_price - (takeProfitby100*last_price)
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)

        print('Stop Loss by 100 ----------------------------------------------------------')
        sLoss = float(data['stopLoss'])
        print(sLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        stopLossby100 = sLoss/100
        print(stopLossby100*last_price)
        stoploss = (stopLossby100*last_price) + last_price
        print('Stop Loss Margin----------------------------------------------------------')
        print(stoploss)
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount+position_value,
        stop_loss=stoploss,time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        
        data['type'] = 'Limit'
        data['side'] = 'Buy'
        
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        tprofit = float(data['takeProfit'])
        takeProfitby100 = tprofit/100
        takeprofit = entry_price-(takeProfitby100*entry_price)
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position and ',position_value,'Position Value')
        print('And ', takeprofit,'Take profit Value')
        print('And ', entry_price,'Position Entry price Value')
        
        
        """
        order_resp = bybit1.replace_active_order(order_id = nonesell, symbol = data['symbol'], 
        p_r_qty = position_value, p_r_price = int(takeprofit)) 
        """
        
        """"""
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value, price=int(takeprofit),time_in_force='PostOnly', reduce_only='True')
        print(json.dumps(order_resp, indent=2))
        order_resp = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_resp)

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")

        data['side']='Sell'
        
    if position_side == 'Sell' and data['side']=='Buy'and data['takeProfit']!='None' and data['stopLoss']!='None' and data['trailingStop']=='None': 
        
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')

        # and we have a new Buy Order
        print("Buy  Buy order being executed" )
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = (takeProfitby100*last_price)+last_price
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)

        print('Stop Loss by 100 ----------------------------------------------------------')
        sLoss = float(data['stopLoss'])
        print(sLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        stopLossby100 = sLoss/100
        print(stopLossby100*last_price)
        stoploss = last_price-(stopLossby100*last_price)
        print('Stop Loss Margin----------------------------------------------------------')
        print(stoploss)
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        stop_loss=stoploss,time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        data['type'] = 'Limit'
        data['side'] = 'Sell'
        #We want to Add TP to the Market Order
                #We want to Add TP to the Market Order
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        tprofit = float(data['takeProfit'])
        takeProfitby100 = tprofit/100
        takeprofit = (takeProfitby100*entry_price)+entry_price
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position')
        #,p_r_qty = int(orderamount), p_r_price = int(entry_price)
        #order_resp = bybit1.replace_active_order(order_id = nonebuy, symbol = data['symbol'], 
        #p_r_qty = position_value, p_r_price = int(takeprofit)) 
        
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value, price=int(takeprofit),time_in_force='PostOnly', reduce_only='True')
        
        print(json.dumps(order_resp, indent=2))
        nonebuy = order_resp['result']['order_id'] if order_resp['result'] else None
        

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")


        data['side']='Buy'

    if position_side == 'Buy' and data['side']=='Sell'and data['takeProfit']!='None' and data['stopLoss']!='None' and data['trailingStop']=='None':
        
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')
        
        data['side'] = 'Sell'
        print("None Sell order being executed")
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = last_price - (takeProfitby100*last_price)
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)

        print('Stop Loss by 100 ----------------------------------------------------------')
        sLoss = float(data['stopLoss'])
        print(sLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        stopLossby100 = sLoss/100
        print(stopLossby100*last_price)
        stoploss = (stopLossby100*last_price) + last_price
        print('Stop Loss Margin----------------------------------------------------------')
        print(stoploss)
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        stop_loss=stoploss,time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        
        data['type'] = 'Limit'
        data['side'] = 'Buy'
        
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        tprofit = float(data['takeProfit'])
        takeProfitby100 = tprofit/100
        takeprofit = entry_price-(takeProfitby100*entry_price)
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position and ',position_value,'Position Value')
        print('And ', takeprofit,'Take profit Value')
        print('And ', entry_price,'Position Entry price Value')
        
        
        """
        order_resp = bybit1.replace_active_order(order_id = nonesell, symbol = data['symbol'], 
        p_r_qty = position_value, p_r_price = int(takeprofit)) 
        """
        
        """"""
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value, price=int(takeprofit),time_in_force='PostOnly', reduce_only='True')
        print(json.dumps(order_resp, indent=2))
        order_resp = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_resp)

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")

        data['side']='Sell' 
        
        #-----------------------------------------------------------------------------------------------------------------
        
    if position_side == 'None' and data['side']=='Buy' and data['takeProfit']=='None' and data['stopLoss']!='None' and data['trailingStop']=='None':
        # if there is no order Position at All
        # and we have a new Buy Order
        print("None  Buy order being executed")
        # Since a Buy Position has been Opened, First Thing we set data type to Limit
      

        print('Stop Loss by 100 ----------------------------------------------------------')
        sLoss = float(data['stopLoss'])
        print(sLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        stopLossby100 = sLoss/100
        print(stopLossby100*last_price)
        stoploss = last_price-(stopLossby100*last_price)
        print('Stop Loss Margin----------------------------------------------------------')
        print(stoploss)

        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
 
		
        data['type'] = 'Limit'
        data['side'] = 'Sell'
        #We want to Add TP to the Market Order
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = orderamount, time_in_force='PostOnly', reduce_only='True')
        print(json.dumps(order_resp, indent=2))
        nonebuy = order_resp['result']['order_id'] if order_resp['result'] else None
        oldqty = orderamount
        

        print('Order ID for this Sale', nonebuy)


        """
        order_resp = bybit1.replace_active_order(order_id = nonebuy, symbol = data['symbol'],
        p_r_qty = position_value, p_r_price = takeprofit)
        """

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")

        data['side']='Buy'
        
    if position_side == 'None' and data['side']=='Sell' and data['takeProfit']=='None' and data['stopLoss']!='None' and data['trailingStop']=='None':  
        # if there is no order Position at All
        # and we have a new Sell Order
        print("None   Sell order being executed")
       

        print('Stop Loss by 100 ----------------------------------------------------------')
        sLoss = float(data['stopLoss'])
        print(sLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        stopLossby100 = sLoss/100
        print(stopLossby100*last_price)
        stoploss = (stopLossby100*last_price) + last_price
        print('Stop Loss Margin----------------------------------------------------------')
        print(stoploss)

        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        time_in_force='PostOnly', reduce_only='False')
        #print(json.dumps(order_resp, indent=2))
        order_idss = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_idss)


        data['type'] = 'Limit'
        data['side'] = 'Buy'
        #We want to Add TP to the Market Order
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = orderamount, time_in_force='PostOnly', reduce_only='True')
        print(json.dumps(order_resp, indent=2))
        nonesell = order_resp['result']['order_id'] if order_resp['result'] else None
        oldqtysell = orderamount
        oldpricesell = stoploss
        nonesell = nonesell

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")  

        data['side']='Sell'

    if position_side == 'Buy' and data['side']=='Buy' and data['takeProfit']=='None' and data['stopLoss']!='None' and data['trailingStop']=='None':  
        # if there is no order Position at All
        
        data['side'] = 'Sell'
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')
        
        data['side'] = 'Buy'
        # and we have a new Buy Order
        print("Buy  Buy order being executed" )
     

        print('Stop Loss by 100 ----------------------------------------------------------')
        sLoss = float(data['stopLoss'])
        print(sLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        stopLossby100 = sLoss/100
        print(stopLossby100*last_price)
        stoploss = last_price-(stopLossby100*last_price)
        print('Stop Loss Margin----------------------------------------------------------')
        print(stoploss)
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount+position_value,
        stop_loss=stoploss,time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        data['type'] = 'Limit'
        data['side'] = 'Sell'
        #We want to Add TP to the Market Order
                #We want to Add TP to the Market Order
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        tprofit = float(data['takeProfit'])
        takeProfitby100 = tprofit/100
        takeprofit = (takeProfitby100*entry_price)+entry_price
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position')
        #,p_r_qty = int(orderamount), p_r_price = int(entry_price)
        #order_resp = bybit1.replace_active_order(order_id = nonebuy, symbol = data['symbol'], 
        #p_r_qty = position_value, p_r_price = int(takeprofit)) 
        
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value,time_in_force='PostOnly', reduce_only='True')
        
        print(json.dumps(order_resp, indent=2))
        nonebuy = order_resp['result']['order_id'] if order_resp['result'] else None
        

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")


        data['side']='Buy'

    if position_side == 'Sell' and data['side']=='Sell'and data['takeProfit']=='None' and data['stopLoss']!='None' and data['trailingStop']=='None':  # if there is no order Position at All
        # and we have a new Sell Order
        data['side'] = 'Buy'
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')
        
        data['side'] = 'Sell'
        print("None Sell order being executed")
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = last_price - (takeProfitby100*last_price)
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)

        print('Stop Loss by 100 ----------------------------------------------------------')
        sLoss = float(data['stopLoss'])
        print(sLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        stopLossby100 = sLoss/100
        print(stopLossby100*last_price)
        stoploss = (stopLossby100*last_price) + last_price
        print('Stop Loss Margin----------------------------------------------------------')
        print(stoploss)
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount+position_value,
        stop_loss=stoploss,time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        
        data['type'] = 'Limit'
        data['side'] = 'Buy'
        
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        tprofit = float(data['takeProfit'])
        takeProfitby100 = tprofit/100
        takeprofit = entry_price-(takeProfitby100*entry_price)
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position and ',position_value,'Position Value')
        print('And ', takeprofit,'Take profit Value')
        print('And ', entry_price,'Position Entry price Value')
        
        
        """
        order_resp = bybit1.replace_active_order(order_id = nonesell, symbol = data['symbol'], 
        p_r_qty = position_value, p_r_price = int(takeprofit)) 
        """
        
        """"""
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value,time_in_force='PostOnly', reduce_only='True')
        print(json.dumps(order_resp, indent=2))
        order_resp = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_resp)

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")

        data['side']='Sell'
        
    if position_side == 'Sell' and data['side']=='Buy'and data['takeProfit']=='None' and data['stopLoss']!='None' and data['trailingStop']=='None': 
        
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')

        # and we have a new Buy Order
        print("Buy  Buy order being executed" )
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = (takeProfitby100*last_price)+last_price
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)

        print('Stop Loss by 100 ----------------------------------------------------------')
        sLoss = float(data['stopLoss'])
        print(sLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        stopLossby100 = sLoss/100
        print(stopLossby100*last_price)
        stoploss = last_price-(stopLossby100*last_price)
        print('Stop Loss Margin----------------------------------------------------------')
        print(stoploss)
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        stop_loss=stoploss,time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        data['type'] = 'Limit'
        data['side'] = 'Sell'
        #We want to Add TP to the Market Order
                #We want to Add TP to the Market Order
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        tprofit = float(data['takeProfit'])
        takeProfitby100 = tprofit/100
        takeprofit = (takeProfitby100*entry_price)+entry_price
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position')
        #,p_r_qty = int(orderamount), p_r_price = int(entry_price)
        #order_resp = bybit1.replace_active_order(order_id = nonebuy, symbol = data['symbol'], 
        #p_r_qty = position_value, p_r_price = int(takeprofit)) 
        
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value,time_in_force='PostOnly', reduce_only='True')
        
        print(json.dumps(order_resp, indent=2))
        nonebuy = order_resp['result']['order_id'] if order_resp['result'] else None
        

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")


        data['side']='Buy'

    if position_side == 'Buy' and data['side']=='Sell'and data['takeProfit']=='None' and data['stopLoss']!='None' and data['trailingStop']=='None':
        
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')
        
        data['side'] = 'Sell'
        print("None Sell order being executed")
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = last_price - (takeProfitby100*last_price)
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)

        print('Stop Loss by 100 ----------------------------------------------------------')
        sLoss = float(data['stopLoss'])
        print(sLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        stopLossby100 = sLoss/100
        print(stopLossby100*last_price)
        stoploss = (stopLossby100*last_price) + last_price
        print('Stop Loss Margin----------------------------------------------------------')
        print(stoploss)
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        stop_loss=stoploss,time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        
        data['type'] = 'Limit'
        data['side'] = 'Buy'
        
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        tprofit = float(data['takeProfit'])
        takeProfitby100 = tprofit/100
        takeprofit = entry_price-(takeProfitby100*entry_price)
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position and ',position_value,'Position Value')
        print('And ', takeprofit,'Take profit Value')
        print('And ', entry_price,'Position Entry price Value')
        
        
        """
        order_resp = bybit1.replace_active_order(order_id = nonesell, symbol = data['symbol'], 
        p_r_qty = position_value, p_r_price = int(takeprofit)) 
        """
        
        """"""
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value, time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_resp = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_resp)

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")

        data['side']='Sell' 
        
        #-----------------------------------------------------------------------------------------------------------

    if position_side == 'None' and data['side']=='Buy' and data['takeProfit']!='None' and data['stopLoss']=='None' and data['trailingStop']=='None':
        # if there is no order Position at All
        # and we have a new Buy Order
        print("None  Buy order being executed")
        # Since a Buy Position has been Opened, First Thing we set data type to Limit
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = (takeProfitby100*last_price)+last_price
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)

        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
 
        bybit1.cancel_all_active_orders(symbol=data['symbol'])    
    
        data['type'] = 'Limit'
        data['side'] = 'Sell'
        #We want to Add TP to the Market Order
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = orderamount, price=takeprofit,time_in_force='PostOnly', reduce_only='True')
        print(json.dumps(order_resp, indent=2))
        nonebuy = order_resp['result']['order_id'] if order_resp['result'] else None
        oldqty = orderamount
        oldprice = takeprofit
        nonebuy = nonebuy
        

        print('Order ID for this Sale', nonebuy)


        """
        order_resp = bybit1.replace_active_order(order_id = nonebuy, symbol = data['symbol'],
        p_r_qty = position_value, p_r_price = takeprofit)
        """

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")

        data['side']='Buy'
        
    if position_side == 'None' and data['side']=='Sell' and data['takeProfit']!='None' and data['stopLoss']=='None' and data['trailingStop']=='None':  
        # if there is no order Position at All
        # and we have a new Sell Order
        print("None   Sell order being executed")
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = last_price - (takeProfitby100*last_price)
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)

        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        time_in_force='PostOnly', reduce_only='False')
        #print(json.dumps(order_resp, indent=2))
        order_idss = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_idss)
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])

        data['type'] = 'Limit'
        data['side'] = 'Buy'
        #We want to Add TP to the Market Order
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = orderamount, price=takeprofit,time_in_force='PostOnly', reduce_only='True')
        print(json.dumps(order_resp, indent=2))
        nonesell = order_resp['result']['order_id'] if order_resp['result'] else None
        oldqtysell = orderamount
        nonesell = nonesell

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")  

        data['side']='Sell'

    if position_side == 'Buy' and data['side']=='Buy' and data['takeProfit']!='None' and data['stopLoss']=='None' and data['trailingStop']=='None': 
        # if there is no order Position at All
        
        data['side'] = 'Sell'
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')

        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount+position_value,
        time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        data['type'] = 'Limit'
        data['side'] = 'Sell'
        #We want to Add TP to the Market Order
                #We want to Add TP to the Market Order
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        tprofit = float(data['takeProfit'])
        takeProfitby100 = tprofit/100
        takeprofit = (takeProfitby100*entry_price)+entry_price
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position')
        #,p_r_qty = int(orderamount), p_r_price = int(entry_price)
        #order_resp = bybit1.replace_active_order(order_id = nonebuy, symbol = data['symbol'], 
        #p_r_qty = position_value, p_r_price = int(takeprofit)) 

        #order_rep = bybit1.replace_active_order(order_id = real_time_active_order_result['order_id'], symbol=data['symbol'],
        #                     p_r_qty=orderamount+position_value, p_r_price=int(takeprofit))
        
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
                     qty = position_value, price=int(takeprofit),time_in_force='PostOnly', reduce_only='True')
        
        print(json.dumps(order_resp, indent=2))
        nonebuy = order_resp['result']['order_id'] if order_resp['result'] else None
        

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")


        data['side']='Buy'

    if position_side == 'Sell' and data['side']=='Sell'and data['takeProfit']!='None' and data['stopLoss']=='None' and data['trailingStop']=='None': 
        # if there is no order Position at All
        # and we have a new Sell Order
        data['side'] = 'Buy'
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')
        
        data['side'] = 'Sell'
        print("None Sell order being executed")
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = last_price - (takeProfitby100*last_price)
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)

        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount+position_value,
        time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        
        data['type'] = 'Limit'
        data['side'] = 'Buy'
        
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        tprofit = float(data['takeProfit'])
        takeProfitby100 = tprofit/100
        takeprofit = entry_price-(takeProfitby100*entry_price)
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position and ',position_value,'Position Value')
        print('And ', takeprofit,'Take profit Value')
        print('And ', entry_price,'Position Entry price Value')
        
        
        """
        order_resp = bybit1.replace_active_order(order_id = nonesell, symbol = data['symbol'], 
        p_r_qty = position_value, p_r_price = int(takeprofit)) 
        """
        
        """"""
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value, price=int(takeprofit),time_in_force='PostOnly', reduce_only='True')
        print(json.dumps(order_resp, indent=2))
        order_resp = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_resp)

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")

        data['side']='Sell'
        
    if position_side == 'Sell' and data['side']=='Buy'and data['takeProfit']!='None' and data['stopLoss']=='None' and data['trailingStop']=='None': 
        
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')

        # and we have a new Buy Order
        print("Buy  Buy order being executed" )
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = (takeProfitby100*last_price)+last_price
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        data['type'] = 'Limit'
        data['side'] = 'Sell'
        #We want to Add TP to the Market Order
                #We want to Add TP to the Market Order
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        tprofit = float(data['takeProfit'])
        takeProfitby100 = tprofit/100
        takeprofit = (takeProfitby100*entry_price)+entry_price
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position')
        #,p_r_qty = int(orderamount), p_r_price = int(entry_price)
        #order_resp = bybit1.replace_active_order(order_id = nonebuy, symbol = data['symbol'], 
        #p_r_qty = position_value, p_r_price = int(takeprofit)) 
        
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value, price=int(takeprofit),time_in_force='PostOnly', reduce_only='True')
        
        print(json.dumps(order_resp, indent=2))
        nonebuy = order_resp['result']['order_id'] if order_resp['result'] else None
        

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")


        data['side']='Buy'

    if position_side == 'Buy' and data['side']=='Sell'and data['takeProfit']!='None' and data['stopLoss']=='None' and data['trailingStop']=='None':
        
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')
        
        data['side'] = 'Sell'
        print("None Sell order being executed")
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = last_price - (takeProfitby100*last_price)
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        data['type'] = 'Limit'
        data['side'] = 'Buy'
        
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        tprofit = float(data['takeProfit'])
        takeProfitby100 = tprofit/100
        takeprofit = entry_price-(takeProfitby100*entry_price)
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position and ',position_value,'Position Value')
        print('And ', takeprofit,'Take profit Value')
        print('And ', entry_price,'Position Entry price Value')
        
        
        """
        order_resp = bybit1.replace_active_order(order_id = nonesell, symbol = data['symbol'], 
        p_r_qty = position_value, p_r_price = int(takeprofit)) 
        """
        
        """"""
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value, price=int(takeprofit),time_in_force='PostOnly', reduce_only='True')
        print(json.dumps(order_resp, indent=2))
        order_resp = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_resp)

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")

        data['side']='Sell' 
        
        #---------------------------------------------------------------------------------------------------------------
        
    if position_side == 'None' and data['side']=='Buy' and data['takeProfit']=='None' and data['stopLoss']=='None' and data['trailingStop']=='None':
        

        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        

        data['type'] = 'Limit'
        data['side'] = 'Sell'
        #We want to Add TP to the Market Order
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = orderamount, time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        nonebuy = order_resp['result']['order_id'] if order_resp['result'] else None
        oldqty = orderamount
        nonebuy = nonebuy
        

        print('Order ID for this Sale', nonebuy)

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")

        data['side']='Buy'
        
    if position_side == 'None' and data['stopLoss']=='None' and data['trailingStop']=='None':  


        data['type'] = 'Limit'
        data['side'] = 'Buy'
        #We want to Add TP to the Market Order
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = orderamount, time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        nonesell = order_resp['result']['order_id'] if order_resp['result'] else None
        oldqtysell = orderamount
        nonesell = nonesell

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")  

        data['side']='Sell'

    if position_side == 'Buy'and data['side']=='Buy' and data['takeProfit']=='None' and data['stopLoss']=='None' and data['trailingStop']=='None':  # if there is no order Position at All
        
        data['side'] = 'Sell'
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')
        
        data['side'] = 'Buy'
        # and we have a new Buy Order
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount+position_value,
        time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        data['type'] = 'Limit'
        data['side'] = 'Sell'
        #We want to Add TP to the Market Order
                #We want to Add TP to the Market Order
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position')
        #,p_r_qty = int(orderamount), p_r_price = int(entry_price)
        #order_resp = bybit1.replace_active_order(order_id = nonebuy, symbol = data['symbol'], 
        #p_r_qty = position_value, p_r_price = int(takeprofit)) 
        
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value,time_in_force='PostOnly', reduce_only='False')
        
        print(json.dumps(order_resp, indent=2))
        nonebuy = order_resp['result']['order_id'] if order_resp['result'] else None
        

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")


        data['side']='Buy'

    if position_side == 'Sell' and data['side']=='Sell'and data['takeProfit']=='None' and data['stopLoss']=='None' and data['trailingStop']=='None':  
        # if there is no order Position at All
        # and we have a new Sell Order
        data['side'] = 'Buy'
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')
        
        data['side'] = 'Sell'
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount+position_value,
        time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        
        data['type'] = 'Limit'
        data['side'] = 'Buy'
        
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position and ',position_value,'Position Value')
        print('And ', entry_price,'Position Entry price Value')
        
        
        """
        order_resp = bybit1.replace_active_order(order_id = nonesell, symbol = data['symbol'], 
        p_r_qty = position_value, p_r_price = int(takeprofit)) 
        """
        
        """"""
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value, time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_resp = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_resp)

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")

        data['side']='Sell'
        
    if position_side == 'Sell' and data['side']=='Buy'and data['takeProfit']=='None' and data['stopLoss']=='None' and data['trailingStop']=='None': 
        
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')

        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        data['type'] = 'Limit'
        data['side'] = 'Sell'
        #We want to Add TP to the Market Order
                #We want to Add TP to the Market Order
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position')
        #,p_r_qty = int(orderamount), p_r_price = int(entry_price)
        #order_resp = bybit1.replace_active_order(order_id = nonebuy, symbol = data['symbol'], 
        #p_r_qty = position_value, p_r_price = int(takeprofit)) 
        
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value, time_in_force='PostOnly', reduce_only='False')
        
        print(json.dumps(order_resp, indent=2))
        nonebuy = order_resp['result']['order_id'] if order_resp['result'] else None
        

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")


        data['side']='Buy'

    if position_side == 'Buy' and data['side']=='Sell'and data['takeProfit']=='None' and data['stopLoss']=='None' and data['trailingStop']=='None':
        
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')
        
        data['side'] = 'Sell'
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        data['type'] = 'Limit'
        data['side'] = 'Buy'
        
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position and ',position_value,'Position Value')
        print('And ', entry_price,'Position Entry price Value')

        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value,time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_resp = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_resp)

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")

        data['side']='Sell' 
        
        #---------------------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------------------------------
        #----------Start of Code where Trailing Stop is Activated-----------------------------------------
    
    if position_side == 'None' and data['side']=='Buy' and data['takeProfit']!='None'  and data['stopLoss']!='None' and data['trailingStop']!='None':
        # if there is no order Position at All
        # and we have a new Buy Order
        print("None  Buy order being executed")
        # Since a Buy Position has been Opened, First Thing we set data type to Limit
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = (takeProfitby100*last_price)+last_price
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)

        print('Stop Loss by 100 ----------------------------------------------------------')
        sLoss = float(data['stopLoss'])
        print(sLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        stopLossby100 = sLoss/100
        print(stopLossby100*last_price)
        stoploss = last_price-(stopLossby100*last_price)
        print('Stop Loss Margin----------------------------------------------------------')
        print(stoploss)
        
        print('Trailing Stop by 100 ----------------------------------------------------------')
        tsLoss = float(data['trailingStop'])
        print(tsLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        tstopLossby100 = tsLoss/100
        print(tstopLossby100*last_price)
        tstoploss = tstopLossby100*last_price
        print('Trailing Stop  Margin ----------------------------------------------------------')
        print(tstoploss)

        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        stop_loss=stoploss,time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        
        print('Activating Trailing Stop')
        order_resp = bybit1.place_active_order_ts(symbol=data['symbol'], trailing_stop = tstoploss)
        print(json.dumps(order_resp, indent=2))
 

        data['type'] = 'Limit'
        data['side'] = 'Sell'
        #We want to Add TP to the Market Order
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = orderamount, price=takeprofit,time_in_force='PostOnly', reduce_only='True')
        print(json.dumps(order_resp, indent=2))
        nonebuy = order_resp['result']['order_id'] if order_resp['result'] else None
        oldqty = orderamount
        oldprice = takeprofit
        nonebuy = nonebuy
        

        print('Order ID for this Sale', nonebuy)


        """
        order_resp = bybit1.replace_active_order(order_id = nonebuy, symbol = data['symbol'],
        p_r_qty = position_value, p_r_price = takeprofit)
        """

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")

        data['side']='Buy'
        
    if position_side == 'None' and data['side']=='Sell' and data['takeProfit']!='None' and data['stopLoss']!='None' and data['trailingStop']!='None':  
        # if there is no order Position at All
        # and we have a new Sell Order
        print("None   Sell order being executed")
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = last_price - (takeProfitby100*last_price)
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)

        print('Stop Loss by 100 ----------------------------------------------------------')
        sLoss = float(data['stopLoss'])
        print(sLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        stopLossby100 = sLoss/100
        print(stopLossby100*last_price)
        stoploss = (stopLossby100*last_price) + last_price
        print('Stop Loss Margin----------------------------------------------------------')
        print(stoploss)
        
        print('Trailing Stop by 100 ----------------------------------------------------------')
        tsLoss = float(data['trailingStop'])
        print(tsLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        tstopLossby100 = tsLoss/100
        print(tstopLossby100*last_price)
        tstoploss = tstopLossby100*last_price
        print('Trailing Stop  Margin ----------------------------------------------------------')
        print(tstoploss)

        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        stop_loss=stoploss,time_in_force='PostOnly', reduce_only='False')
        #print(json.dumps(order_resp, indent=2))
        order_idss = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_idss)
        
        print('Activating Trailing Stop')
        order_resp = bybit1.place_active_order_ts(symbol=data['symbol'], trailing_stop = tstoploss)
        print(json.dumps(order_resp, indent=2))


        data['type'] = 'Limit'
        data['side'] = 'Buy'
        #We want to Add TP to the Market Order
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = orderamount, price=takeprofit,time_in_force='PostOnly', reduce_only='True')
        print(json.dumps(order_resp, indent=2))
        nonesell = order_resp['result']['order_id'] if order_resp['result'] else None
        oldqtysell = orderamount
        oldpricesell = stoploss
        nonesell = nonesell

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")  

        data['side']='Sell'

    if position_side == 'Buy' and data['side']=='Buy' and data['takeProfit']!='None' and data['stopLoss']!='None' and data['trailingStop']!='None':  
        # if there is no order Position at All
        
        data['side'] = 'Sell'
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')
        
        data['side'] = 'Buy'
        # and we have a new Buy Order
        print("Buy  Buy order being executed" )
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = (takeProfitby100*last_price)+last_price
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)

        print('Stop Loss by 100 ----------------------------------------------------------')
        sLoss = float(data['stopLoss'])
        print(sLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        stopLossby100 = sLoss/100
        print(stopLossby100*last_price)
        stoploss = last_price-(stopLossby100*last_price)
        print('Stop Loss Margin----------------------------------------------------------')
        print(stoploss)
        
        print('Trailing Stop by 100 ----------------------------------------------------------')
        tsLoss = float(data['trailingStop'])
        print(tsLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        tstopLossby100 = tsLoss/100
        print(tstopLossby100*last_price)
        tstoploss = tstopLossby100*last_price
        print('Trailing Stop  Margin ----------------------------------------------------------')
        print(tstoploss)
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount+position_value,
        stop_loss=stoploss,time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else 'None'
        print(order_ids)
        
        print('Activating Trailing Stop')
        order_resp = bybit1.place_active_order_ts(symbol=data['symbol'], trailing_stop = tstoploss)
        print(json.dumps(order_resp, indent=2))
        
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        data['type'] = 'Limit'
        data['side'] = 'Sell'
        #We want to Add TP to the Market Order
                #We want to Add TP to the Market Order
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        tprofit = float(data['takeProfit'])
        takeProfitby100 = tprofit/100
        takeprofit = (takeProfitby100*entry_price)+entry_price
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position')
        #,p_r_qty = int(orderamount), p_r_price = int(entry_price)
        #order_resp = bybit1.replace_active_order(order_id = nonebuy, symbol = data['symbol'], 
        #p_r_qty = position_value, p_r_price = int(takeprofit)) 
        
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value, price=int(takeprofit),time_in_force='PostOnly', reduce_only='True')
        
        print(json.dumps(order_resp, indent=2))
        nonebuy = order_resp['result']['order_id'] if order_resp['result'] else None
        

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")


        data['side']='Buy'

    if position_side == 'Sell' and data['side']=='Sell'and data['takeProfit']!='None' and data['stopLoss']!='None' and data['trailingStop']!='None':  
        # if there is no order Position at All
        # and we have a new Sell Order
        data['side'] = 'Buy'
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')
        
        data['side'] = 'Sell'
        print("None Sell order being executed")
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = last_price - (takeProfitby100*last_price)
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)

        print('Stop Loss by 100 ----------------------------------------------------------')
        sLoss = float(data['stopLoss'])
        print(sLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        stopLossby100 = sLoss/100
        print(stopLossby100*last_price)
        stoploss = (stopLossby100*last_price) + last_price
        print('Stop Loss Margin----------------------------------------------------------')
        print(stoploss)
        
        print('Trailing Stop by 100 ----------------------------------------------------------')
        tsLoss = float(data['trailingStop'])
        print(tsLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        tstopLossby100 = tsLoss/100
        print(tstopLossby100*last_price)
        tstoploss = tstopLossby100*last_price
        print('Trailing Stop  Margin ----------------------------------------------------------')
        print(tstoploss)
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount+position_value,
        stop_loss=stoploss,time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        
        print('Activating Trailing Stop')
        order_resp = bybit1.place_active_order_ts(symbol=data['symbol'], trailing_stop = tstoploss)
        print(json.dumps(order_resp, indent=2))
        
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        
        data['type'] = 'Limit'
        data['side'] = 'Buy'
        
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        tprofit = float(data['takeProfit'])
        takeProfitby100 = tprofit/100
        takeprofit = entry_price-(takeProfitby100*entry_price)
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position and ',position_value,'Position Value')
        print('And ', takeprofit,'Take profit Value')
        print('And ', entry_price,'Position Entry price Value')
        
        
        """
        order_resp = bybit1.replace_active_order(order_id = nonesell, symbol = data['symbol'], 
        p_r_qty = position_value, p_r_price = int(takeprofit)) 
        """
        
        """"""
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value, price=int(takeprofit),time_in_force='PostOnly', reduce_only='True')
        print(json.dumps(order_resp, indent=2))
        order_resp = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_resp)

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")

        data['side']='Sell'
        
    if position_side == 'Sell' and data['stopLoss']!='None' and data['trailingStop']!='None': 
        
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')

        # and we have a new Buy Order
        print("Buy  Buy order being executed" )
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = (takeProfitby100*last_price)+last_price
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)

        print('Stop Loss by 100 ----------------------------------------------------------')
        sLoss = float(data['stopLoss'])
        print(sLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        stopLossby100 = sLoss/100
        print(stopLossby100*last_price)
        stoploss = last_price-(stopLossby100*last_price)
        print('Stop Loss Margin----------------------------------------------------------')
        print(stoploss)
        
        print('Trailing Stop by 100 ----------------------------------------------------------')
        tsLoss = float(data['trailingStop'])
        print(tsLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        tstopLossby100 = tsLoss/100
        print(tstopLossby100*last_price)
        tstoploss = tstopLossby100*last_price
        print('Trailing Stop  Margin ----------------------------------------------------------')
        print(tstoploss)
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        stop_loss=stoploss,time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        
        print('Activating Trailing Stop')
        order_resp = bybit1.place_active_order_ts(symbol=data['symbol'], trailing_stop = tstoploss)
        print(json.dumps(order_resp, indent=2))
        
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        data['type'] = 'Limit'
        data['side'] = 'Sell'
        #We want to Add TP to the Market Order
                #We want to Add TP to the Market Order
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        tprofit = float(data['takeProfit'])
        takeProfitby100 = tprofit/100
        takeprofit = (takeProfitby100*entry_price)+entry_price
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position')
        #,p_r_qty = int(orderamount), p_r_price = int(entry_price)
        #order_resp = bybit1.replace_active_order(order_id = nonebuy, symbol = data['symbol'], 
        #p_r_qty = position_value, p_r_price = int(takeprofit)) 
        
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value, price=int(takeprofit),time_in_force='PostOnly', reduce_only='True')
        
        print(json.dumps(order_resp, indent=2))
        nonebuy = order_resp['result']['order_id'] if order_resp['result'] else None
        

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")


        data['side']='Buy'

    if position_side == 'Buy' and data['side']=='Sell'and data['takeProfit']!='None' and data['stopLoss']!='None' and data['trailingStop']!='None':
        
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')

        print('Stop Loss by 100 ----------------------------------------------------------')
        sLoss = float(data['stopLoss'])
        print(sLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        stopLossby100 = sLoss/100
        print(stopLossby100*last_price)
        stoploss = (stopLossby100*last_price) + last_price
        print('Stop Loss Margin----------------------------------------------------------')
        print(stoploss)
        
        print('Trailing Stop by 100 ----------------------------------------------------------')
        tsLoss = float(data['trailingStop'])
        print(tsLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        tstopLossby100 = tsLoss/100
        print(tstopLossby100*last_price)
        tstoploss = tstopLossby100*last_price
        print('Trailing Stop  Margin ----------------------------------------------------------')
        print(tstoploss)
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        stop_loss=stoploss,time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        
        print('Activating Trailing Stop')
        order_resp = bybit1.place_active_order_ts(symbol=data['symbol'], trailing_stop = tstoploss)
        print(json.dumps(order_resp, indent=2))
        
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        
        data['type'] = 'Limit'
        data['side'] = 'Buy'
        
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        tprofit = float(data['takeProfit'])
        takeProfitby100 = tprofit/100
        takeprofit = entry_price-(takeProfitby100*entry_price)
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position and ',position_value,'Position Value')
        print('And ', takeprofit,'Take profit Value')
        print('And ', entry_price,'Position Entry price Value')
        
        
        """
        order_resp = bybit1.replace_active_order(order_id = nonesell, symbol = data['symbol'], 
        p_r_qty = position_value, p_r_price = int(takeprofit)) 
        """
        
        """"""
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value, price=int(takeprofit),time_in_force='PostOnly', reduce_only='True')
        print(json.dumps(order_resp, indent=2))
        order_resp = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_resp)

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")

        data['side']='Sell' 
        
        #-----------------------------------------------------------------------------------------------------------------
        
    if position_side == 'None' and data['side']=='Buy' and data['takeProfit']=='None' and data['stopLoss']!='0'and data['trailingStop']!='None':
        # if there is no order Position at All
        # and we have a new Buy Order
        print("None  Buy order being executed")
        # Since a Buy Position has been Opened, First Thing we set data type to Limit
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = (takeProfitby100*last_price)+last_price
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)

        print('Stop Loss by 100 ----------------------------------------------------------')
        sLoss = float(data['stopLoss'])
        print(sLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        stopLossby100 = sLoss/100
        print(stopLossby100*last_price)
        stoploss = last_price-(stopLossby100*last_price)
        print('Stop Loss Margin----------------------------------------------------------')
        print(stoploss)
        
        print('Trailing Stop by 100 ----------------------------------------------------------')
        tsLoss = float(data['trailingStop'])
        print(tsLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        tstopLossby100 = tsLoss/100
        print(tstopLossby100*last_price)
        tstoploss = tstopLossby100*last_price
        print('Trailing Stop  Margin ----------------------------------------------------------')
        print(tstoploss)

        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        
        print('Activating Trailing Stop')
        order_resp = bybit1.place_active_order_ts(symbol=data['symbol'], trailing_stop = tstoploss)
        print(json.dumps(order_resp, indent=2))
 

        data['type'] = 'Limit'
        data['side'] = 'Sell'
        #We want to Add TP to the Market Order
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = orderamount, time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        nonebuy = order_resp['result']['order_id'] if order_resp['result'] else None
        oldqty = orderamount
        oldprice = takeprofit
        nonebuy = nonebuy
        

        print('Order ID for this Sale', nonebuy)


        """
        order_resp = bybit1.replace_active_order(order_id = nonebuy, symbol = data['symbol'],
        p_r_qty = position_value, p_r_price = takeprofit)
        """

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")

        data['side']='Buy'
        
    if position_side == 'None' and data['stopLoss']!='None' and data['trailingStop']!='None':  
        # if there is no order Position at All
        # and we have a new Sell Order
        print("None   Sell order being executed")
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = last_price - (takeProfitby100*last_price)
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)

        print('Stop Loss by 100 ----------------------------------------------------------')
        sLoss = float(data['stopLoss'])
        print(sLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        stopLossby100 = sLoss/100
        print(stopLossby100*last_price)
        stoploss = (stopLossby100*last_price) + last_price
        print('Stop Loss Margin----------------------------------------------------------')
        print(stoploss)
        
        print('Trailing Stop by 100 ----------------------------------------------------------')
        tsLoss = float(data['trailingStop'])
        print(tsLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        tstopLossby100 = tsLoss/100
        print(tstopLossby100*last_price)
        tstoploss = tstopLossby100*last_price
        print('Trailing Stop  Margin ----------------------------------------------------------')
        print(tstoploss)

        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        time_in_force='PostOnly', reduce_only='False')
        #print(json.dumps(order_resp, indent=2))
        order_idss = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_idss)
        
        print('Activating Trailing Stop')
        order_resp = bybit1.place_active_order_ts(symbol=data['symbol'], trailing_stop = tstoploss)
        print(json.dumps(order_resp, indent=2))


        data['type'] = 'Limit'
        data['side'] = 'Buy'
        #We want to Add TP to the Market Order
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = orderamount, time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        nonesell = order_resp['result']['order_id'] if order_resp['result'] else None
        oldqtysell = orderamount
        oldpricesell = stoploss
        nonesell = nonesell

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")  

        data['side']='Sell'

    if position_side == 'Buy' and data['side']=='Buy' and data['takeProfit']=='None' and data['stopLoss']!='None' and data['trailingStop']!='None':  
        # if there is no order Position at All
        
        data['side'] = 'Sell'
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')
        
        data['side'] = 'Buy'
        # and we have a new Buy Order
        print("Buy  Buy order being executed" )
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = (takeProfitby100*last_price)+last_price
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)

        print('Stop Loss by 100 ----------------------------------------------------------')
        sLoss = float(data['stopLoss'])
        print(sLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        stopLossby100 = sLoss/100
        print(stopLossby100*last_price)
        stoploss = last_price-(stopLossby100*last_price)
        print('Stop Loss Margin----------------------------------------------------------')
        print(stoploss)
        
        print('Trailing Stop by 100 ----------------------------------------------------------')
        tsLoss = float(data['trailingStop'])
        print(tsLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        tstopLossby100 = tsLoss/100
        print(tstopLossby100*last_price)
        tstoploss = tstopLossby100*last_price
        print('Trailing Stop  Margin ----------------------------------------------------------')
        print(tstoploss)
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount+position_value,
        stop_loss=stoploss,time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        
        print('Activating Trailing Stop')
        order_resp = bybit1.place_active_order_ts(symbol=data['symbol'], trailing_stop = tstoploss)
        print(json.dumps(order_resp, indent=2))
        
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        data['type'] = 'Limit'
        data['side'] = 'Sell'
        #We want to Add TP to the Market Order
                #We want to Add TP to the Market Order
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        tprofit = float(data['takeProfit'])
        takeProfitby100 = tprofit/100
        takeprofit = (takeProfitby100*entry_price)+entry_price
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position')
        #,p_r_qty = int(orderamount), p_r_price = int(entry_price)
        #order_resp = bybit1.replace_active_order(order_id = nonebuy, symbol = data['symbol'], 
        #p_r_qty = position_value, p_r_price = int(takeprofit)) 
        
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value,time_in_force='PostOnly', reduce_only='False')
        
        print(json.dumps(order_resp, indent=2))
        nonebuy = order_resp['result']['order_id'] if order_resp['result'] else None

        data['side']='Buy'

    if position_side == 'Sell' and data['side']=='Sell'and data['takeProfit']=='None' and data['stopLoss']!='None' and data['trailingStop']!='None':  # if there is no order Position at All
        # and we have a new Sell Order
        data['side'] = 'Buy'
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')
        
        data['side'] = 'Sell'
        print("None Sell order being executed")
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = last_price - (takeProfitby100*last_price)
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)

        print('Stop Loss by 100 ----------------------------------------------------------')
        sLoss = float(data['stopLoss'])
        print(sLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        stopLossby100 = sLoss/100
        print(stopLossby100*last_price)
        stoploss = (stopLossby100*last_price) + last_price
        print('Stop Loss Margin----------------------------------------------------------')
        print(stoploss)
        
        print('Trailing Stop by 100 ----------------------------------------------------------')
        tsLoss = float(data['trailingStop'])
        print(tsLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        tstopLossby100 = tsLoss/100
        print(tstopLossby100*last_price)
        tstoploss = tstopLossby100*last_price
        print('Trailing Stop  Margin ----------------------------------------------------------')
        print(tstoploss)
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount+position_value,
        stop_loss=stoploss,time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        
        print('Activating Trailing Stop')
        order_resp = bybit1.place_active_order_ts(symbol=data['symbol'], trailing_stop = tstoploss)
        print(json.dumps(order_resp, indent=2))
        
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        
        data['type'] = 'Limit'
        data['side'] = 'Buy'
        
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        tprofit = float(data['takeProfit'])
        takeProfitby100 = tprofit/100
        takeprofit = entry_price-(takeProfitby100*entry_price)
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position and ',position_value,'Position Value')
        print('And ', takeprofit,'Take profit Value')
        print('And ', entry_price,'Position Entry price Value')
        
        
        """
        order_resp = bybit1.replace_active_order(order_id = nonesell, symbol = data['symbol'], 
        p_r_qty = position_value, p_r_price = int(takeprofit)) 
        """
        
        """"""
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value,time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_resp = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_resp)

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")

        data['side']='Sell'
        
    if position_side == 'Sell' and data['side']=='Buy'and data['takeProfit']=='None' and data['stopLoss']!='None' and data['trailingStop']!='None': 
        
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')

        # and we have a new Buy Order
        print("Buy  Buy order being executed" )
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = (takeProfitby100*last_price)+last_price
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)

        print('Stop Loss by 100 ----------------------------------------------------------')
        sLoss = float(data['stopLoss'])
        print(sLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        stopLossby100 = sLoss/100
        print(stopLossby100*last_price)
        stoploss = last_price-(stopLossby100*last_price)
        print('Stop Loss Margin----------------------------------------------------------')
        print(stoploss)
        
        print('Trailing Stop by 100 ----------------------------------------------------------')
        tsLoss = float(data['trailingStop'])
        print(tsLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        tstopLossby100 = tsLoss/100
        print(tstopLossby100*last_price)
        tstoploss = tstopLossby100*last_price
        print('Trailing Stop  Margin ----------------------------------------------------------')
        print(tstoploss)
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        stop_loss=stoploss,time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        
        print('Activating Trailing Stop')
        order_resp = bybit1.place_active_order_ts(symbol=data['symbol'], trailing_stop = tstoploss)
        print(json.dumps(order_resp, indent=2))
        
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        data['type'] = 'Limit'
        data['side'] = 'Sell'
        #We want to Add TP to the Market Order
                #We want to Add TP to the Market Order
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        tprofit = float(data['takeProfit'])
        takeProfitby100 = tprofit/100
        takeprofit = (takeProfitby100*entry_price)+entry_price
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position')
        #,p_r_qty = int(orderamount), p_r_price = int(entry_price)
        #order_resp = bybit1.replace_active_order(order_id = nonebuy, symbol = data['symbol'], 
        #p_r_qty = position_value, p_r_price = int(takeprofit)) 
        
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value,time_in_force='PostOnly', reduce_only='False')
        
        print(json.dumps(order_resp, indent=2))
        nonebuy = order_resp['result']['order_id'] if order_resp['result'] else None
        

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")


        data['side']='Buy'

    if position_side == 'Buy' and data['side']=='Sell'and data['takeProfit']=='None' and data['stopLoss']!='None' and data['trailingStop']!='None':
        
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')
        
        data['side'] = 'Sell'
        print("None Sell order being executed")
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = last_price - (takeProfitby100*last_price)
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)

        print('Stop Loss by 100 ----------------------------------------------------------')
        sLoss = float(data['stopLoss'])
        print(sLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        stopLossby100 = sLoss/100
        print(stopLossby100*last_price)
        stoploss = (stopLossby100*last_price) + last_price
        print('Stop Loss Margin----------------------------------------------------------')
        print(stoploss)
        
        print('Trailing Stop by 100 ----------------------------------------------------------')
        tsLoss = float(data['trailingStop'])
        print(tsLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        tstopLossby100 = tsLoss/100
        print(tstopLossby100*last_price)
        tstoploss = tstopLossby100*last_price
        print('Trailing Stop  Margin ----------------------------------------------------------')
        print(tstoploss)
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        stop_loss=stoploss,time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        
        print('Activating Trailing Stop')
        order_resp = bybit1.place_active_order_ts(symbol=data['symbol'], trailing_stop = tstoploss)
        print(json.dumps(order_resp, indent=2))
        
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        
        data['type'] = 'Limit'
        data['side'] = 'Buy'
        
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        tprofit = float(data['takeProfit'])
        takeProfitby100 = tprofit/100
        takeprofit = entry_price-(takeProfitby100*entry_price)
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position and ',position_value,'Position Value')
        print('And ', takeprofit,'Take profit Value')
        print('And ', entry_price,'Position Entry price Value')
        
        
        """
        order_resp = bybit1.replace_active_order(order_id = nonesell, symbol = data['symbol'], 
        p_r_qty = position_value, p_r_price = int(takeprofit)) 
        """
        
        """"""
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value, time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_resp = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_resp)

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")

        data['side']='Sell' 
        
        #-----------------------------------------------------------------------------------------------------------

    if position_side == 'None' and data['side']=='Buy' and data['takeProfit']!='None' and data['stopLoss']=='None' and data['trailingStop']!='None':
        # if there is no order Position at All
        # and we have a new Buy Order
        print("None  Buy order being executed")
        # Since a Buy Position has been Opened, First Thing we set data type to Limit
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = (takeProfitby100*last_price)+last_price
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)

        
        print('Trailing Stop by 100 ----------------------------------------------------------')
        tsLoss = float(data['trailingStop'])
        print(tsLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        tstopLossby100 = tsLoss/100
        print(tstopLossby100*last_price)
        tstoploss = tstopLossby100*last_price
        print('Trailing Stop  Margin ----------------------------------------------------------')
        print(tstoploss)

        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        
        print('Activating Trailing Stop')
        order_resp = bybit1.place_active_order_ts(symbol=data['symbol'], trailing_stop = tstoploss)
        print(json.dumps(order_resp, indent=2))
 
        bybit1.cancel_all_active_orders(symbol=data['symbol'])    
    
        data['type'] = 'Limit'
        data['side'] = 'Sell'
        #We want to Add TP to the Market Order
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = orderamount, price=takeprofit,time_in_force='PostOnly', reduce_only='True')
        print(json.dumps(order_resp, indent=2))
        nonebuy = order_resp['result']['order_id'] if order_resp['result'] else None
        oldqty = orderamount
        oldprice = takeprofit
        nonebuy = nonebuy
        

        print('Order ID for this Sale', nonebuy)


        """
        order_resp = bybit1.replace_active_order(order_id = nonebuy, symbol = data['symbol'],
        p_r_qty = position_value, p_r_price = takeprofit)
        """

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")

        data['side']='Buy'
        
    if position_side == 'None' and data['side']=='Sell' and data['takeProfit']!='None' and data['stopLoss']=='None' and data['trailingStop']!='None':  
        # if there is no order Position at All
        # and we have a new Sell Order
        print("None   Sell order being executed")
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = last_price - (takeProfitby100*last_price)
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)
        
        print('Trailing Stop by 100 ----------------------------------------------------------')
        tsLoss = float(data['trailingStop'])
        print(tsLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        tstopLossby100 = tsLoss/100
        print(tstopLossby100*last_price)
        tstoploss = tstopLossby100*last_price
        print('Trailing Stop  Margin ----------------------------------------------------------')
        print(tstoploss)

        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        time_in_force='PostOnly', reduce_only='False')
        #print(json.dumps(order_resp, indent=2))
        order_idss = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_idss)
        
        print('Activating Trailing Stop')
        order_resp = bybit1.place_active_order_ts(symbol=data['symbol'], trailing_stop = tstoploss)
        print(json.dumps(order_resp, indent=2))
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])

        data['type'] = 'Limit'
        data['side'] = 'Buy'
        #We want to Add TP to the Market Order
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = orderamount, price=takeprofit,time_in_force='PostOnly', reduce_only='True')
        print(json.dumps(order_resp, indent=2))
        nonesell = order_resp['result']['order_id'] if order_resp['result'] else None
        oldqtysell = orderamount
        oldpricesell = stoploss
        nonesell = nonesell

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")  

        data['side']='Sell'

    if position_side == 'Buy' and data['side']=='Buy' and data['takeProfit']!='None' and data['stopLoss']=='None' and data['trailingStop']!='None': 
        # if there is no order Position at All
        
        data['side'] = 'Sell'
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')
        
        data['side'] = 'Buy'
        # and we have a new Buy Order
        print("Buy  Buy order being executed" )
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = (takeProfitby100*last_price)+last_price
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)
        
        print('Trailing Stop by 100 ----------------------------------------------------------')
        tsLoss = float(data['trailingStop'])
        print(tsLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        tstopLossby100 = tsLoss/100
        print(tstopLossby100*last_price)
        tstoploss = tstopLossby100*last_price
        print('Stop Loss Margin----------------------------------------------------------')
        
        print('Activating Trailing Stop')
        order_resp = bybit1.place_active_order_ts(symbol=data['symbol'], trailing_stop = tstoploss)
        print(json.dumps(order_resp, indent=2))
        
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        data['type'] = 'Limit'
        data['side'] = 'Sell'
        #We want to Add TP to the Market Order
                #We want to Add TP to the Market Order
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        tprofit = float(data['takeProfit'])
        takeProfitby100 = tprofit/100
        takeprofit = (takeProfitby100*entry_price)+entry_price
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position')
        #,p_r_qty = int(orderamount), p_r_price = int(entry_price)
        #order_resp = bybit1.replace_active_order(order_id = nonebuy, symbol = data['symbol'], 
        #p_r_qty = position_value, p_r_price = int(takeprofit)) 

        #order_rep = bybit1.replace_active_order(order_id = real_time_active_order_result['order_id'], symbol=data['symbol'],
        #                     p_r_qty=orderamount+position_value, p_r_price=int(takeprofit))
        
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
                     qty = position_value, price=int(takeprofit),time_in_force='PostOnly', reduce_only='True')
        
        print(json.dumps(order_resp, indent=2))
        nonebuy = order_resp['result']['order_id'] if order_resp['result'] else None
        

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")


        data['side']='Buy'

    if position_side == 'Sell' and data['side']=='Sell'and data['takeProfit']!='None' and data['stopLoss']=='None' and data['trailingStop']!='None': 
        # if there is no order Position at All
        # and we have a new Sell Order
        data['side'] = 'Buy'
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')
        
        data['side'] = 'Sell'
        print("None Sell order being executed")
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = last_price - (takeProfitby100*last_price)
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)
        
        print('Trailing Stop by 100 ----------------------------------------------------------')
        tsLoss = float(data['trailingStop'])
        print(tsLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        tstopLossby100 = tsLoss/100
        print(tstopLossby100*last_price)
        tstoploss = tstopLossby100*last_price
        print('Trailing Stop  Margin ----------------------------------------------------------')
        print(tstoploss)
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount+position_value,
        time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        
        print('Activating Trailing Stop')
        order_resp = bybit1.place_active_order_ts(symbol=data['symbol'], trailing_stop = tstoploss)
        print(json.dumps(order_resp, indent=2))
        
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        
        data['type'] = 'Limit'
        data['side'] = 'Buy'
        
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        tprofit = float(data['takeProfit'])
        takeProfitby100 = tprofit/100
        takeprofit = entry_price-(takeProfitby100*entry_price)
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position and ',position_value,'Position Value')
        print('And ', takeprofit,'Take profit Value')
        print('And ', entry_price,'Position Entry price Value')
        
        
        """
        order_resp = bybit1.replace_active_order(order_id = nonesell, symbol = data['symbol'], 
        p_r_qty = position_value, p_r_price = int(takeprofit)) 
        """
        
        """"""
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value, price=int(takeprofit),time_in_force='PostOnly', reduce_only='True')
        print(json.dumps(order_resp, indent=2))
        order_resp = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_resp)

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")

        data['side']='Sell'
        
    if position_side == 'Sell' and data['side']=='Buy'and data['takeProfit']!='None' and data['stopLoss']=='None' and data['trailingStop']!='None': 
        
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        
        print('Activating Trailing Stop')
        order_resp = bybit1.place_active_order_ts(symbol=data['symbol'], trailing_stop = tstoploss)
        print(json.dumps(order_resp, indent=2))
        
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        data['type'] = 'Limit'
        data['side'] = 'Sell'
        #We want to Add TP to the Market Order
                #We want to Add TP to the Market Order
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        tprofit = float(data['takeProfit'])
        takeProfitby100 = tprofit/100
        takeprofit = (takeProfitby100*entry_price)+entry_price
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position')
        #,p_r_qty = int(orderamount), p_r_price = int(entry_price)
        #order_resp = bybit1.replace_active_order(order_id = nonebuy, symbol = data['symbol'], 
        #p_r_qty = position_value, p_r_price = int(takeprofit)) 
        
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value, price=int(takeprofit),time_in_force='PostOnly', reduce_only='True')
        
        print(json.dumps(order_resp, indent=2))
        nonebuy = order_resp['result']['order_id'] if order_resp['result'] else None
        

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")


        data['side']='Buy'

    if position_side == 'Buy' and data['side']=='Sell'and data['takeProfit']!='None' and data['stopLoss']=='None' and data['trailingStop']!='None':
        
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')
        
        data['side'] = 'Sell'
        print("None Sell order being executed")
        print('Take Profit by 100 ----------------------------------------------------------')
        tprofit = float(data['takeProfit'])
        print(tprofit/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        takeProfitby100 = tprofit/100
        print(takeProfitby100*last_price)
        takeprofit = last_price - (takeProfitby100*last_price)
        print('Take Profit Margin----------------------------------------------------------')
        print(takeprofit)
        
        print('Trailing Stop by 100 ----------------------------------------------------------')
        tsLoss = float(data['trailingStop'])
        print(tsLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        tstopLossby100 = tsLoss/100
        print(tstopLossby100*last_price)
        tstoploss = tstopLossby100*last_price
        print('Trailing Stop  Margin ----------------------------------------------------------')
        print(tstoploss)
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        
        print('Activating Trailing Stop')
        order_resp = bybit1.place_active_order_ts(symbol=data['symbol'], trailing_stop = tstoploss)
        print(json.dumps(order_resp, indent=2))
        
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        data['type'] = 'Limit'
        data['side'] = 'Buy'
        
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        tprofit = float(data['takeProfit'])
        takeProfitby100 = tprofit/100
        takeprofit = entry_price-(takeProfitby100*entry_price)
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position and ',position_value,'Position Value')
        print('And ', takeprofit,'Take profit Value')
        print('And ', entry_price,'Position Entry price Value')
        
        
        """
        order_resp = bybit1.replace_active_order(order_id = nonesell, symbol = data['symbol'], 
        p_r_qty = position_value, p_r_price = int(takeprofit)) 
        """
        
        """"""
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value, price=int(takeprofit),time_in_force='PostOnly', reduce_only='True')
        print(json.dumps(order_resp, indent=2))
        order_resp = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_resp)

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")

        data['side']='Sell' 
        
        #---------------------------------------------------------------------------------------------------------------
        
    if position_side == 'None' and data['side']=='Buy' and data['takeProfit']=='None' and data['stopLoss']=='None' and data['trailingStop']!='None':
        

        print('Trailing Stop by 100 ----------------------------------------------------------')
        tsLoss = float(data['trailingStop'])
        print(tsLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        tstopLossby100 = tsLoss/100
        print(tstopLossby100*last_price)
        tstoploss = tstopLossby100*last_price
        print('Stop Loss Margin----------------------------------------------------------')
        print(tstoploss)
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        
        print('Activating Trailing Stop')
        order_resp = bybit1.place_active_order_ts(symbol=data['symbol'], trailing_stop = tstoploss)
        print(json.dumps(order_resp, indent=2))
        

        data['type'] = 'Limit'
        data['side'] = 'Sell'
        #We want to Add TP to the Market Order
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = orderamount, time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        nonebuy = order_resp['result']['order_id'] if order_resp['result'] else None
        oldqty = orderamount
        nonebuy = nonebuy
        

        print('Order ID for this Sale', nonebuy)

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")

        data['side']='Buy'
        
    if position_side == 'None' and data['side']=='Sell' and data['takeProfit']=='None' and data['stopLoss']=='None' and data['trailingStop']=='None':  
      

        print('Trailing Stop by 100 ----------------------------------------------------------')
        tsLoss = float(data['trailingStop'])
        print(tsLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        tstopLossby100 = tsLoss/100
        print(tstopLossby100*last_price)
        tstoploss = tstopLossby100*last_price
        print('Trailing Stop  Margin ----------------------------------------------------------')
        print(tstoploss)
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        time_in_force='PostOnly', reduce_only='False')
        #print(json.dumps(order_resp, indent=2))
        order_idss = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_idss)
        
        print('Activating Trailing Stop')
        order_resp = bybit1.place_active_order_ts(symbol=data['symbol'], trailing_stop = tstoploss)
        print(json.dumps(order_resp, indent=2))


        data['type'] = 'Limit'
        data['side'] = 'Buy'
        #We want to Add TP to the Market Order
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = orderamount, time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        nonesell = order_resp['result']['order_id'] if order_resp['result'] else None
        oldqtysell = orderamount
        nonesell = nonesell

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")  

        data['side']='Sell'

    if position_side == 'Buy' and data['side']=='Buy' and data['takeProfit']=='None' and data['stopLoss']=='None' and data['trailingStop']!='None':  
        # if there is no order Position at All
        
        data['side'] = 'Sell'
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')
        
        data['side'] = 'Buy'
        # and we have a new Buy Order
        
        print('Trailing Stop by 100 ----------------------------------------------------------')
        tsLoss = float(data['trailingStop'])
        print(tsLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        tstopLossby100 = tsLoss/100
        print(tstopLossby100*last_price)
        tstoploss = tstopLossby100*last_price
        print('Trailing Stop  Margin ----------------------------------------------------------')
        print(tstoploss)
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount+position_value,
        time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        
        print('Activating Trailing Stop')
        order_resp = bybit1.place_active_order_ts(symbol=data['symbol'], trailing_stop = tstoploss)
        print(json.dumps(order_resp, indent=2))
        
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        data['type'] = 'Limit'
        data['side'] = 'Sell'
        #We want to Add TP to the Market Order
                #We want to Add TP to the Market Order
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position')
        #,p_r_qty = int(orderamount), p_r_price = int(entry_price)
        #order_resp = bybit1.replace_active_order(order_id = nonebuy, symbol = data['symbol'], 
        #p_r_qty = position_value, p_r_price = int(takeprofit)) 
        
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value,time_in_force='PostOnly', reduce_only='False')
        
        print(json.dumps(order_resp, indent=2))
        nonebuy = order_resp['result']['order_id'] if order_resp['result'] else None
        

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")


        data['side']='Buy'

    if position_side == 'Sell' and data['side']=='Sell'and data['takeProfit']=='None' and data['stopLoss']=='None' and data['trailingStop']!='None':  
        # if there is no order Position at All
        # and we have a new Sell Order
        data['side'] = 'Buy'
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')
        
        data['side'] = 'Sell'
        
        print('Trailing Stop by 100 ----------------------------------------------------------')
        tsLoss = float(data['trailingStop'])
        print(tsLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        tstopLossby100 = tsLoss/100
        print(tstopLossby100*last_price)
        tstoploss = tstopLossby100*last_price
        print('Trailing Stop  Margin ----------------------------------------------------------')
        print(tstoploss)
        
        data['type'] = 'Limit'
        data['side'] = 'Buy'
        
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position and ',position_value,'Position Value')
        print('And ', entry_price,'Position Entry price Value')
        
        
        """
        order_resp = bybit1.replace_active_order(order_id = nonesell, symbol = data['symbol'], 
        p_r_qty = position_value, p_r_price = int(takeprofit)) 
        """
        
        """"""
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value, time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_resp = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_resp)

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")

        data['side']='Sell'
        
    if position_side == 'Sell' and data['side']=='Buy'and data['takeProfit']=='None' and data['stopLoss']=='None' and data['trailingStop']!='None': 
        
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')

        
        print('Trailing Stop by 100 ----------------------------------------------------------')
        tsLoss = float(data['trailingStop'])
        print(tsLoss/100)
        print('Multiply By Entry Price ----------------------------------------------------------')
        tstopLossby100 = tsLoss/100
        print(tstopLossby100*last_price)
        tstoploss = tstopLossby100*last_price
        print('Trailing Stop  Margin ----------------------------------------------------------')
        print(tstoploss)
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        
        print('Activating Trailing Stop')
        order_resp = bybit1.place_active_order_ts(symbol=data['symbol'], trailing_stop = tstoploss)
        print(json.dumps(order_resp, indent=2))
        
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        data['type'] = 'Limit'
        data['side'] = 'Sell'
        #We want to Add TP to the Market Order
                #We want to Add TP to the Market Order
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position')
        #,p_r_qty = int(orderamount), p_r_price = int(entry_price)
        #order_resp = bybit1.replace_active_order(order_id = nonebuy, symbol = data['symbol'], 
        #p_r_qty = position_value, p_r_price = int(takeprofit)) 
        
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value, time_in_force='PostOnly', reduce_only='False')
        
        print(json.dumps(order_resp, indent=2))
        nonebuy = order_resp['result']['order_id'] if order_resp['result'] else None
        

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")


        data['side']='Buy'

    if position_side == 'Buy' and data['trailingStop']!='None':
        
        position_value = position_result[0]['size']
        position_valueS = position_value*entry_price
        print('position Value in USD', position_valueS)
        bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=position_value,time_in_force='PostOnly', reduce_only='False')
        
        data['side'] = 'Sell'
        
        
        print('Sending Order in ', data['side'],'position')
        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'], qty=orderamount,
        time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_ids = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_ids)
        
        print('Activating Trailing Stop')
        order_resp = bybit1.place_active_order_ts(symbol=data['symbol'], trailing_stop = tstoploss)
        print(json.dumps(order_resp, indent=2))
        
        pos_take_profit = position_result[0]['take_profit']
        
        bybit1.cancel_all_active_orders(symbol=data['symbol'])
        
        data['type'] = 'Limit'
        data['side'] = 'Buy'
        
        position = bybit1.get_position_http()
        position_result  = position['result']
        entry_price = position_result[0]['entry_price']
        position_value = position_result[0]['size']
        print('Sending Order in ', data['side'],'position and ',position_value,'Position Value')
        print('And ', entry_price,'Position Entry price Value')

        order_resp = bybit1.place_active_order(side=data['side'], order_type=data['type'],
        qty = position_value,time_in_force='PostOnly', reduce_only='False')
        print(json.dumps(order_resp, indent=2))
        order_resp = order_resp['result']['order_id'] if order_resp['result'] else None
        print(order_resp)

        leverage = bybit1.get_leverage()
        print('Leverage ----------------------------------------------------------')
        print(leverage)
        print("Change Leverage")
        save_leverage = bybit1.change_leverage(data['symbol'], data['leverage'])
        print(save_leverage)
        print("Leverage Saved")

        data['side']='Sell'
        
    else: #If Order Side is the same.  I mean Order in SAME Direction

        print('End of WebHook Execution')
    
