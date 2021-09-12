from bs4 import BeautifulSoup
import requests
import os
from config import *

def Search_MetaCritic(Search_Term, platform=''):
    url = 'https://www.metacritic.com/search/game/' + Search_Term + '/results'

    os.chdir('Game_Info')
    os.chdir('HTML')
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    File = requests.get(url, headers=headers)
    File = File.text
    Text_File = open(url.split("/")[-1] + '.txt', "w")
    Text_File.write(File)
    Text_File.close()
    parse = BeautifulSoup(File, 'html.parser')

    Search_Results = []
    for i in range(len(parse.select("ul.search_results")[0].findAll('a'))):
        Search_Results.append(parse.select("ul.search_results")[0].findAll('a')[i].get_text().strip())

    Search_Results = list(dict.fromkeys(Search_Results))
    print(Search_Results)

    global Search_Results
    Search_Results =[]
    for i in range():
        print(parse)