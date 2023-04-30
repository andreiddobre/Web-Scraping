from bs4 import BeautifulSoup
import requests

#the website URL
url_link = "https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States"
result = requests.get(url_link).text
doc = BeautifulSoup(result, "html.parser")
print('Prettify results: \n', doc.prettify())

#find elements by ID
res = doc.find(id = "content")
print('Find by ID resuslts: \n', res)

#find elements by class name
heading = res.find(class_ = "firstHeading")
print('Find by class name results: \n', heading)

#extracting text from  html element
print('Extracting text: Heading \n', heading.txt)

#accesing the nested tag
res = doc.find(id = "content")
for ele in res:
  print('Find h2 results: \n', res.find("h2"))

#searching using string
res = doc.find_all(text = "California")
print('Searching string California: \n', res)

#search by passing a list
res=doc.find_all(['a', 'p', 'div'])
print('Searching by passing a list: \n', res)

#search by passing a regular expression
import re
for str in doc.find_all(text = re.compile("1788")):
  print('Regular expression results: \n', str)

#search by passing a regular expression  with limited number of results
for str in doc.find_all(text = re.compile("1788"), limit = 2): print('Regular expression results (limit = 2): \n', str)

#search using css selectors
print('Using CSS selectors :\n', doc.select(".vector-menu-content"))

#find tags by ID
print('Finding tags by ID', doc.select("#p-logo"))
print('Finding tags by ID', doc.select("div#mw-panel"))

#testing if the atribute exists in a tag
print('Testing if the atribute exists in a tag', doc.select("footer[role]"))
print('Testing if the atribute exists in a tag', doc.select("a[href]"))

