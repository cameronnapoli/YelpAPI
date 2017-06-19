# Copyright Cameron Napoli 2017
# Demo of Yelp API and responses

import requests
import urllib

class YelpAPIInterface():
    auth_token_url = "https://api.yelp.com/oauth2/token"
    # NOTE: Your Yelp App client ID here
    client_id = ""
    # NOTE: Your Yelp App client secret here
    client_secret = ""

    search_url = "https://api.yelp.com/v3/businesses/search"

    def __init__(self):
        return

    # POST request to URL which returns an access token
    def fetchYelpToken(self):
        auth_req = requests.post(self.auth_token_url, data = \
            {'client_id': self.client_id, \
             'client_secret': self.client_secret})
        if 'access_token' not in auth_req.json():
            return False
        return auth_req.json()['access_token']

    # GET request with access token in header which fetches API data
    def getYelpAPIResponse(self):
        token = self.fetchYelpToken() # fetch token
        if(token == False):
            return ""

        oauth_header = {'Authorization': 'Bearer ' + token}
        params = {
            "term":"bars",
            "location":"Irvine,CA",
            "radius":"5000"
        }
        req_url = self.search_url +"?"+ urllib.parse.urlencode(params)
        print(req_url + "   ") # DEBUG

        api_req = requests.get(req_url, headers=oauth_header)
        return api_req.text

y = YelpAPIInterface()

print(y.getYelpAPIResponse())
