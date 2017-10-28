import requests
import os
import json
import uuid
import time


AUTHORIZATION_ENDPOINT = 'authorize'
TOKEN_ENDPOINT = 'token'


class OAuth2Session(object):
    base_url = None
    client_id = None
    client_secret = None
    redirect_uri = None
    token = None
    state = None
    expiry = None

    """docstring for OAuth2Session"""
    def __init__(self, base_url, client_id, client_secret, redirect_uri):
        super(OAuth2Session, self).__init__()

        if base_url[-1] != '/':
            base_url = base_url + '/'
        self.base_url = base_url

        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.state = str(uuid.uuid4())

    def authorization_url(self, scopes=None):
        # base url + query start
        authorization_url = self.base_url + AUTHORIZATION_ENDPOINT + '?'

        params = {
            # 'scope': scopes,
            'response_type': 'code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'state': self.state,
        }

        # add key=value& for all in params
        for key, value in params.items():
            authorization_url = authorization_url + key + '=' + value + '&'

        authorization_url = authorization_url[:-1]

        return authorization_url

    def authorize(self, auth_response):
        response = self._url_to_params(auth_response)

        try:
            if response['state'] != self.state:
                raise ValueError("WARNING: CSRF detected. Please start the process again.")
        except KeyError:
            raise ValueError("WARNING: CSRF detected. Please start the process again.")

        token_url = self.base_url + TOKEN_ENDPOINT

        params = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'code': response['code'],
        }
        
        r = requests.post(token_url, data=params)
        if r.status_code == 200:
            self.token = r.json()
            self.expiry = time.time() + self.token['expires_in']
            return True
        else:
            return False

    def get(self, url, params=None):
        if self.is_authorized():
            return self._get(url, params)
        else:
            self._refresh_token()
            return self._get(url, params)

    def is_authorized(self):
        return (self.token != None and self.expiry > time.time())

    def _get(self, url, params=None):
        if self.token:
            header = {
                'Authorization': 'Bearer {}'.format(self.token['access_token'])
            }

            return requests.get(self.base_url + url, headers=header, params=params)
        else:
            raise AttributeError("No token found. Restart SumUp OAuth Authentification.")

    def _refresh_token(self):
        if self.token:
            params = {
                'grant_type': 'refresh_token',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'refresh_token': self.token['refresh_token'],
            }
            r = self._get(TOKEN_ENDPOINT, params=params)
            return r.status_code == 200
        else:
            return False

    def _url_to_params(self, url):
        # Take only the parameters part of url, and then split on 'key=value' pairs, then make dict {'key':'value'}
        url = url.split('?')[1]
        return {x[0] : x[1] for x in [y.split('=') for y in url.split('&')]}










