import requests, json
import config.configuration

def translate( text ):
    #yandex_prefix = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=' + config.configuration.app.config['YANDEX_KEY'] + '&text='
    yandex_prefix = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=' + 'trnsl.1.1.20151117T102755Z.bfcf9daea0a5eec5.05eead1277a72db8492c639285107c946c074188' + '&text='
    yandex_postfix = '&lang=en-hu'
    
    response = requests.request( 'GET', yandex_prefix + str( text ) + yandex_postfix )
    data = json.loads( response.text )
    try:
        return data['text'][0]
    except KeyError:
        return ''
    
    
