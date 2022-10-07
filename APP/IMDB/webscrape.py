from tabulate import tabulate
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import csv

from config import *
from settings import *


class SCRAPE:

    """
    Available functions!
    --------------------
    * scrape_person
    * scrape_title
    * chart_box_office
    * chart_most_popular_movies

    """

    def __init__(self) -> None:
        self.filter = FILTER

    def scrape_person(self, person_url):

        # general setup for html page
        response = requests.request('GET', person_url, headers=HEADERS)
        html = response.text 
        soup = BeautifulSoup(html, 'html.parser')
        person_dict = {}

        # name of person we are scraping
        name_person = soup.find('h1').get_text().strip()

        # get every category in filmography and save in array
        div = soup.find('div', {'id': 'jumpto'}).find_all('a')
        category = [str(c.get_text()).lower() for c in div]

        # get first div category of Filmography, ex 'director'
        div_category = soup.find('div', {'class': 'filmo-category-section'})
        for index in range(len(category)):
            # if category in filter, else loop next category
            if category[index] in self.filter:
                # finding every movie and so on in this category & print progress bar
                for cat in tqdm(div_category.find_all('b'), desc=category[index]):
                    # if title name in dictionary add this category to dictionary
                    if cat.text in person_dict:
                        person_dict[cat.text]['Category'].append(category[index])
                    else:
                        # get url to movie and return dictionary with info about movie
                        movie_dict = self.scrape_title(f"https://www.imdb.com{cat.find('a')['href']}")
                        # add movie dictionary to title
                        person_dict[cat.text] = movie_dict
                        # add category to category key
                        person_dict[cat.text]['Category'] = [category[index]]
                        #print(f"{cat.text} : {person_dict[cat.text]}\n")
                print("\n")

            # change to next div category in Filmography, ex 'writer'
            div_category = div_category.find_next('div', {'class': 'filmo-category-section'})

        print("\n------------------")
        self.write_to_csv(person_dict, name_person)
        print("------------------")

    def scrape_title(self, title_url):
        
        # general setup
        response = requests.request('GET', title_url, headers=HEADERS)
        html = response.text 
        soup = BeautifulSoup(html, 'html.parser')

        # title dictionary init
        title_dict = {
            'Category': None,
            'Rating': None,
            'Year': None,
            'Length': None,
            'Type': None,
            'Age': None,
            'Genre': None,
            'URL': title_url
        }

        try:
            # Gets movie rating /10
            rating = soup.find('span', {'class' : "sc-7ab21ed2-1 jGRxWM"}).get_text()
            title_dict['Rating'] = float(rating) 
        except AttributeError:
            title_dict['Rating'] = "-"

        try:
            # Gets every genre
            title_dict['Genre'] = [genre.get_text() for genre in list(soup.find_all('span', {'class' : "ipc-chip__text"}))][:-1]
        except AttributeError:
            title_dict['Genre'] = "-"

        
        lu = soup.find('ul', {'class' : "ipc-inline-list ipc-inline-list--show-dividers sc-8c396aa2-0 kqWovI baseAlt"})
        # get array of info = ['TV Series', '2021– ', '15+', '1h']
        for i in lu.find_all('li'):
            span = i.find('span')
            info = ""
            # some attributes can only be found with span tag
            if span:
                info = span.get_text().strip()
            else:
                info = i.get_text().strip()
            # sometimes there is only length or type, so to pair values with right key
            if info in AGE:
                title_dict['Age'] = info
            elif info in TYPE:
                title_dict['Type'] = info
            elif 'h' in info or 'm' in info:
                title_dict['Length'] = info
            else:
                title_dict['Year'] = info
        if title_dict['Type'] == None:
            title_dict['Type'] = 'Movie' 

        return title_dict

    def write_to_csv(self, dic, name):
        csv_filepath = f"csv/{name}_imdb.csv"
        try:
            with open(csv_filepath, 'w') as file:
                writer = csv.DictWriter(file, CSV_HEADER)
                writer.writeheader()
                for k in dic:
                    temp_dict = {'Title': k}
                    for i in dic[k]:
                        temp_dict[i] = dic[k][i]
                    writer.writerow(temp_dict)
            print(f"* Successfully wrote {name} to file!!")
        except FileNotFoundError:
            print("* Could not write to file, make sure your csv folder is in same folder as main")

    def chart_box_office(self):

        # general setup 
        boxoffice_url = "https://www.imdb.com/chart/boxoffice"
        response = requests.request('GET', boxoffice_url)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        topic = soup.find("h1").text
        time_span = soup.find("h4").text

        data = []
        head = ["Title", "Weekend", "Gross", "Weeks"]

        title = [t.text.strip() for t in soup.select("td.titleColumn")]
        weekend = [w.text.strip() for i, w in enumerate(soup.select("td.ratingColumn")) if i % 2 == 0 ]
        gross = [g.text.strip() for g in soup.select("span.secondaryInfo")]
        weeks = [ws.text.strip() for ws in soup.select("td.weeksColumn")]

        for i in range(len(weekend)):
            temp_list = []
            temp_list.append(title[i])
            temp_list.append(weekend[i])
            temp_list.append(gross[i])
            temp_list.append(weeks[i])
            data.append(temp_list)

        print(topic)
        print(time_span)
        print(tabulate(data, headers=head, tablefmt="grid"))

    def chart_most_popular_movies(self):

        """
        * Most popular movies on IMDb

            As determined by IMDb Users
        """

        # general setup 
        popular_movies = "https://www.imdb.com/chart/moviemeter"
        response = requests.request('GET', popular_movies)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        topic = soup.find("h1").text
  
        data = []
        head = ["Rank", "Title", "Rating", "Progress", "Year"]

        rank = [rk.attrs.get('data-value') for rk in soup.select('td.posterColumn span[name=rk]')]
        rating = [r.attrs.get('data-value') for r in soup.select('td.posterColumn span[name=ir]')]
        movie = [title for title in soup.select('td.titleColumn')]

    
        for i in range(len(movie)):

            title = movie[i].find('a').text
            year_div = movie[i].find('span')
            year = year_div.text[1:-1]
            prog = year_div.find_next('span').text[1:-1].strip()
        
            if movie[i].find('span', {'class' : 'global-sprite titlemeter up'}):
                prog = "+" + prog
            elif movie[i].find('span', {'class' : 'global-sprite titlemeter down'}):
                prog = "-" + prog

            temp_list = []
            temp_list.append(rank[i])
            temp_list.append(title)
            temp_list.append(rating[i])
            temp_list.append(prog)
            temp_list.append(year)

            data.append(temp_list)
    
    
        print(topic)
        print(tabulate(data, headers=head, tablefmt="grid"))


  










