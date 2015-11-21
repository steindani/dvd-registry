'''
Created on Nov 21, 2015

@author: benjo

'''

from flask import Flask
from flask_cors import CORS
import os


def init( file, name ):
    # Configuration
    current_path = os.path.dirname( file )
    client_path = os.path.abspath( os.path.join( current_path, '..', '..', 'client' ) )
    
    global app
    app = Flask( name , static_url_path = '', static_folder = client_path )
    app.config.from_object( 'config.config' )

    cors = CORS( app, resources = {
        r"/helper/search": {
            "origins": [{"*"}, {"localhost:9000"}, {"localhost:5000"}],
            "send_wildcard": True
            },
                                   
        r"/search/movies": {
            "origins": [{"*"}, {"localhost:9000"}, {"localhost:5000"}],
            "send_wildcard": True
            },
            
        r"/media": {
            "origins": [{"*"}, {"localhost:9000"}, {"localhost:5000"}],
            "send_wildcard": True
            },
            
        r"/movies": {
            "origins": [{"*"}, {"localhost:9000"}, {"localhost:5000"}],
            "send_wildcard": True
            },
            
        r"/random": {
            "origins": [{"*"}, {"localhost:9000"}, {"localhost:5000"}],
            "send_wildcard": True
            },
            
        r"/random/one": {
            "origins": [{"*"}, {"localhost:9000"}, {"localhost:5000"}],
            "send_wildcard": True
            },
        
        r"/auth/google": {
            "origins": [{"localhost:9000"}, {"localhost:5000"}]
            }
        } )
