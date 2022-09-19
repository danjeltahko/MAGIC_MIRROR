from bs4 import BeautifulSoup
from config import *
import time
import requests


def getBasicMovie(URL):

    response = requests.request('GET', URL)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    new_movie = BASIC.copy()

    try:

        try:
            # Gets Original title if there is one
            new_movie['title'] = soup.find('div', {'class' : "sc-dae4a1bc-0 gwBsXc"}).get_text().split(': ')[1]
        except AttributeError as e:
            # Gets Title
            new_movie['title'] = soup.find('h1', {'class' : "sc-b73cd867-0 eKrKux"}).get_text() 
        
        try:
            # Gets movie rating /10
            rating = soup.find('span', {'class' : "sc-7ab21ed2-1 jGRxWM"}).get_text()
            new_movie['rating'] = rating + "/10"
        except AttributeError:
                print(f"Could not retrive rating from {new_movie['title']}\nURL = {URL}" )

        """
        # Print movie 
        for i in new_movie:
            print(new_movie[i])
        """ 

        return new_movie
       
    except AttributeError as movie_error:
        print(f"Scraping object again : {movie_error}")
        time.sleep(2)
        getBasicMovie(URL)


def getMovie(URL):

    response = requests.request('GET', URL)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    new_movie = MOVIE.copy()

    try:

        try:
            # Gets Original title if there is one
            new_movie['title'] = soup.find('div', {'class' : "sc-dae4a1bc-0 gwBsXc"}).get_text().split(': ')[1]
        except AttributeError as e:
            print(f"No original title : {e}")
            # Gets Title
            new_movie['title'] = soup.find('h1', {'class' : "sc-b73cd867-0 eKrKux"}).get_text() 

        """
        # TV Movie - 1983 - PG - 1h
        try:
            # Get type movie, tv series etc
            new_movie['type'] = list(soup.find('ul', {'class' : "ipc-inline-list ipc-inline-list--show-dividers sc-8c396aa2-0 kqWovI baseAlt"}))[0].get_text()
        except AttributeError as e:
            print(f"No type found : {e}")
            new_movie['type'] = "Movie"
        # Gets year movie was made
        new_movie['year'] = list(soup.find('ul', {'class' : "ipc-inline-list ipc-inline-list--show-dividers sc-8c396aa2-0 kqWovI baseAlt"}))[0].find('span').get_text()
        # Gets age rating for movie
        new_movie['age_rating'] = list(soup.find('ul', {'class' : "ipc-inline-list ipc-inline-list--show-dividers sc-8c396aa2-0 kqWovI baseAlt"}))[1].find('span').get_text()
        # Gets movie length
        new_movie['length'] = list(soup.find('ul', {'class' : "ipc-inline-list ipc-inline-list--show-dividers sc-8c396aa2-0 kqWovI baseAlt"}))[2].get_text()
        """


        # Gets movie rating /10
        new_movie['rating'] = soup.find('span', {'class' : "sc-7ab21ed2-1 jGRxWM"}).get_text()
         # Gets every genre
        new_movie['genre'] = [genre.get_text() for genre in list(soup.find_all('span', {'class' : "ipc-chip__text"}))][:-1]
        # Gets description for movie
        new_movie['description'] = soup.find('span', {'class' : "sc-16ede01-0 fMPjMP"}).get_text()
        
    
        # Print movie 
        for i in new_movie:
            print(new_movie[i])
        
    except AttributeError as movie_error:
        print(f"Scraping object again : {movie_error}")
        time.sleep(2)
        getMovie(URL)

if __name__ == "__main__":
    SER = "https://www.imdb.com/title/tt0251504/?ref_=nm_flmg_dr_1"
    MOV = "https://www.imdb.com/title/tt0080846/?ref_=nm_flmg_dr_17"
    getBasicMovie(SER)
    print("\n")
    getBasicMovie(MOV)