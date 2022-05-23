# Import modules
import requests
from bs4 import BeautifulSoup
import os
from fake_useragent import UserAgent
import PySimpleGUI as sg
import random

sg.theme(random.choice(sg.theme_list()))

layout = [[sg.Text('Input your link here')],
          [sg.Input(key='link')],
          [sg.Button('Check'), sg.Button('Exit')]]

window = sg.Window('WallPaperCave Manager', layout)

while True:
    event, values = window.read()
#   print(event, values)

    if event in (None, 'Exit', 'Cancel', 'Exit!'):
        break

    if event == 'Check':
        try:
            responce = requests.get(values['link'], headers={'User-Agent': UserAgent().chrome}).text
            soup = BeautifulSoup(responce, 'lxml')
            name = str(soup.find_all('h1')[1])[4:-5]
            images = soup.find_all('div', class_='wallpaper')
            count = len(images)

            window.extend_layout(window, [[sg.Text(f'The album {name} with {count} wallpapers was discovered.')],
                                          [sg.Button('Continue'), sg.Button('Cancel')]])
        except:
            print('Incorrect link address!! Try again')

    if event == 'Continue':
        try:
            if not os.path.exists('wallpapers'):
                os.mkdir('wallpapers')
            if not os.path.exists(f'wallpapers/{name}'):
                os.mkdir(f'wallpapers/{name}')

            window.extend_layout(window, [[sg.Col([[sg.T('Logs')]], scrollable=True, key='logs', s=(200, 200))]])

            n = 0
            for image in images:
                n += 1
                download = image.find('a', class_='download').get('href')
                final = 'https://wallpapercave.com' + download
                r = requests.get(final, headers={'User-Agent': UserAgent().chrome}, allow_redirects=True)
                open(f'wallpapers/{name}/{n}.jpg', 'wb').write(r.content)
                window.extend_layout(window['logs'], [[sg.Text(f'№{n} is downloaded')]])
                window.visibility_changed()
                window['logs'].contents_changed()

            window.extend_layout(window, [[sg.Text('The album was succesfully downloaded!!')], [sg.Button('Exit!')]])
        except:
            print('Unknown Error')

window.close()
