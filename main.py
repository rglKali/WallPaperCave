import requests
from bs4 import BeautifulSoup
import os
from fake_useragent import UserAgent


site = 'https://wallpapercave.com'
link = input('Album link - ')


responce = requests.get(link, headers={'User-Agent': UserAgent().chrome}).text
#open('site.html', 'w', encoding='utf-8').write(responce)
soup = BeautifulSoup(responce, 'lxml')
name = soup.find_all('h1')
folder = str(name[1])[4:-5]

if not os.path.exists('wallpapers'):
    os.mkdir('wallpapers')
if not os.path.exists(f'wallpapers/{folder}'):
    os.mkdir(f'wallpapers/{folder}')

images = soup.find_all('div', class_='wallpaper')

n = 0
for image in images:
    n += 1
    download = image.find('a', class_='download').get('href')
    final = site + download
    r = requests.get(final, headers={'User-Agent': UserAgent().chrome}, allow_redirects=True)
    open(f'wallpapers/{folder}/{n}.jpg', 'wb').write(r.content)
    print(f'№ {n} is OK')