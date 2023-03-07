import requests
import pandas as pd
import os, sys
import json
project = "https://1001albumsgenerator.com/moamagicmirror"


class AlbumGenerator:

    def __init__(self) -> None:
        self.endpoint = "https://1001albumsgenerator.com/api/v1/projects/moamagicmirror"

    def getTodaysAlbum(self):

        # get todays album and convert to json
        response = requests.get(self.endpoint)
        data = json.loads(response.text)

        # write/store/log json to file
        try:
            with open("todays_album.json", "w") as file:
                file.write(data)
        except FileNotFoundError:
            with open("todays_album.json", "a") as file:
                file.write(data)

        return data

    
    """ WIP """
    def randomGenerator(self):
        try:
            with open("API/ALBUMGEN/all_albums.csv", "r") as file:
                df = pd.read_csv(file)
                print(df)
        except FileNotFoundError as e:
            print(e)


