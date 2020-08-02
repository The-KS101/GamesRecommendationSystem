from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import lxml

print('Type in a gaming platform to scrape data on available games')
print('Platform codes are:\n\
1. \'ps4\' \n\
2. \'xboxone\' \n\
3. \'switch\' \n\
4. \'pc\' \n\
5. \'all\' ')
print('Enter Platform code: ', end = '')
platformCode = input()
platformList = ['ps4', 'xboxone', 'switch', 'pc', 'all']
while True:
    if platformCode not in platformList:
        print('Invalid platform code, codes are case sensitive, Try again.')
        print('Enter Platform code: ', end = '')
        platformCode = input()
    else:
        break
urlSearch = 'https://www.metacritic.com/browse/games/score/metascore/all/{}/\
            filtered'.format(platformCode)
urlMain = 'https://www.metacritic.com'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\
            /537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
print('Fetching Page...')
page = requests.get(urlSearch, headers = headers)
if page.status_code == requests.codes.ok:
    soup = BeautifulSoup(page.text, 'lxml')
    print('Page Found')

data = {
        'names' : [],
        'platforms' : [],
        'release_dates' : [],
        'meta_scores' : [],
        'game_descriptions' : [],
        'user_scores' : [],
        'ageRatings' : [],
        'gameDevs' : [],
        'gameGenres' : [],
        }

def findFeats(soup):
    gameLink = []
    namesTab = soup.find_all('a', 'title')
    for i in namesTab:
        gameLink.append(urlMain + i['href'])
        data['names'].append(i.string)
    platTab = soup.find_all('div', 'clamp-details')
    for i in platTab:
        plat = i.find_all('span')
        data['platforms'].append(plat[1].string.strip())
        data['release_dates'].append(plat[2].string.strip())
        
    metaScoreTab = soup.find_all('div', 'clamp-metascore')
    for i in metaScoreTab:
        i2 = i.find_all('a', 'metascore_anchor')
        data['meta_scores'].append(i2[0].contents[1].string)


    userScoreTab = soup.find_all('div', 'clamp-userscore')
    for i in userScoreTab:
        i2 = i.find_all('a', 'metascore_anchor')
        data['user_scores'].append(i2[0].contents[1].string)

    descTab = soup.find_all('div', 'summary')
    for i in descTab:
        data['game_descriptions'].append(i.contents[0].strip())
    descTab = userScoreTab = metaScoreTab = platTab = i2 = None
    return gameLink

pageNo = 1
while True:
    gameLink = findFeats(soup)
    listNo = 1
    urlPageSearch = 'https://www.metacritic.com/browse/games/score/metascore/all\
/{}/filtered?page={}'.format(platformCode,pageNo)
    for i in gameLink:
        listPec = (listNo/len(gameLink)) * 100
        print('Fetching Details {}%...'.format(int(listPec)), end=' ')
        page = requests.get(i + '/details', headers = headers)
        print('Detail Gotten')
        if page.status_code == requests.codes.ok:
            soup = BeautifulSoup(page.text, 'lxml')
            print('Details Found', end=' ')
            dets = soup.find_all('div', 'product_details')
            table = dets[1].find('table')
            try:
                rating = table.find(text = 'Rating:').findNext('td').contents[0]
                data['ageRatings'].append(rating)
            except:
                data['ageRatings'].append(np.nan)
                print('Age Rating not found')
            try:
                dev = table.find(text = 'Developer:').findNext('td').contents[0]
                data['gameDevs'].append(dev)
            except:
                data['gameDevs'].append(np.nan)
                print('Developers Unknown')
            try: 
                genre = table.find(text = 'Genre(s):').findNext('td').contents[0]
                data['gameGenres'].append(genre.strip())
            except:
                data['gameGenres'].append(np.nan)
                print('Genre Unknown')
            listNo += 1
            print('Details Appended')
            
        else:
            data['ageRatings'].append(np.nan)
            data['gameDevs'].append(np.nan)
            data['gameGenres'].append(np.nan)
            print('Could not access given page') 
            listNo += 1

    page = requests.get(urlPageSearch, headers=headers)
    print('Fetching Page {}'.format(pageNo), end = ' ')
    if page.status_code == requests.codes.ok:
        soup = BeautifulSoup(page.text, 'lxml')
        print('Page Found=============================================> {}'.format(pageNo))
        pageNo += 1        
    elif gameLink == []:
        break

print('Scraping Success, Tidying up data')
for i in range(len(data['gameGenres'])):
	if data['gameGenres'][i] != float(np.nan):
		group = str(data['gameGenres'][i]).strip().split(',')
		words = []
	else:
		break
	for j in group:
		words.append(str(j).strip())
	data['gameGenres'][i] = ', '.join(words)
        

dataFrame = pd.DataFrame.from_dict(data, orient='index').transpose()
dataFrame.to_csv('MetaCritic_{}_Game_Rating.csv'.format(platformCode), index=None)
print('DataFrame Created in script location.')
