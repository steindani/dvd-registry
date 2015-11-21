'''
Created on Nov 21, 2015

@author: benjo
'''

from datetime import datetime, timedelta
from flask import g, send_file, request, jsonify, abort, url_for
from functools import wraps
from jwt import DecodeError, ExpiredSignature
import config.configuration
import json
import jwt
import os
import requests


def create_token( user ):
    payload = {
        'sub': user.googleid,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta( days = 14 )
    }
    token = jwt.encode( payload, config.configuration.app.config['TOKEN_SECRET'] )
    return token.decode( 'unicode_escape' )


def parse_token( req ):
    token = req.headers.get( 'Authorization' ).split()[1]
    return jwt.decode( token, config.configuration.app.config['TOKEN_SECRET'] )


def login_required( f ):
    @wraps( f )
    def decorated_function( *args, **kwargs ):
        if not request.headers.get( 'Authorization' ):
            response = jsonify( message = 'Missing authorization header' )
            response.status_code = 401
            return response

        try:
            payload = parse_token( request )
        except DecodeError:
            response = jsonify( message = 'Token is invalid' )
            response.status_code = 401
            return response
        except ExpiredSignature:
            response = jsonify( message = 'Token has expired' )
            response.status_code = 401
            return response

        g.googleid = payload['sub']

        return f( *args, **kwargs )

    return decorated_function
