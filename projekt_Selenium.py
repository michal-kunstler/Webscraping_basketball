from asyncore import loop
from selenium import webdriver
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import getpass
import datetime
import pandas as pd

limit_100 = False

mypath = '/Users/mkunstler/Desktop/WNE/WS/projekt/projekt_Selenium.py' #path to the location of the project
# Init:
gecko_path = '/opt/homebrew/bin/geckodriver'  #path to the location of the geckodriver
ser = Service(gecko_path)
options = webdriver.firefox.options.Options()
options.headless = False
driver = webdriver.Firefox(options = options, service=ser) #defining our webdriver

d = pd.DataFrame({'name':[], 'games':[], 'points':[], 'total_rebounds':[], 'assists':[], "physical":[]})
#simiralry as in the beautiful soup - we create a dataframe from a dictionary where the players stats will be stored

url = 'https://www.basketball-reference.com/leagues/NBA_2022_per_game.html' #the url link to the main page on which we will be scraping

driver.get(url) #opening the url with the webdriver
time.sleep(2) #waiting 2 seconds
try:
    cookies = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/button[1]/span') #confirmation of the cookies
    cookies.click() #"clocking" on the cookies terms
    time.sleep(2)  #waiting 2 seconds
except:
    pass

links = [] #creating a empty list
for i in range(1, 843):  #loop on the Xpaths list of players and getting the inforamtion which is of our interest
#beacuse the Xpaths of every another player look as below, we iteratively clisk on the Xpath looping on the "tr[i]" consecutively
#/html/body/div[3]/div[5]/div[3]/div[3]/table/tbody/tr[1]/td[1]/a
#/html/body/div[3]/div[5]/div[3]/div[3]/table/tbody/tr[2]/td[1]/a
#/html/body/div[3]/div[5]/div[3]/div[3]/table/tbody/tr[3]/td[1]/a

    str_path = '/html/body/div[3]/div[5]/div[3]/div[2]/table/tbody/tr[' + str(i) + ']/td[1]/a' #our loop
    try:
        player = driver.find_element(By.XPATH, str_path).get_attribute('href') #geting the atribute and appending the link list of all the players
        links.append(player)
    except:
        continue

links = list(set(links)) #creating the list of sets on links with the extracted players Xpaths

if limit_100:
    lim = 101
else:
    lim = len(links)

for i in range(0, lim): #looping over the whole list of links

    driver.get(links[i]) #getting into the website
    time.sleep(2) #awaiting 2 sec for all the data to load

    try:
        name = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[1]/div[2]/h1/span').text #taking the header with the name
    except:
        name = ''
   
    try:
        games = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[4]/div[2]/div[1]/p[1]').text #taking the information of the number of played games
    except:
        games = ''
         
    try:
        points = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[4]/div[2]/div[2]/p[1]').text #taking the information of the number of points scored
    except:
        points = ''
         
    try:
        total_rebounds = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[4]/div[2]/div[3]/p[1]').text #taking the information of the number of total rebounds
    except:
        total_rebounds = ''
       
    try:
        assists = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[4]/div[2]/div[4]/p[1]').text #taking the information of the number of assists of a player
    except:
        assists = ''
         
    try:
        physical = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[1]/div[2]/p[4]').text #taking the information of the physical stats
    except:
        physical = ''

    playa = {'name':name, 'games':games, 'points':points, 'total_rebounds':total_rebounds, 'assists':assists, 'physical':physical}
   
    print(i)
    print(playa)
    d = d.append(playa, ignore_index = True) #appending the collected data
   
driver.quit() #quitting the webdriver
