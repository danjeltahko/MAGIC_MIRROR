import requests
import json
from API.api_keys import TRAKT_KEY

# https://trakt.docs.apiary.io/#introduction/extended-info

class Trakt:

    def __init__(self) -> None:
        self.api_url = "https://api.trakt.tv/"
        self.header = {
            "Content-type": "application/json",
            "trakt-api-key": TRAKT_KEY,
            "trakt-api-version": "2"
        }

    def get_movie(self, movie:str) -> dict:
        """#### Get movie
        Takes movie och tv show title as argument
        returns dictionary
        """
        url = self.api_url + f"search?query={movie}"
        response = requests.get(url, headers=self.header)
        print(f"response:[{response.status_code}]")
        print(response.text)
        if (response.status_code < 400):
            movie = json.loads(response.text)
            return movie
        else:
            return None


if __name__ == '__main__':
    foo = Trakt()
    print(foo.get_movie("Star Wars"))


"""
https://trakt.docs.apiary.io/#introduction/filters
query		    batman	        Search titles and descriptions.
years		    2016	        4 digit year or range of years.
genres	    ✓	action	        Genre slugs.
languages	✓	en	            2 character language code.
countries	✓	us	            2 character country code.
runtimes		30-90	        Range in minutes.
studios	    ✓	marvel-studios	Studio slugs.
"""
