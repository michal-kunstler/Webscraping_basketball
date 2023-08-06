import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from urllib import request
from bs4 import BeautifulSoup as BS
import re
import pandas as pd
import requests

limit_100 = False

# Look at the page and the code
url = 'https://www.basketball-reference.com/leagues/NBA_2022_per_game.html' #our page that we want to scrap
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
bs = BS(response.content, 'html.parser')

tags = bs.find_all('a', {'href':re.compile('/players/.*')}) #looking for the hrefs containing "/players/"

links = ['https://www.basketball-reference.com/' + tag['href'] for tag in tags] #mearging the main domain with the extracted tags
links = list(set(links))
   
d = pd.DataFrame({'name':[], 'games':[], 'points':[], 'total_rebounds':[], 'assists':[], "physical":[]}) #creating a dataframe from a dictionary where the stats will be gathered

if limit_100:
    lim = 101
else:
    lim = len(links)

for link in range(0,lim): #loop on every extracted likn which is searching for exact hrefs and getting the inforamtion which is of our interest
    url = links[link]
    html = request.urlopen(url)
    bs = BS(html.read(), 'html.parser')
   
    try:
        name = bs.find('h1').find('span').text #trying to take the header with the name of the player
    except:
        name = ''
   
    try:
        games = bs.find('span',{"data-tip":"Games"}).next_sibling.text #trying to take the span with the number of games played
    except:
        games = ''
       
    try:
        points = bs.find('span',{"data-tip":"Points"}).next_sibling.text #trying to take the span with the number of points collected
    except:
        points = ''
       
    try:
        total_rebounds = bs.find('span',{"data-tip":"Total Rebounds"}).next_sibling.text #trying to take the span with the number of total rebounds of a player
    except:
        total_rebounds = ''
     
    try:
        assists = bs.find('span',{"data-tip":"Assists"}).next_sibling.text #trying to take the span with the number of assists of a player
    except:
        assists = ''
       
    try:
        physical = bs.find('h1').parent.find('span', string = re.compile(".*lb")).parent.text #trying to take the span with the information concerning the physical information (heigth and weigth)
    except:
        physical = ''
     
    playa = {'name':name, 'games':games, 'points':points, 'total_rebounds':total_rebounds, 'assists':assists, 'physical':physical}
   
    print(link)
    d = d.append(playa, ignore_index = True) #appending gathered data to our dataframe

print(d)

d.to_csv('ws.csv', index=False,encoding='utf-8') #saving the csv with the data