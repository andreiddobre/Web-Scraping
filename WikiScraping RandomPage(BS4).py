#pip install bs4
#pip install requests

from bs4 import BeautifulSoup
import requests

#trying to open a random wikipedia article
#'Special: Random' function opens random articles
res = requests.get("https://en.wikipedia.org/wiki/Special:Random")
res.raise_for_status()

#if not installed, pip install htmlparser
wiki = BeautifulSoup(res.text, "html.parser")
r = open("Random_wiki_article.txt", "w+", encoding='utf-8')

# Adding the heading to the text file
heading = wiki.find("h1").text
r.write(heading + "\n")
for i in wiki.select("p"):
    # Optional Printing of text
    # print(i.getText())
    r.write(i.getText())

r.close()
print("File Saved as Random_wiki_article.txt")

#original code inspired by: clcoding



