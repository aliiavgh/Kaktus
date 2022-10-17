from tkinter import image_names
import requests
from bs4 import BeautifulSoup as BS
import csv
import datetime 

def get_html(url): 
    response = requests.get(url)
    return response.text

def get_soup(html):
    soup = BS(html, 'lxml')
    return soup

def get_data(soup):
    all_news = soup.find('div', class_='Tag--articles')
    news = all_news.find_all('div', class_='ArticleItem--data ArticleItem--data--withImage')
    for point in news: 
        try: 
            time = point.find('div', class_='ArticleItem--time').text.strip()
        except:
            time = ''
        try: 
            title = point.find('a', class_='ArticleItem--name').text.strip()
        except: 
            title = ''
        try:
            image = point.find('img', class_='ArticleItem--image-img').get('src')
        except:
            image = ''
        
        write_csv({
            'time': time,
            'title': title, 
            'image': image
        })
        
        write_txt(title + '\n')
        

def write_csv(data):
    with open('news.csv', 'a', newline='') as file: 
        names = ['time', 'title', 'image']
        write = csv.DictWriter(file, delimiter=';', fieldnames=names)
        write.writerow(data)

def write_txt(data):
    with open('titles.txt', 'a') as file:
        file.writelines(data)


def main():
    f1 = open('news.csv', 'w')
    f1.close()
    f2 = open('title.txt', 'w')
    f2.close()
    date = datetime.date.today()
    BASE_URL = f'https://kaktus.media/?lable=8&date={date}&order=time'
    html = get_html(BASE_URL)
    soup = get_soup(html)
    get_data(soup)
