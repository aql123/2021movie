# 引用库
import os
import re
import time

import requests
from bs4 import BeautifulSoup
from django.core.wsgi import get_wsgi_application

# sys.path.extend(['D:\\github\\movie-recommendation-system\\python-django\\movieSystem', ])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movierecomend.settings")
application = get_wsgi_application()
import django

django.setup()
from movie.models import *

count = 0
# 设置headers
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}

# 设置url
urls = set('https://movie.douban.com/top250?start={}'.format(str(i)) for i in range(0, 250, 25))

page_count = 0


# 获得url的电影
def get_url_movie():
    global page_count
    while urls:
        url = urls.pop()
        page_count += 1
        print('fetch url', url, page_count)
        payload = {'filter': ''}
        response = requests.get(url, headers=headers, params=payload)
        soup = BeautifulSoup(response.text, 'lxml')
        movie_hrefs = soup.select('div.pic > a')
        for movie_href in movie_hrefs:
            print('fetch movie href', movie_href)
            get_info_movie(movie_href['href'])
        time.sleep(2)


def save_images(link, name):
    res = requests.get(url=link, headers=headers)
    if res.status_code != 200:
        raise IOError("code not 200")
    image_name = '../movie_images/' + name + '.png'
    print(image_name)
    with open(image_name, 'wb') as opener:
        opener.write(res.content)
    # print('image success', image_name)


# 获得电影详情
def get_info_movie(url):
    global count
    count += 1
    print('count')
    response = requests.get(url, headers=headers)
    if (response.status_code != 404):
        soup = BeautifulSoup(response.text, 'lxml')
        name = soup.select('div#content > h1 > span')[0].get_text()
        tags = [tag.text.strip() for tag in soup.find_all('span', {'property': 'v:genre'})]
        brief = soup.find_all("span", attrs={"property": "v:summary"})[0].get_text().strip()
        rate = soup.find_all("strong", attrs={"property": "v:average"})[0].get_text()
        link = re.findall('<span class="pl">IMDb链接:</span>[^"]*"(.*?)"', response.text, re.S)[0]
        img = soup.find_all("img", attrs={"rel": "v:image"})[0]['src']
        years = soup.find_all("span", attrs={"property": "v:initialReleaseDate"})[0].get_text()
        # type_str = '/'.join(genre.text for genre in soup.findAll('span',property='v:genre'))
        # print(name, brief, rate, link, img, years)
        film, created = Film.objects.get_or_create(
            name=name, defaults={
                'brief': brief,
                'rate': rate,
                'link': link,
                'img': name,
                "years": years
            }
        )
        if created:

            print("插入电影成功！")
            save_images(img, name)
        else:
            print('movie exists')
        for tag in tags:
            tags, created = Genres.objects.get_or_create(name=tag)
            if created:
                print('tag create success', created)
            film.tags.add(tags)


if __name__ == '__main__':
    get_url_movie()
