from API.api_keys import *
from datetime import datetime, timedelta
from urllib import parse
from threading import Thread
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
        self.token_type = None
        self.access_token = None
        self.expires_in = None
        self.refresh_token = None

        self.list_name = None

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
        URL = f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?{parse.urlencode(params)}"
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
        print(f"Access token request:  {response.status_code}")
        if (response.status_code == 200):
            load = json.loads(response.text)
            self.access_token = load["access_token"]
            self.expires_in = datetime.strptime((datetime.now() + timedelta(seconds=int(load["expires_in"]))).strftime("%m-%d-%y %H:%M:%S"), "%m-%d-%y %H:%M:%S")
            self.token_type = load["token_type"]
            self.authorization = self.token_type + " " + self.access_token
            self.header["Authorization"] = self.authorization
            self.refresh_token = load["refresh_token"]
        else:
            print("Failed to retrive access token...")

    def refresh_get_token(self) -> None:
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
            self.expires_in = datetime.strptime((datetime.now() + timedelta(seconds=int(load["expires_in"]))).strftime("%m-%d-%y %H:%M:%S"), "%m-%d-%y %H:%M:%S")
            self.authorization = self.token_type + " " + self.access_token
            self.header["Authorization"] = self.authorization
            self.refresh_token = load["refresh_token"]
            print("Successfully refreshed access token with refresh token")
        else:
            print("Filed to refreshed access token with refresh token")

    def return_tasks(self, list_name) -> dict:

        try:
            self.list_name = list_name
            URL = f"https://graph.microsoft.com/v1.0/me/todo/lists/{TODO_LIST_ID[self.list_name]}/tasks"
            response = requests.get(URL, headers=self.header)
            task_data = {"name": list_name}
            tasks = []
            print(f"return_tasks : {response}")
            if (response.status_code == 200):
                data = json.loads(response.text)
                completed_tasks = []
                for task in data["value"]:

                    # Only add tasks thats not done
                    if (task["status"] == "notStarted"):
                        tasks.append(task["title"])
                    # Remove done tasks
                    else:
                        completed_tasks.append(task["id"])
                
                thread = Thread(target=self.delete_tasks_thread, args=(completed_tasks,))
                thread.start()

                task_data["tasks"] = tasks
                return task_data

            else:
                print("Could not retrive data from microsoft graph, raise error?")
                return None

        except:
            print("except in try & catch with todo tasks")
            return None

    def add_task(self, new_task) -> None:

        try:
            URL = f"https://graph.microsoft.com/v1.0/me/todo/lists/{TODO_LIST_ID[self.list_name]}/tasks"
            data = {
                "title": new_task,
                "categories": [],
                "linkedResources":[
                    {
                        "webUrl":"http://microsoft.com",
                        "applicationName":"Magic Mirror",
                        "displayName":"Magic Mirror"
                    }
                ]
            }
            response = requests.post(URL, json=data, headers=self.header)
            print(f"Added new task : {new_task} [{response.status_code}]")
            if (response.status_code == 201):
                print(f"Successfully added new task to {self.list_name}")
            else:
                print(f"Failed to add new task to {self.list_name}")
                
        except:
            print("Could not create new task to list")


    def delete_tasks_thread(self, completes_tasks) -> None:

        for task in completes_tasks:
            try:
                delete_url = f"https://graph.microsoft.com/v1.0/me/todo/lists/{TODO_LIST_ID[self.list_name]}/tasks/{task}"
                delete_res = requests.delete(delete_url, headers=self.header)
                print(f"{delete_res.status_code} - Deleted {task} task")
            except:
                print(f"Could not delete {task} task")