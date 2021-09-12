from bs4 import BeautifulSoup
import requests
import os
from config import *

def Get_Game_Data(url):
    url = 'https://www.metacritic.com/game/playstation-3/portal-2'

    os.chdir('Game_Info')
    os.chdir('HTML')
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    File = requests.get(url, headers=headers)
    File = File.text
    Text_File = open(url.split("/")[-1] + '.txt', "w")
    Text_File.write(File)
    Text_File.close()
    parse = BeautifulSoup(File, 'html.parser')

    Title = parse.select('.product_title > a:nth-child(1) > h1:nth-child(1)')[0].get_text()
    Description = parse.select('.product_summary > span:nth-child(2) > span:nth-child(1) > span:nth-child(2)')[0].get_text()
    Release_Date = parse.select('.release_data > span:nth-child(2)')[0].get_text()
    Metascore = parse.select('.xlarge > span:nth-child(3)')[0].get_text()
    Genres = []
    for i in range(1, len(parse.select('.product_genre')[0].contents)):
        Genres.append(parse.select('.product_genre')[0].contents[i].get_text())
        Genres = list(dict.fromkeys(Genres))
    del Genres[1]
    del Genres[-1]

def Search_MetaCritic(Search_Term, platform=''):
    url = 'https://www.metacritic.com/search/game/' + Search_Term + '/results'

    os.chdir('Game_Info')
    os.chdir('HTML')
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    File = requests.get(url, headers=headers)
    File = File.text
    Text_File = open("Search '" + url.split("/")[-2].split("/")[0] + "'" + '.html', "w")
    Text_File.write(File)
    Text_File.close()
    parse = BeautifulSoup(File, 'html.parser')

    Search_Results = []
    for i in range(len(parse.select("ul.search_results")[0].findAll('a'))):
        Search_Results.append([parse.select("ul.search_results")[0].findAll('a')[i].get_text().strip()])
    for i in range(0, len(parse.select("ul.search_results")[0].findAll('a')), 2):
        Search_Results[int(i/2)].append(parse.select("ul.search_results")[0].findAll('img')[i]["src"])
    print(Search_Results)

Search_MetaCritic("GTA")