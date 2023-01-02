import webbrowser
import requests
import json

from API.api_keys import *


class Fitbit:

    def __init__(self) -> None:

        self.client_id = FITBIT_CLIENT_ID
        # inside url from authorization request
        self.auth_code = None

        self.user_id = None
        self.access_token = None
        self.refresh_token = None
        self.token_type = None

        self.auth_url = "https://api.fitbit.com/oauth2/token"
        self.header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

    def open_browser(self):
        # can we do this to flask/django page? 127.0.0.1:1312/token/ ?? extract it directly
        url = f"https://www.fitbit.com/oauth2/authorize?response_type=code&client_id={self.client_id}&scope=activity+cardio_fitness+electrocardiogram+heartrate+location+nutrition+oxygen_saturation+profile+respiratory_rate+settings+sleep+social+temperature+weight&code_challenge={PKCE_challenge}&code_challenge_method=S256&state={PKCE_state}"
        webbrowser.open(url)
        self.auth_code = str(input("Auth code -> "))

    def get_token(self):
        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "code": self.auth_code,
            "code_verifier": PKCE_verifier
        }
        response = requests.post(self.auth_url, data=data, headers=self.header)
        print(response)
        if (response.status_code == 200):
            load = json.loads(response.text)
            self.user_id = load["user_id"]
            self.access_token = load["access_token"]
            self.refresh_token = load["refresh_token"]
            self.token_type = load["token_type"]
        #print(response.text)

    def refreshing_token(self):
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "refresh_token": self.refresh_token
        }
        response = requests.post(self.auth_url, data=data, headers=self.header)
        print(response)
        if (response.status_code == 200):
            load = json.loads(response.text)
            self.user_id = load["user_id"]
            self.access_token = load["access_token"]
            self.refresh_token = load["refresh_token"]
            self.token_type = load["token_type"]
        #print(response.text)


    def access_user_data(self):
        authorization = self.token_type + " " + self.access_token
        url = "https://api.fitbit.com/1/user/-/profile.json"
        header = {
            "Authorization" : authorization
        }
        response = requests.get(url, headers=header)
        print(response)
        #print(response.text)

    def get_sleep_log(self):
        url = f"https://api.fitbit.com/1.2/user/{self.user_id}/sleep/list.json"
        authorization = self.token_type + " " + self.access_token
        header = {
            "Authorization" : authorization,
            "accept": "application/json"
        }
        parameters = {
            "afterDate": "2022-12-26",
            "sort": "desc",
            "limit": "100",
            "offset": "0"
        }
        response = requests.get(url, params=parameters, headers=header)
        print(response)
        print(response.text)

    
    def run(self):

        # open url to extract authorization code from request url
        print("\nOpen url to login and choose scopes, extract code from redirected url")
        self.open_browser()
        print("\n* GET TOKEN")
        self.get_token()
        print("\n* GET USER DATA")
        #self.access_user_data()
        #if (404):
        #    self.refreshing_token()
        self.get_sleep_log()


if __name__ == "__main__":
    fitbit = Fitbit()
    fitbit.run()






