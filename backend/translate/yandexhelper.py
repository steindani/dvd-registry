'''
Created on Nov 17, 2015

@author: benjo
'''

import requests, json

api_key = 'trnsl.1.1.20151117T102755Z.bfcf9daea0a5eec5.05eead1277a72db8492c639285107c946c074188'
yandex_prefix = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=' + api_key
add_text = '&text='
yandex_postfix = '&lang=en-hu'

def translate( text ):
    response = requests.request( 'GET', yandex_prefix + add_text + str( text ) + yandex_postfix )
    data = json.loads( response.text )
    return data['text'][0]