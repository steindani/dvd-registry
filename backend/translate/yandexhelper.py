'''
Created on Nov 17, 2015

@author: benjo
'''

import requests, json
import config.configuration

def translate( text ):
    yandex_prefix = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=' + config.configuration.app.config['YANDEX_KEY'] + '&text='
    yandex_postfix = '&lang=en-hu'
    
    response = requests.request( 'GET', yandex_prefix + str( text ) + yandex_postfix )
    data = json.loads( response.text )
    try:
        return data['text'][0]
    except KeyError:
        return ''
    
    
