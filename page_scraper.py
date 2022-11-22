import requests
from bs4 import BeautifulSoup
import re
import csv


default_url = 'https://www.imdb.com'
full_url = 'https://www.imdb.com/search/title/?genres=fantasy&explore=title_type,genres'

def scrape_page(url ,  title_list = [] , year_list = [] , rating_list = []) :
    print(len(title_list))
    if len(title_list) >= 1000 :
        file = open('imdb.csv' , 'w')
        writer = csv.writer(file)
        writer.writerow(['Title' , 'Year' , 'Rating'])
        for title, year, rating in zip(title_list, year_list , rating_list) :
            writer.writerow([title , year, rating])
        file.close()
        return
    page = requests.get(url)
    soup = BeautifulSoup(page.text , 'html.parser')
    # titles = soup.findAll(href=re.compile('/title/tt'))
    titles = soup.findAll('img', attrs={'height':'98'})
    
    for title in titles :
        title_list.append(title['alt'])
        
    
    years = soup.findAll('span' , attrs={'class' : 'lister-item-year text-muted unbold'})
    ratings = soup.findAll('div' , attrs={'class' : 'inline-block ratings-imdb-rating'})

    # for title in test_titles :
    #     title_holder.append(re.sub(r'\n\s*\n' , r'\n\n', title.get_text().strip() , flags = re.M))
    
    # for title in title_holder :
    #     if len(title) > 2 :
    #         title_list.append(title)
    
    for year in years :
        year_list.append(re.sub(r'\n\s*\n' , r'\n\n', year.get_text().strip(), flags = re.M))
    
    for rating in ratings :
        rating_list.append(re.sub(r'\n\s*\n' , r'\n\n', rating.get_text().strip() , flags = re.M))

    try:
        next_page = soup.find('div' , attrs = {'class' : 'desc'}).find('a', attrs = {'class' : 'lister-page-next next-page'})['href']
        if next_page :
            next_url = default_url + next_page + '&ref_=adv_nxt'
            scrape_page(next_url , title_list , year_list , rating_list)
    except Exception as e:
        print(e)
        return 
        



