# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.btcbox import btcbox


class jubi (btcbox):

    def describe(self):
        return self.deep_extend(super(jubi, self).describe(), {
            'id': 'jubi',
            'name': 'jubi.com',
            'countries': ['CN'],
            'rateLimit': 1500,
            'version': 'v1',
            'has': {
                'CORS': False,
                'fetchTickers': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766581-9d397d9a-5edd-11e7-8fb9-5d8236c0e692.jpg',
                'api': 'https://www.jubi.com/api',
                'www': 'https://www.jubi.com',
                'doc': 'https://www.jubi.com/help/api.html',
            },
        })

    def fetch_markets(self, params={}):
        markets = self.publicGetAllticker(params)
        keys = list(markets.keys())
        result = []
        for i in range(0, len(keys)):
            id = keys[i]
            baseId = id
            quoteId = 'cny'
            base = self.common_currency_code(baseId.upper())
            quote = self.common_currency_code(quoteId.upper())
            symbol = base + '/' + quote
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'info': id,
            })
        return result
