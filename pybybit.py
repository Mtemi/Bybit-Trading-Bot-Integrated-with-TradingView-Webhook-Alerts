import hashlib
import hmac
import json
import time
import urllib.parse
from threading import Thread
from collections import deque

from requests import Request, Session
from requests.exceptions import HTTPError
from websocket import WebSocketApp
import pandas as pd

test = 'test'
class Bybit():
    url_main = 'https://api.bybit.com'
    url_test = 'https://api-testnet.bybit.com'
    ws_url_main = 'wss://stream.bybit.com/realtime'
    ws_url_test = 'wss://stream-testnet.bybit.com/realtime'
    headers = {'Content-Type': 'application/json'}

    def __init__(self, api_key, secret, symbol, ws=True, test=False):
        self.api_key = api_key
        self.secret = secret

        self.symbol = symbol
        self.s = Session()
        self.s.headers.update(self.headers)

        self.url = self.url_main if not test else self.url_test
        self.ws_url = self.ws_url_main if not test else self.ws_url_test

        self.ws = ws
        if ws:
            self._connect()

    #
    # WebSocket
    #

    def _connect(self):
        self.ws = WebSocketApp(url=self.ws_url,
                               on_open=self._on_open,
                               on_message=self._on_message)

        self.ws_data = {'trade.' + str(self.symbol): deque(maxlen=200), 
                        'instrument.' + str(self.symbol): {}, 
                        'order_book_25L1.' + str(self.symbol): pd.DataFrame(), 
                        'position': {}, 
                        'execution': deque(maxlen=200), 
                        'order': deque(maxlen=200)
                        }

        positions = self.get_position_http()['result']
       
        if positions is None:
            pass
        else:
            for p in positions:
                if p['data']['symbol'] == self.symbol:
                    self.ws_data['position'].update(p['data'])
                    break

        Thread(target=self.ws.run_forever, daemon=True).start()

    def _on_open(self):
        timestamp = int(time.time() * 1000)
        param_str = 'GET/realtime' + str(timestamp)
        sign = hmac.new(self.secret.encode('utf-8'),
                        param_str.encode('utf-8'), hashlib.sha256).hexdigest()

        self.ws.send(json.dumps(
            {'op': 'auth', 'args': [self.api_key, timestamp, sign]}))
        self.ws.send(json.dumps(
            {'op': 'subscribe', 'args': ['trade.' + str(self.symbol),
                                         'instrument.' + str(self.symbol),
                                         'order_book_25L1.' + str(self.symbol),
                                         'position',
                                         'execution',
                                         'order']}))

    def _on_message(self, message):
        message = json.loads(message)
        topic = message.get('topic')
        if topic == 'order_book_25L1.' + str(self.symbol):
            if message['type'] == 'snapshot':
                self.ws_data[topic] = pd.io.json.json_normalize(message['data']).set_index('id').sort_index(ascending=False)
            else: # message['type'] == 'delta'
                # delete or update or insert
                if len(message['data']['delete']) != 0:
                    drop_list = [x['id'] for x in message['data']['delete']]
                    self.ws_data[topic].drop(index=drop_list)
                elif len(message['data']['update']) != 0:
                    update_list = pd.io.json.json_normalize(message['data']['update']).set_index('id')
                    self.ws_data[topic].update(update_list)
                    self.ws_data[topic] = self.ws_data[topic].sort_index(ascending=False)
                elif len(message['data']['insert']) != 0:
                    insert_list = pd.io.json.json_normalize(message['data']['insert']).set_index('id')
                    self.ws_data[topic].update(insert_list)
                    self.ws_data[topic] = self.ws_data[topic].sort_index(ascending=False)

        elif topic in ['trade.' + str(self.symbol), 'execution', 'order']:
            self.ws_data[topic].append(message['data'][0])

        elif topic in ['instrument.' + str(self.symbol), 'position']:
            self.ws_data[topic].update(message['data'][0])

    def get_trade(self):
        if not self.ws: return None
        
        return self.ws_data['trade.' + str(self.symbol)]

    def get_instrument(self):
        if not self.ws: return None
        while len(self.ws_data['instrument.' + str(self.symbol)]) != 4:
            time.sleep(1.0)
        
        return self.ws_data['instrument.' + str(self.symbol)]

    def get_orderbook(self, side=None):
        if not self.ws: return None
        while self.ws_data['order_book_25L1.' + str(self.symbol)].empty:
            time.sleep(1.0)

        if side == 'Sell':
            orderbook = self.ws_data['order_book_25L1.' + str(self.symbol)].query('side.str.contains("Sell")', engine='python')
        elif side == 'Buy':
            orderbook = self.ws_data['order_book_25L1.' + str(self.symbol)].query('side.str.contains("Buy")', engine='python')
        else:
            orderbook = self.ws_data['order_book_25L1.' + str(self.symbol)]
        return orderbook

    def get_position(self):
        if not self.ws: return None
        
        return self.ws_data['position']

    def get_my_executions(self):

        if not self.ws: return None
        
        return self.ws_data['execution']

    def get_order(self):

        if not self.ws: return None
        
        return self.ws_data['order']

    #
    # Http Apis
    #

    def _request(self, method, path, payload):
        payload['api_key'] = self.api_key
        payload['timestamp'] = int(time.time() * 1000)
        payload = dict(sorted(payload.items()))
        for k, v in list(payload.items()):
            if v is None:
                del payload[k]

        param_str = urllib.parse.urlencode(payload)
        sign = hmac.new(self.secret.encode('utf-8'),
                        param_str.encode('utf-8'), hashlib.sha256).hexdigest()
        payload['sign'] = sign
        
        #print('SIGNED PAYLOAD SIGNED PAYLOAD SIGNED PAYLOAD SIGNED PAYLOAD SIGNED PAYLOAD SIGNED PAYLOAD SIGNED PAYLOAD SIGNED  PAYLOAD ')
        #print(payload)

        if method == 'GET':
            query = payload
            body = None
        else:
            query = None
            body = json.dumps(payload)

        req = Request(method, self.url + path, data=body, params=query)
        prepped = self.s.prepare_request(req)

        resp = None
        try:
            resp = self.s.send(prepped)
            resp.raise_for_status()
        except HTTPError as e:
            print(e)

        try:
            return resp.json()
        except json.decoder.JSONDecodeError as e:
            print('json.decoder.JSONDecodeError: ' + str(e))
            return resp.text

    def place_active_order(self, side=None, symbol=None, order_type=None,
        qty=None, price=None,
        time_in_force='GoodTillCancel', take_profit=None,
        stop_loss=None, reduce_only=None, order_link_id=None):

        payload = {
        'side': side,
        'symbol': symbol if symbol else self.symbol,
        'order_type': order_type,
        'qty': qty,
        'price': price,
        'time_in_force': time_in_force,
        'take_profit': take_profit,
        'stop_loss': stop_loss,
        'order_link_id': order_link_id
        }
        #/open-api/order/create

        print("skfk", payload)
        return self._request('POST', '/v2/private/order/create', payload=payload)

    def place_active_order_v2(self, data):

        # example of payload
        # payload = {
        # 'side': side,
        # 'symbol': symbol if symbol else self.symbol,
        # 'order_type': order_type,
        # 'qty': qty,
        # 'price': price,
        # 'time_in_force': time_in_force,
        # 'take_profit': take_profit,
        # 'stop_loss': stop_loss,
        # 'order_link_id': order_link_id
        # }

        #/open-api/order/create
       
        return self._request('POST', '/v2/private/order/create', payload=data)
        
    def place_active_order_ts_v2(self,payload):
        # example of payload
        # payload = {
        #     'symbol': symbol if symbol else self.symbol,
        #     'take_profit': take_profit,
        #     'stop_loss': stop_loss,
        #     'trailing_stop': trailing_stop,
        #     'new_trailing_active': new_trailing_active
        # }
        #/open-api/position/trading-stop
        return self._request('POST', '/v2/private/position/trading-stop', payload=payload)


    def place_active_order_ts(self, symbol=None, take_profit=None,
                           stop_loss=None, trailing_stop=None, new_trailing_active=None):

        payload = {
            'symbol': symbol if symbol else self.symbol,
            'take_profit': take_profit,
            'stop_loss': stop_loss,
            'trailing_stop': trailing_stop,
            'new_trailing_active': new_trailing_active
        }
        #/open-api/position/trading-stop
        return self._request('POST', '/v2/private/position/trading-stop', payload=payload)
        
    def get_active_order(self, order_id=None, order_link_id=None, symbol=None,
                         sort=None, order=None, page=None, limit=None,
                         order_status=None):

        payload = {
            'order_id': order_id,
            'order_link_id': order_link_id,
            'symbol': symbol if symbol else self.symbol,
            'sort': sort,
            'order': order,
            'page': page,
            'limit': limit,
            'order_status': order_status
        }
        return self._request('GET', '/open-api/order/list', payload=payload)
    """
    def cancel_active_order(self, order_id=None):

        payload = {
            'order_id': order_id
        }
        return self._request('POST', '/open-api/order/cancel', payload=payload)
    """
    def place_conditional_order(self, side=None, symbol=None, order_type=None,
                                qty=None, price=None, base_price=None,
                                stop_px=None, time_in_force='GoodTillCancel',
                                close_on_trigger=None, reduce_only=None,
                                order_link_id=None):

        payload = {
            'side': side,
            'symbol': symbol if symbol else self.symbol,
            'order_type': order_type,
            'qty': qty,
            'price': price,
            'base_price': base_price,
            'stop_px': stop_px,
            'time_in_force': time_in_force,
            'close_on_trigger': close_on_trigger,
            'reduce_only': reduce_only,
            'order_link_id': order_link_id
        }
        return self._request('POST', '/open-api/stop-order/create', payload=payload)

    def get_conditional_order(self, stop_order_id=None, order_link_id=None,
                              symbol=None, sort=None, order=None, page=None,
                              limit=None):

        payload = {
            'stop_order_id': stop_order_id,
            'order_link_id': order_link_id,
            'symbol': symbol if symbol else self.symbol,
            'sort': sort,
            'order': order,
            'page': page,
            'limit': limit
        }
        return self._request('GET', '/open-api/stop-order/list', payload=payload)

    def cancel_conditional_order(self, order_id=None):

        payload = {
            'order_id': order_id
        }
        return self._request('POST', '/open-api/stop-order/cancel', payload=payload)

    def get_leverage(self):

        payload = {}
        return self._request('GET', '/user/leverage', payload=payload)

    def get_time_stamp(self):

        payload = {}
        return self._request('GET', '/v2/public/time', payload=payload)

    def change_leverage(self, symbol=None, leverage=None):

        payload = {
            'symbol': symbol if symbol else self.symbol,
            'leverage': leverage
        }
        return self._request('POST', '/user/leverage/save', payload=payload)

    def get_position_http(self):

        payload = {}
        return self._request('GET', '/v2/private/position/list', payload=payload)

    def get_position_list(self, symbol=None):

        payload = {
            'symbol': symbol if symbol else self.symbol
        }
        return self._request('GET', '/v2/private/position/list', payload=payload)


    def change_position_margin(self, symbol=None, margin=None):

        payload = {
            'symbol': symbol if symbol else self.symbol,
            'margin': margin
        }
        return self._request('POST', '/position/change-position-margin', payload=payload)

    def get_prev_funding_rate(self, symbol=None):

        payload = {
            'symbol': symbol if symbol else self.symbol,
        }
        return self._request('GET', '/open-api/funding/prev-funding-rate', payload=payload)

    def get_prev_funding(self, symbol=None):

        payload = {
            'symbol': symbol if symbol else self.symbol,
        }
        return self._request('GET', '/open-api/funding/prev-funding', payload=payload)

    def get_predicted_funding(self, symbol=None):

        payload = {
            'symbol': symbol if symbol else self.symbol,
        }
        return self._request('GET', '/open-api/funding/predicted-funding', payload=payload)

    def get_my_execution(self, order_id=None):

        payload = {
            'order_id': order_id
        }
        return self._request('GET', '/v2/private/execution/list', payload=payload)

    #
    # New Http Apis (developing)
    #

    def symbols(self):

        payload = {}
        return self._request('GET', '/v2/public/symbols', payload=payload)

    def kline(self, symbol=None, interval=None, _from=None, limit=None):

        payload = {
            'symbol': symbol if symbol else self.symbol,
            'interval': interval,
            'from': _from,
            'limit': limit
        }
        return self._request('GET', '/v2/public/kline/list', payload=payload)

    """
    def cancel_active_order_v2(self, order_id=None):

        payload = {
            'order_id': order_id
        }
        return self._request('POST', '/v2/private/order/cancel', payload=payload)
    """
    def cancel_active_order(self, symbol=None, order_id=None):

        payload = {
            'symbol': symbol if symbol else self.symbol, 
            'order_id': order_id
        }
        return self._request('POST', '/v2/private/order/cancel', payload=payload)


    def cancel_all_active_orders(self, symbol=None):

        payload = {
            'symbol': symbol if symbol else self.symbol
        }
        return self._request('POST', '/v2/private/order/cancelAll', payload=payload)

    def cancel_all_conditional_orders(self, symbol=None):

        payload = {
            'symbol': symbol if symbol else self.symbol
        }
        return self._request('POST', '/v2/private/stop-order/cancelAll', payload=payload)

    def get_active_order_real_time(self, symbol=None):

        payload = {
            'symbol': symbol if symbol else self.symbol
        } 
        return self._request('GET', '/v2/private/order', payload=payload)

    def get_wallet_balance(self, coin=None):

        payload = {
            'coin': coin if coin else self.symbol
        }
        return self._request('GET', '/v2/private/wallet/balance', payload=payload)

    def get_tickers(self, symbol=None):

        payload = {
            'symbol': symbol if symbol else self.symbol
        }
        return self._request('GET', '/v2/public/tickers', payload=payload)

    def get_api_data(self):

        payload = {}
        return self._request('GET', '/open-api/api-key', payload=payload)

    def replace_active_order(self, order_id = None, symbol=None,
                              p_r_qty=None, p_r_price=None):
 
        payload = {
            'order_id': order_id,
            'symbol': symbol if symbol else self.symbol,
            'p_r_qty': p_r_qty,
            'p_r_price': p_r_price
        }
        return self._request('POST', '/open-api/order/replace', payload=payload)


    def get_user_trade_record(self, symbol=None, start_time=None, end_time=None, page=None, exec_type=None, limit=None,order=None):

        payload = {
            'symbol': symbol,
            'start_time': start_time,
            'end_time':end_time,
            'exec_type': exec_type,
            'page':page,
            'limit':limit,
            'order':order

        }
        return self._request('GET', '/v2/private/trade/closed-pnl/list', payload=payload)
