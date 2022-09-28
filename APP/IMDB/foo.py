from dataclasses import field
from bs4 import BeautifulSoup
from config import *
import requests
import csv
import time


def testing():
    URL = "https://www.imdb.com/name/nm0000600/?ref_=nv_sr_srsg_0"
    response = requests.request("GET", URL)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    name_person = soup.find('h1').get_text().strip()

    print(name_person.strip())


def write_to_csv(dic, name):
    csv_filepath = f"csv/{name}_imdb.csv"
    with open(csv_filepath, 'w') as file:
        writer = csv.DictWriter(file, CSV_HEADER)
        writer.writeheader()
        for k in dic:
            temp_dict = {'Title': k}
            for i in dic[k]:
                temp_dict[i] = dic[k][i]
            writer.writerow(temp_dict)
            #temp_dic = {'Title'}
            # haha did not understand this, found on stack overflow
            #writer.writerow({field: dic[k].get(field) or k for field in CSV_HEADER})
    
def title_scrape(title_url):

    response = requests.request("GET", title_url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    title = soup.find('h1').get_text()

    # creates temp dictionary with category and will add more keys
    temp_dict = {
        'Category': None,
        'Rating': None,
        'Year': None,
        'Length': None,
        'Type': None,
        'Age': None,
        'Genre': None
        }

    try:
        # Gets movie rating /10
        rating = soup.find('span', {'class' : "sc-7ab21ed2-1 jGRxWM"}).get_text()
        temp_dict['Rating'] = rating + "/10"
    except AttributeError:
        print(f"Could not retrieve rating from {title}")

    try:
        # Gets every genre
        temp_dict['Genre'] = [genre.get_text() for genre in list(soup.find_all('span', {'class' : "ipc-chip__text"}))][:-1]
    except AttributeError:
        print(f"Could not retrieve rating from {title}")


    lu = soup.find('ul', {'class' : "ipc-inline-list ipc-inline-list--show-dividers sc-8c396aa2-0 kqWovI baseAlt"})
    # get array of info = ['TV Series', '2021– ', '15+', '1h']
    for i in lu.find_all('li'):
        span = i.find('span')
        info = ""
        if span:
            info = span.get_text().strip()
        else:
            info = i.get_text().strip()

        if info in AGE:
            temp_dict['Age'] = info
        
        elif info in TYPE:
            temp_dict['Type'] = info

        elif 'h' in info or 'm' in info:
            temp_dict['Length'] = info

        else:
            temp_dict['Year'] = info

    if temp_dict['Type'] == None:
        temp_dict['Type'] = 'Movie' 

    return temp_dict
    
def person_scrape(URL):

    start = time.time()

    # general setup for html page
    response = requests.request("GET", URL)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    # name of person we are searching
    name_person = soup.find('h1').get_text().strip()

    # get every category in filmography
    div = soup.find('div', {'id' : 'jumpto'}).find_all('a')
    category = [str(cat.get_text()).lower() for cat in div]

    imdb_dic = {}
    # get first div category of Filmography, ex 'director'
    div_category = soup.find('div', {'class': 'filmo-category-section'})
    for index in range(len(category)):
        # finding every movie and so on in category
        for cat in div_category.find_all('b'):
            # if title name in dictionary, add this category to movie
            if cat.text in imdb_dic:
                imdb_dic[cat.text]['Category'].append(category[index])
            else:
            
                # get link to movie and return dict with info about movie
                temp_dict = title_scrape(f"https://www.imdb.com{cat.find('a')['href']}")
                
                # add movie dict to title
                imdb_dic[cat.text] = temp_dict

                # add category to title
                imdb_dic[cat.text]['Category'] = [category[index]]

                print(f"{cat.text} : {imdb_dic[cat.text]}\n")

        print(f"* Done with {category[index]}")   
        # changing to text div category in Filmography, ex 'writer'
        div_category = div_category.find_next('div', {'class': 'filmo-category-section'})

    print("\n------------------")
    write_to_csv(imdb_dic, name_person)

    end = time.time()
    print("\nDONE!!\n* Total time " + str(end - start))


if __name__ == "__main__":
    _URL_ = "https://www.imdb.com/name/nm0001675/?ref_=nv_sr_srsg_1"
    person_scrape(_URL_)


"""
Change original title of movie if its in swedish....

"""