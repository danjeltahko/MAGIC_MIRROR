from API.api_keys import *
from urllib import parse
import requests
import json

class ToDo:

    def __init__(self) -> None:
        self.active = False


        self.api = "https://graph.microsoft.com/v1.0"

        self.header = {
            "Authorization" : None,
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "connection":"keep-alive"
        }

        self.token_type = None
        self.access_token = None
        self.time_limit = None

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
            self.time_limit = load["expires_in"]
            self.token_type = load["token_type"]
            self.authorization = self.token_type + " " + self.access_token
            self.header["Authorization"] = self.authorization
            self.active = True
        else:
            print("Failed to retrive access token...")

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
            if (response.status_code == 200):
                data = json.loads(response.text)
                for task in data["value"]:
                    tasks.append(task["title"])
                task_data["tasks"] = tasks
                return task_data
            else:
                print("Could not retrive data, raise error?")
                return None

        except:
            print("except in try & catch with todo tasks")
            return None