# Written by: Cameron Napoli, 2017
# Demo of Yelp API and responses

import requests
import urllib

class YelpAPIInterface():
    ''' API interface to make HTTP requests to fetch Yelp data '''

    auth_token_url = "https://api.yelp.com/oauth2/token"
    search_url = "https://api.yelp.com/v3/businesses/search"

    def __init__(self, api_config_file_name):
        # Read client id & client secret from config file
        with open(api_config_file_name) as f:
            for line in f:
                if 'YELP_CLIENT_ID' in line:
                    self.client_id = line.split('=')[1].strip(' \n')
                elif 'YELP_CLIENT_SECRET' in line:
                    self.client_secret = line.split('=')[1].strip(' \n')

    def fetchYelpToken(self):
        '''
        POST request to URL which returns an access token

        :returns: access token from Yelp
        '''

        auth_req = requests.post(self.auth_token_url, data = \
            {'client_id': self.client_id, \
             'client_secret': self.client_secret})

        if 'access_token' not in auth_req.json():
            return False

        return auth_req.json()['access_token']

    def getYelpAPIResponse(self, params):
        '''
        GET request with access token in header which fetches API data

        :param params: parameters to be passed into Yelp query
        :returns: JSON response from Yelp
        '''
        token = self.fetchYelpToken()
        if not token:
            return None

        # Yelp Basic Authentication header
        oauth_header = {'Authorization': 'Bearer ' + token}

        # change parameters into URL form and concatentate them with
        # the search url
        req_url = self.search_url +"?"+ urllib.parse.urlencode(params)

        # send HTTP request to Yelp API
        api_req = requests.get(req_url, headers=oauth_header)

        # return API response content
        return api_req.text



y = YelpAPIInterface('yelp_api_config.txt')

params = {
    "term": "sushi",
    "location": "Irvine,CA",
    "radius": "5000"
}

print(y.getYelpAPIResponse(params))
