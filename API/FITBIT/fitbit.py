from datetime import datetime, timedelta
from urllib import parse
import requests
import json

from API.api_keys import *

class Fitbit:

    def __init__(self) -> None:

        # This header is used for api request, not authorization
        self.header = {
            "Authorization" : None,
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "connection":"keep-alive"
        }
        # General init
        self.user_id = None
        self.access_token = None
        self.refresh_token = None
        self.token_type = None
        self.expires_in = None

    def authorize(self) -> str:
        """ Create and return authorization url for Fitbit """
        params = {
            "client_id": FITBIT_CLIENT_ID,
            "response_type": "code",
            "scope": "activity cardio_fitness electrocardiogram heartrate location nutrition oxygen_saturation profile respiratory_rate settings sleep social temperature weight",
            "code_challenge": FITBIT_CODE_CHALLENGE,
            "code_challenge_method": "S256",
            "state": FITBIT_STATE
        }
        # parse.urlencode creates url suited string of all parameters
        return f"https://www.fitbit.com/oauth2/authorize?{parse.urlencode(params)}"

    def get_token(self, code:str) -> bool:
        """ Gets access token from fitbit """
        URL = "https://api.fitbit.com/oauth2/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": FITBIT_CLIENT_ID,
            "code": code,
            "code_verifier": FITBIT_CODE_VERIFIER
        }
        # if everything worked as intended response will give as access token & other necessary data
        response = requests.post(URL, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        if (response.status_code == 200):
            load = json.loads(response.text)
            self.user_id = load["user_id"]
            self.access_token = load["access_token"]
            self.refresh_token = load["refresh_token"]
            self.token_type = load["token_type"]
            self.header["Authorization"] = self.token_type + " " + self.access_token
            self.expires_in = datetime.strptime((datetime.now() + timedelta(seconds=int(load["expires_in"])-10)).strftime("%m-%d-%y %H:%M:%S"), "%m-%d-%y %H:%M:%S")
            return True
        else:
            return False

    def refreshing_token(self) -> bool:
        """ refreshing access token when it expires """
        data = {
            "grant_type": "refresh_token",
            "client_id": FITBIT_CLIENT_ID,
            "refresh_token": self.refresh_token
        }
        URL = "https://www.fitbit.com/oauth2/authorize"
        # if everything worked as intended response will give as a new access token
        response = requests.post(URL, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        if (response.status_code == 200):
            load = json.loads(response.text)
            self.user_id = load["user_id"]
            self.access_token = load["access_token"]
            self.refresh_token = load["refresh_token"]
            self.token_type = load["token_type"]
            return True
        else:
            return False

    def get_sleep_log(self) -> dict:
        """ returns all sleep data from past week """
        url = f"https://api.fitbit.com/1.2/user/{self.user_id}/sleep/list.json"
        past_week = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        parameters = {
            "afterDate": past_week,
            "sort": "desc",
            "limit": "100",
            "offset": "0"
        }
        response = requests.get(url, params=parameters, headers=self.header)
        if (response.status_code == 200):
            data = json.loads(response.text)
            return data
        else:
            return None

    def get_sleep_summary(self) -> dict:
        """ 
            adds past weeks sleep data as dictionary in list 
            with startdate & enddate and also summary.
            * adds an average dictionary at det end
        """
        data = self.get_sleep_log()
        # if data is a dictionary with sleep data
        if (data != None):
            sleep_data = []
            total_minutes = 0
            for sleep in data["sleep"]:

                summary = sleep["levels"]["summary"]
                # if deep,light or rem even exists
                if ("deep" in summary):
                    deep_sleep = summary["deep"]["minutes"]
                if ("light" in summary):
                    light_sleep = summary["light"]["minutes"]
                if ("rem" in summary):
                    rem_sleep = summary["rem"]["minutes"]

                start_time = sleep["startTime"]
                end_time = sleep["endTime"]
                # takes date(2023-01-17T01:47:00.000), converting to datetime(2023-01-17), getting weekday index & gets that value in list
                day = ['Måndag','Tisdag', 'Onsdag', 'Tordag', 'Fredag', 'Lördag', 'Söndag'][datetime.strptime(start_time.split('T')[0], "%Y-%m-%d").weekday()]
                total_sleep = sleep["minutesAsleep"]
                total_minutes += total_sleep

                sleep_summary = {
                    "start": start_time,
                    "end": end_time,
                    "day": day,
                    "hours": int(total_sleep/60),
                    "minutes": total_sleep % 60,
                    "total_minutes" : total_sleep,
                    "deep": deep_sleep,
                    "light": light_sleep,
                    "rem": rem_sleep
                }
                sleep_data.append(sleep_summary)

            avg_sleep = int(total_minutes/len(data["sleep"]))
            fitbit_sleep = {"summary": f"Sömn: ~{int(avg_sleep/60)}h {avg_sleep % 60}min", "data": sleep_data}
            return fitbit_sleep
        else:
            return {"summary": "ERROR", "data": ["Could not retrieve sleep log"]}


if __name__ == "__main__":
    fitbit = Fitbit()