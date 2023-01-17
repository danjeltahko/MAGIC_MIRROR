from datetime import datetime, timedelta
from urllib import parse
import requests
import json

from API.api_keys import *


class Fitbit:

    def __init__(self) -> None:

        self.header = {
            "Authorization" : None,
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "connection":"keep-alive"
        }

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
        print(f"Creating URL for fitbit")
        return f"https://www.fitbit.com/oauth2/authorize?{parse.urlencode(params)}"

    def get_token(self, code:str):
        """ Gets access token from fitbit """
        URL = "https://api.fitbit.com/oauth2/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": FITBIT_CLIENT_ID,
            "code": code,
            "code_verifier": FITBIT_CODE_VERIFIER
        }
        response = requests.post(URL, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        print(f"Received code from redirected URI\n-> {code}")
        print(f"Response: {response.status_code}\nData: {response.text}")
        if (response.status_code == 200):
            load = json.loads(response.text)
            self.user_id = load["user_id"]
            self.access_token = load["access_token"]
            self.refresh_token = load["refresh_token"]
            self.token_type = load["token_type"]
            self.authorization = self.token_type + " " + self.access_token
            self.header["Authorization"] = self.authorization
            self.expires_in = datetime.strptime((datetime.now() + timedelta(seconds=int(load["expires_in"]))).strftime("%m-%d-%y %H:%M:%S"), "%m-%d-%y %H:%M:%S")
        else:
            print("Failed to retrive access token...")

    def refreshing_token(self):
        data = {
            "grant_type": "refresh_token",
            "client_id": FITBIT_CLIENT_ID,
            "refresh_token": self.refresh_token
        }
        URL = "https://www.fitbit.com/oauth2/authorize"
        response = requests.post(URL, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        print(response)
        if (response.status_code == 200):
            load = json.loads(response.text)
            self.user_id = load["user_id"]
            self.access_token = load["access_token"]
            self.refresh_token = load["refresh_token"]
            self.token_type = load["token_type"]
        else:
            print("Failed to retrive refreshed access token...")


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

    def get_sleep_summary(self):
        """ 
            adds past weeks sleep data as dictionary in list 
            with startdate & enddate and also summary.
            * adds an average dictionary at det end
        """
        data = self.get_sleep_log()
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
                day = ['Mån','Tis', 'Ons', 'Tor', 'Fre', 'Lör', 'Sön'][datetime.strptime(start_time.split('T')[0], "%Y-%m-%d").weekday()]
                total_sleep = sleep["minutesAsleep"]
                total_minutes += total_sleep

                sleep_summary = {
                    "start": start_time,
                    "end": end_time,
                    "day": day,
                    "hours": int(total_sleep/60),
                    "minutes": total_sleep % 60,
                    "deep": deep_sleep,
                    "light": light_sleep,
                    "rem": rem_sleep
                }
                sleep_data.append(sleep_summary)

            avg_sleep = int(total_minutes/len(data["sleep"]))
            fitbit_sleep = {"summary": {"hours": int(avg_sleep/60),"minutes": avg_sleep % 60},
                            "data": sleep_data}

            return fitbit_sleep
        else:
            print("Could not retrieve sleep log")
            return []




        


if __name__ == "__main__":
    fitbit = Fitbit()






