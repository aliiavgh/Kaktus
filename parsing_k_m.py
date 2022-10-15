import requests
from bs4 import BeautifulSoup as BS
import csv

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
            time = point.find('div', class_='ArticleItem--time').text
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
            'time':time,
            'title':title, 
            'image':image
        })

        write_txt(title + '\n')
        # write_csv([[time], [title], [image]])
        
        
def write_csv(data):
    with open('news.csv', 'a') as file: 
        names = ['time', 'title', 'image']
        write = csv.DictWriter(file, delimiter='/', fieldnames=names)
        write.writerow(data)

def write_txt(data):
    with open('news.txt', 'a') as file:
        file.writelines(data)


def main():
    BASE_URL = 'https://kaktus.media/?lable=8&date=2022-10-14&order=time'
    html = get_html(BASE_URL)
    soup = get_soup(html)
    get_data(soup)
    

if __name__ == '__main__':
    main()