#pip install scrapy
#pip install crochet

#import necesary libraries
import scrapy
from scrapy.crawler import CrawlerRunner
from crochet import setup
setup()
import requests
from scrapy.http import TextResponse

#requesting the website to be scrap which is bookdepository.com
r=requests.get("https://www.bookdepository.com/search?searchTerm=big+data&search=Find+book")

#extracting the Data and put in a Dataframe
response = TextResponse(r.url, body=r.text, encoding='utf-8')

#use CSS selector to find HTML elements in response variable and extract the selected information
#the title, author, published date, format and price of the books are extracted and stored in different lists
title = response.css('.item-info > h3 > a::text').extract()
author = response.css('.item-info > .author > span > a > span::text').extract()
published = response.css('.item-info > .published::text').extract()
format = response.css('.item-info > .format::text').extract()
price = response.css('.item-info > .price-wrap > .price > span::text').extract()
     
#all the lists above are combined and converted to pandas dataframe
import pandas as pd
df = pd.DataFrame(list(zip(title, author, published, format, price)), columns=['Title','Author', 'Published date', 'Foramt', 'Price'])
print('Dataframe (original): \n', df)

#performing some cleaning process on the extracted data
# remove leading and trailing whitespace in string
for col in df.columns:
  df[col] = df[col].str.strip()

#remove US$ from price column
df['Price'] = df['Price'].str.replace('US$','', regex=False)

#parse string to date
df['Published date'] = pd.to_datetime(df['Published date'], format='%d %b %Y')
print('Dataframe (clean data): \n', df)

#export the cleaned data to a csv file
df.to_csv('BookDepository_big_data_books.csv', index = False)


#original code inspired by https://github.com/drshahizan
