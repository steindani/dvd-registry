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

    CORS( app, resources = {
        r"/helper/search": {
            "origins": [{"*"}],
            "send_wildcard": True
            },
                                   
        r"/search/movies": {
            "origins": [{"*"}],
            "send_wildcard": True
            },
            
        r"/media": {
            "origins": [{"*"}],
            "send_wildcard": True
            },
            
        r"/movies": {
            "origins": [{"*"}],
            "send_wildcard": True
            },
            
        r"/random": {
            "origins": [{"*"}],
            "send_wildcard": True
            },
            
        r"/random/one": {
            "origins": [{"*"}],
            "send_wildcard": True
            },
        
        r"/auth/google": {
            "origins": [{"*"}]  # old: {"localhost:9000"}, {"localhost:5000"}
            }
        } )
