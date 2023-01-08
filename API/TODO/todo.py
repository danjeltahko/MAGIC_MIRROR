from API.api_keys import *
from urllib import parse
import requests
import json

class ToDo:

    def __init__(self) -> None:
        self.active = False

        self.auth_url = f"https://login.microsoftonline.com/common/oauth2/v2.0/"
        self.api = "https://graph.microsoft.com/v1.0"

        self.header = {"Content-Type": "application/x-www-form-urlencoded"}
        self.token_type = None
        self.access_token = None
        self.time_limit = None

    def authorize(self) -> str:
        """ Create authorization url for Microsoft Todo """
        params = {
            "client_id": AZURE_CLIENT_ID,
            "response_type": "code",
            "redirect_uri": "http://localhost:1312/getAzureToken",
            "response_mode": "query",
            "scope": "openid profile offline_access User.Read Mail.Read Tasks.ReadWrite",
            "state": "007"
        }
        URL = f"{self.auth_url}authorize?{parse.urlencode(params) }"
        return URL

    
    def get_token(self, code:str) -> None:
        """ Gets access token from Microsoft """
        URL = f"https://login.microsoftonline.com/common/oauth2/v2.0/token"
        data = {
            "client_id": AZURE_CLIENT_ID,
            "scope": "openid profile offline_access User.Read Mail.Read Tasks.ReadWrite",
            "code": code,
            "redirect_uri": "http://localhost:1312/getAzureToken",
            "grant_type": "authorization_code",
            "client_secret": AZURE_CLIENT_VALUE
        }
        response = requests.post(URL, data=data, headers=self.header)
        print(response)
        if (response.status_code == 200):
            load = json.loads(response.text)
            self.access_token = load["access_token"]
            self.time_limit = load["expires_in"]
            self.token_type = load["token_type"]
            self.active = True
        else:
            print("Failed to retrive access token...")

    def graph_request(self, user_input:str):
        authorization = self.token_type + " " + self.access_token
        header = {
            "Authorization" : authorization,
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "connection":"keep-alive"
        }
        URL = self.api + user_input
        response = requests.get(URL, headers=header)
        return response.text