import requests
from bs4 import BeautifulSoup
import urllib.request
import os.path 

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

pageLeagueA = 'https://www.transfermarkt.com.tr/super-lig/startseite/wettbewerb/TR1'

treeLeagueA = requests.get(pageLeagueA, headers = headers)
soupLeagueA = BeautifulSoup(treeLeagueA.content, 'html.parser')

playerNames = []
playerImageLinks = []
teamNamesA = []
teamIdsA = []

for teamName in soupLeagueA.findAll('td', class_ = 'hauptlink no-border-links hide-for-small hide-for-pad'):
    if teamName.text != '':
        #print(teamName.find('a')['href'].split('/')[1])  
        teamNamesA.append(teamName.find('a')['href'].split('/')[1])
        #print(teamName.find('a')['href'].split('/')[4]) 
        teamIdsA.append(teamName.find('a')['href'].split('/')[4])

for i in range(len(teamNamesA)):
    
    playerNames.clear()
    playerImageLinks.clear()
    
    pageA = 'https://www.transfermarkt.com.tr/' + teamNamesA[i] + '/startseite/verein/' + teamIdsA[i]
    pageLoan = 'https://www.transfermarkt.com.tr/' + teamNamesA[i] + '/leihspieler/verein/' + teamIdsA[i]

    treeA = requests.get(pageA, headers = headers)
    treeLoan = requests.get(pageLoan, headers = headers)
    soupA = BeautifulSoup(treeA.content, 'html.parser')
    soupLoan = BeautifulSoup(treeLoan.content, 'html.parser')

    for playerName in soupA.findAll('img', class_ = 'bilderrahmen-fixed'):
        if playerName['title'] != '':
            #print(playerName['title'].replace(" ", "-").lower())  
            playerNames.append(playerName['title'].replace(" ", "-").lower())

    for playerName in soupLoan.findAll('img', class_ = 'bilderrahmen-fixed'):
        if playerName['title'] != '':
            #print(playerName['title'].replace(" ", "-").lower())  
            playerNames.append(playerName['title'].replace(" ", "-").lower())

    for playerImageLink in soupA.findAll('img', class_ = 'bilderrahmen-fixed'):
        #print(playerImageLink['data-src'].replace("small", "header"))
        playerImageLinks.append(playerImageLink['data-src'].replace("small", "header"))

    for playerImageLink in soupLoan.findAll('img', class_ = 'bilderrahmen-fixed'):
        #print(playerImageLink['src'].replace("small", "header"))
        playerImageLinks.append(playerImageLink['src'].replace("small", "header"))

    for j in range(len(playerNames)): 
        #print (playerNames[j] + ", " + playerImageLinks[j])

        path = "D:\\Documents\\WebScraping\\Transfermarkt\\" + teamNamesA[i] + "\\"
        
        if not os.path.isdir(path):
            os.mkdir(path)
            
        urllib.request.urlretrieve(playerImageLinks[j], path + playerNames[j] + '.png') 
