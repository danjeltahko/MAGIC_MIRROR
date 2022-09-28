from math import prod
from readline import write_history_file
from bs4 import BeautifulSoup
from config import *
from movie import *
import requests

class IMDB:

    def __init__(self) -> None:
        self.director_list = []
        self.writer_list = []
        self.producer_list = []
        self.actor_list = []

    def start(self, URL):
        
        response = requests.request("GET", URL)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        # Saves every directed movie in list director_list with title and rating
        div_director = soup.find('div', {'class': 'filmo-category-section'})
        for directed in div_director.find_all('b'):
            url_link = f"https://www.imdb.com{directed.find('a')['href']}"
            new_dict = getBasicMovie(url_link)
            self.director_list.append(new_dict)

        # Saves every written movie in list writer_list with title and rating
        div_writers = div_director.find_next('div', {'class': 'filmo-category-section'})
        for written in div_writers.find_all('b'):
            url_link = f"https://www.imdb.com{written.find('a')['href']}"
            new_dict = getBasicMovie(url_link)
            self.writer_list.append(new_dict)

        # Saves every produced movie in list producer_list with title and rating
        div_producer = div_writers.find_next('div', {'class': 'filmo-category-section'})
        for produced in div_producer.find_all('b'):
            url_link = f"https://www.imdb.com{produced.find('a')['href']}"
            new_dict = getBasicMovie(url_link)
            self.producer_list.append(new_dict)

     

    def calculate(self):
        
        full_list = []

        for ob in self.director_list:
            new_dict = {}
            new_dict['title'] = ob['title']
            new_dict['rating'] = ob['rating']
            new_dict['director'] = True
            for a in self.writer_list:
                if a['title'] == ob['title']:
                    a.pop('title')
                    new_dict['writer'] = True

            for b in self.producer_list:
                if b['title'] == ob['title']:
                    b.pop('title')
                    new_dict['producer'] = True

            full_list.append(new_dict)

        
        for i in full_list:
            print(i)

        


        """
        tile | rating | dir | wri | pro |
        """
    

if __name__ == "__main__":
    imdb = IMDB()
    imdb.start("https://www.imdb.com/name/nm0545169/?ref_=tt_cl_dr_1")
    imdb.calculate()
