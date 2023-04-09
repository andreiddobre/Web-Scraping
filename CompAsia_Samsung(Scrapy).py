#pip install scrapy
#pip install crochet

#import necesary libraries
import scrapy
from scrapy.crawler import CrawlerRunner
from crochet import setup
setup()
import requests
from scrapy.http import TextResponse

#requesting the website to be scrap which is Compasia.com
r=requests.get("https://shop.compasia.com/collections/samsung")

#extracting the Data and put in a Dataframe
response = TextResponse(r.url, body=r.text, encoding='utf-8')

name = response.css('.product-item__info > div > a::text').extract()
price = response.css('.product-item__info > div > div > span > span:nth-child(2)::text ').extract()
URL = response.css('.product-item__info > div > a::attr(href)').extract()
discount = response.css('.product-item__label-list > span> span >span::text').extract()

import pandas as pd
df = pd.DataFrame(list(zip(name, price, discount, URL, )), columns=['Product Name', 'Price', 'Discount', 'Link'])
print('Dataframe (original): \n', df)

#do some data cleaning for the extracted data
#extend the product's link 
df['Link'] = df['Link'].apply(lambda x: 'https://shop.compasia.com/collections/samsung' + x)
print('Dataframe (clean): \n', df)

#export the dataframe to csv file
df.to_csv('CompAsia_SamsungProducts.csv', index = False)

#original code inspired by https://github.com/drshahizan
