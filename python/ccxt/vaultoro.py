# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange


class vaultoro (Exchange):

    def describe(self):
        return self.deep_extend(super(vaultoro, self).describe(), {
            'id': 'vaultoro',
            'name': 'Vaultoro',
            'countries': ['CH'],
            'rateLimit': 1000,
            'version': '1',
            'has': {
                'CORS': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766880-f205e870-5ee9-11e7-8fe2-0d5b15880752.jpg',
                'api': 'https://api.vaultoro.com',
                'www': 'https://www.vaultoro.com',
                'doc': 'https://api.vaultoro.com',
            },
            'commonCurrencies': {
                'GLD': 'Gold',
            },
            'api': {
                'public': {
                    'get': [
                        'bidandask',
                        'buyorders',
                        'latest',
                        'latesttrades',
                        'markets',
                        'orderbook',
                        'sellorders',
                        'transactions/day',
                        'transactions/hour',
                        'transactions/month',
                    ],
                },
                'private': {
                    'get': [
                        'balance',
                        'mytrades',
                        'orders',
                    ],
                    'post': [
                        'buy/{symbol}/{type}',
                        'cancel/{id}',
                        'sell/{symbol}/{type}',
                        'withdraw',
                    ],
                },
            },
        })

    def fetch_markets(self, params={}):
        result = []
        response = self.publicGetMarkets(params)
        market = self.safe_value(response, 'data')
        baseId = self.safe_string(market, 'MarketCurrency')
        quoteId = self.safe_string(market, 'BaseCurrency')
        base = self.common_currency_code(baseId)
        quote = self.common_currency_code(quoteId)
        symbol = base + '/' + quote
        id = self.safe_string(market, 'MarketName')
        result.append({
            'id': id,
            'symbol': symbol,
            'base': base,
            'quote': quote,
            'baseId': baseId,
            'quoteId': quoteId,
            'info': market,
        })
        return result

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetBalance(params)
        balances = self.safe_value(response, 'data')
        result = {'info': balances}
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = balance['currency_code']
            uppercaseId = currencyId.upper()
            code = self.common_currency_code(uppercaseId)
            free = self.safe_float(balance, 'cash')
            used = self.safe_float(balance, 'reserved')
            total = self.sum(free, used)
            account = {
                'free': free,
                'used': used,
                'total': total,
            }
            result[code] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        response = self.publicGetOrderbook(params)
        orderbook = {
            'bids': response['data'][0]['b'],
            'asks': response['data'][1]['s'],
        }
        return self.parse_order_book(orderbook, None, 'bids', 'asks', 'Gold_Price', 'Gold_Amount')

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        quote = self.publicGetBidandask(params)
        bidsLength = len(quote['bids'])
        bid = quote['bids'][bidsLength - 1]
        ask = quote['asks'][0]
        response = self.publicGetMarkets(params)
        ticker = self.safe_value(response, 'data')
        timestamp = self.milliseconds()
        last = self.safe_float(ticker, 'LastPrice')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, '24hHigh'),
            'low': self.safe_float(ticker, '24hLow'),
            'bid': bid[0],
            'bidVolume': None,
            'ask': ask[0],
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': None,
            'quoteVolume': self.safe_float(ticker, '24hVolume'),
            'info': ticker,
        }

    def parse_trade(self, trade, market):
        timestamp = self.parse8601(self.safe_string(trade, 'Time'))
        return {
            'id': None,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'order': None,
            'type': None,
            'side': None,
            'price': trade['Gold_Price'],
            'amount': trade['Gold_Amount'],
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetTransactionsDay(params)
        return self.parse_trades(response, market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        method = 'privatePost' + self.capitalize(side) + 'SymbolType'
        request = {
            'symbol': market['quoteId'].lower(),
            'type': type,
            'gld': amount,
            'price': price or 1,
        }
        response = getattr(self, method)(self.extend(request, params))
        return {
            'info': response,
            'id': response['data']['Order_ID'],
        }

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'id': id,
        }
        return self.privatePostCancelId(self.extend(request, params))

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/'
        if api == 'public':
            url += path
        else:
            self.check_required_credentials()
            nonce = self.nonce()
            url += self.version + '/' + self.implode_params(path, params)
            query = self.extend({
                'nonce': nonce,
                'apikey': self.apiKey,
            }, self.omit(params, self.extract_params(path)))
            url += '?' + self.urlencode(query)
            headers = {
                'Content-Type': 'application/json',
                'X-Signature': self.hmac(self.encode(url), self.encode(self.secret)),
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
