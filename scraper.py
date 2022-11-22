import requests
from bs4 import BeautifulSoup
import re
import csv


url = 'https://www.imdb.com/search/title/?genres=fantasy&explore=title_type,genres'
page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')
# print(soup.get_text())
titles = soup.findAll(href=re.compile('/title/tt'))
# titles = soup.findAll('a')
# print(titles)
title_list = []
for title in titles :
   title_list.append(re.sub(r'\n\s*\n' , r'\n\n', title.get_text().strip() , flags = re.M))

condensed_list = []
for title in title_list :
    if len(title) > 2:
        condensed_list.append(title)

# print(condensed_list)

years = soup.findAll('span' , attrs={'class' : 'lister-item-year text-muted unbold'})
year_list = []
for year in years :
    year_list.append(re.sub(r'\n\s*\n' , r'\n\n', year.get_text().strip(), flags = re.M))



ratings = soup.findAll('div' , attrs={'class' : 'inline-block ratings-imdb-rating'})
rating_list = []
for rating in ratings :
    rating_list.append(re.sub(r'\n\s*\n' , r'\n\n', rating.get_text().strip() , flags = re.M))




file = open('imdb.csv' , 'w')
writer = csv.writer(file)

writer.writerow(['Title' , 'Year' , 'Rating'])

for title , year , rating in zip(condensed_list , year_list , rating_list) :
    writer.writerow([title, year, rating])

file.close()

default_url = 'https://www.imdb.com'

def get_next_page() :
    