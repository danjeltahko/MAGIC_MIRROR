from API.api_keys import *
from datetime import datetime, timedelta
from urllib import parse
import requests
import json

class ToDo:

    def __init__(self) -> None:

        self.header = {
            "Authorization" : None,
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "connection":"keep-alive"
        }

        self.active = False
        self.token_type = None
        self.access_token = None
        self.expires_in = None
        self.refresh_token = None

    def authorize(self) -> str:
        """ Create and return authorization url for Microsoft Todo """
        params = {
            "client_id": AZURE_CLIENT_ID,
            "response_type": "code",
            "redirect_uri": "http://localhost:1312/getAzureToken",
            "response_mode": "query",
            "scope": "offline_access Tasks.ReadWrite",
            "state": "007"
        }
        URL = f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?{parse.urlencode(params) }"
        return URL
   
    def get_token(self, code:str) -> None:
        """ Gets access token from Microsoft """
        URL = f"https://login.microsoftonline.com/common/oauth2/v2.0/token"
        data = {
            "client_id": AZURE_CLIENT_ID,
            "scope": "offline_access Tasks.ReadWrite",
            "code": code,
            "redirect_uri": "http://localhost:1312/getAzureToken",
            "grant_type": "authorization_code",
            "client_secret": AZURE_CLIENT_VALUE
        }
        response = requests.post(URL, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        print(response)
        if (response.status_code == 200):
            load = json.loads(response.text)
            self.access_token = load["access_token"]
            self.expires_in = datetime.strptime((datetime.now() + timedelta(seconds=int(load["expires_in"]))).strftime("%d-%m-%y %H:%M:%S"), "%d-%m-%y %H:%M:%S")
            self.token_type = load["token_type"]
            self.authorization = self.token_type + " " + self.access_token
            self.header["Authorization"] = self.authorization
            self.refresh_token = load["refresh_token"]
            self.active = True
        else:
            self.active = False
            print("Failed to retrive access token...")

    def refresh_get_token (self):
        """ Refresh access token """

        print("Trying to refresh access token with refresh token")

        URL = f"https://login.microsoftonline.com/common/oauth2/v2.0/token"
        data = {
            "client_id": AZURE_CLIENT_ID,
            "scope": "offline_access Tasks.ReadWrite",
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token",
            "client_secret": AZURE_CLIENT_VALUE
        }
        response = requests.post(URL, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        print(response)
        if (response.status_code == 200):
            load = json.loads(response.text)
            self.access_token = load["access_token"]
            self.token_type = load["token_type"]
            self.expires_in = datetime.strptime((datetime.now() + timedelta(seconds=int(load["expires_in"]))).strftime("%d-%m-%y %H:%M:%S"), "%d-%m-%y %H:%M:%S")
            self.authorization = self.token_type + " " + self.access_token
            self.header["Authorization"] = self.authorization
            self.refresh_token = load["refresh_token"]
            self.active = True
            print("Successfully refreshed access token with refresh token")
        else:
            self.active = False
            print("Filed to refreshed access token with refresh token")

    def get_all_tasks(self):
        URL = "https://graph.microsoft.com/v1.0/me/todo/lists"
        response = requests.get(URL, headers=self.header)
        return response

    def return_tasks(self, list_name) -> dict:

        try:
            URL = f"https://graph.microsoft.com/v1.0/me/todo/lists/{TODO_LIST_ID[list_name]}/tasks"
            response = requests.get(URL, headers=self.header)
            task_data = {"name": list_name}
            tasks = []
            print(f"return_tasks : {response}")
            if (response.status_code == 200):
                data = json.loads(response.text)
                for task in data["value"]:
                    tasks.append(task["title"])
                task_data["tasks"] = tasks
                return task_data
            else:
                print("Could not retrive data from microsoft graph, raise error?")
                self.active = False
                self.refresh_get_token()
                return None

        except:
            print("except in try & catch with todo tasks")
            self.active = False
            self.refresh_get_token()
            return None