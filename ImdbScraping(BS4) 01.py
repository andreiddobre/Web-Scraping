#pip install bs4

import bs4
import requests
import time
import random as ran
import sys
import pandas as pd

#Top Box Office (US) - Released between 2018-01-01 and 2022-12-31 (Sorted by US Box Office Descending)
#scrape results from the first page
url = 'https://www.imdb.com/search/title/?release_date=2018-01-01,2022-12-31&sort=boxoffice_gross_us,desc&start='

#extract all data
source = requests.get(url).text
soup = bs4.BeautifulSoup(source,'html.parser')

#below code is run only to extract movie information on it
movie_blocks = soup.findAll('div',{'class':'lister-item-content'})

#inspect the data of the extracted movie block to identify the elements that we need to scrape
mname = movie_blocks[0].find('a').get_text()        #name of the movie
m_reyear = int(movie_blocks[0].find('span',{'class': 'lister-item-year'}).contents[0][1:-1])                    #release year
m_rating = float(movie_blocks[0].find('div',{'class':'inline-block ratings-imdb-rating'}).get('data-value'))    #rating
m_mscore = float(movie_blocks[0].find('span',{'class':'metascore favorable'}).contents[0].strip())              #meta score
m_votes = int(movie_blocks[0].find('span',{'name':'nv'}).get('data-value'))                                     #votes

print("Movie Name: " + mname,
      "\nRelease Year: " + str(m_reyear),
      "\nIMDb Rating: " + str(m_rating),
      "\nMeta score: " + str(m_mscore),
      "\nVotes: " + '{:,}'.format(m_votes)
      ) #note to self: trying to add gross value

#function to extract targeted elements from a movie block
def scrape_mblock(movie_block):
    movieb_data ={} 
    try:
        movieb_data['Name'] = movie_block.find('a').get_text() #name of the movie
    except:
        movieb_data['Name'] = None
    try:    
        movieb_data['Year'] = str(movie_block.find('span',{'class': 'lister-item-year'}).contents[0][1:-1]) #release year
    except:
        movieb_data['Year'] = None
    try:
        movieb_data['Rating'] = float(movie_block.find('div',{'class':'inline-block ratings-imdb-rating'}).get('data-value')) #rating
    except:
        movieb_data['Rating'] = None    
    try:
        movieb_data['M_score'] = float(movie_block.find('span',{'class':'metascore favorable'}).contents[0].strip()) #meta score
    except:
        movieb_data['M_score'] = None
    try:
        movieb_data['Votes'] = int(movie_block.find('span',{'name':'nv'}).get('data-value')) #votes
    except:
        movieb_data['Votes'] = None
    return movieb_data #note to self: trying to add gross value

#scrape all movie blocks within a single search result page
def scrape_m_page(movie_blocks):    
    page_movie_data = []
    num_blocks = len(movie_blocks)    
    for block in range(num_blocks):
        page_movie_data.append(scrape_mblock(movie_blocks[block]))    
    return page_movie_data

#iterate the above made function through all pages of the search result untill we scrape data for the targeted number of movies
def scrape_this(link,t_count):    
    #from IPython.core.debugger import set_trace

    base_url = link
    target = t_count
    
    current_mcount_start = 0
    current_mcount_end = 0
    remaining_mcount = target - current_mcount_end 
    
    new_page_number = 1    
    movie_data = []
        
    while remaining_mcount > 0:
        url = base_url + str(new_page_number)       
        #set_trace()       
        source = requests.get(url).text
        soup = bs4.BeautifulSoup(source,'html.parser')        
        movie_blocks = soup.findAll('div',{'class':'lister-item-content'})        
        movie_data.extend(scrape_m_page(movie_blocks))          
        current_mcount_start = int(soup.find("div", {"class":"nav"}).find("div", {"class": "desc"}).contents[1].get_text().split("-")[0])
        current_mcount_end = int(soup.find("div", {"class":"nav"}).find("div", {"class": "desc"}).contents[1].get_text().split("-")[1].split(" ")[0])
        remaining_mcount = target - current_mcount_end        
        print('\r' + "\ncurrently scraping movies from: " + str(current_mcount_start) + " - "+str(current_mcount_end), "| remaining count: " + str(remaining_mcount), flush=True, end ="")        
        new_page_number = current_mcount_end + 1        
        time.sleep(ran.randint(0, 10))    
    return movie_data

base_scraping_link = "https://www.imdb.com/search/title/?release_date=2018-01-01,2022-12-31&sort=boxoffice_gross_us,desc&start="

top_movies = 150 #input("How many movies do you want to scrape?")
films = []

movies = scrape_this(base_scraping_link,int(top_movies))

print('\r'+"\nList of top " + str(top_movies) +" movies:" + "\n", end="\n")
movies=pd.DataFrame(movies)
print('List of the top 150 movies: \n', movies)

movies.to_csv('Imdb_scraped_movies.csv', index=False)

#original source code by https://www.kaggle.com
