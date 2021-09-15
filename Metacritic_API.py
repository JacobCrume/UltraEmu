from bs4 import BeautifulSoup
import requests
from config import *
from cli_main import *

update_cache()

def Get_Game_Data(url):
    url = 'https://www.metacritic.com/game/playstation-3/uncharted-2-among-thieves'

    os.chdir('Game_Info')
    os.chdir('HTML')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    File = requests.get(url, headers=headers)
    File = File.text
    Text_File = open(url.split("/")[-1] + '.html', "w")
    Text_File.write(File)
    Text_File.close()
    parse = BeautifulSoup(File, 'html.parser')

    global Title
    global Description
    global Release_Date
    global Metascore
    global Genres
    global Filename
    Title = parse.select('.product_title > a:nth-child(1) > h1:nth-child(1)')[0].get_text()
    Description = parse.select('.product_summary > span:nth-child(2) > span:nth-child(1) > span:nth-child(2)')[
        0].get_text()
    Release_Date = parse.select('.release_data > span:nth-child(2)')[0].get_text()
    Metascore = parse.select('.xlarge > span:nth-child(3)')[0].get_text()
    Genres = []
    for i in range(1, len(parse.select('.product_genre')[0].contents)):
        Genres.append(parse.select('.product_genre')[0].contents[i].get_text())
        Genres = list(dict.fromkeys(Genres))
    del Genres[1]
    del Genres[-1]
    test_key = Title.replace(":", " -")
    if test_key in filelist_final:
        print("Found " + test_key)
    else:
        print("Did not find  " + test_key)
    Filename = filelist_final[test_key]
    os.chdir("..")
    os.chdir("..")


def Search_MetaCritic(Search_Term, platform=''):
    url = 'https://www.metacritic.com/search/game/' + Search_Term + '/results'
    os.chdir('Game_Info')
    os.chdir('HTML')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    File = requests.get(url, headers=headers)
    File = File.text
    Text_File = open("Search '" + url.split("/")[-2].split("/")[0] + "'" + '.html', "w")
    Text_File.write(File)
    Text_File.close()
    parse = BeautifulSoup(File, 'html.parser')

    Search_Results_Keys = []
    for i in range(len(parse.select("ul.search_results")[0].findAll('a'))):
        Search_Results_Keys.append(parse.select("ul.search_results")[0].findAll('a')[i].get_text().strip())
    Search_Results_Keys = list(dict.fromkeys(Search_Results_Keys))

    # Remove all the useless images
    Bad_Images_List = []
    for i in range(len(parse.select("ul.search_results")[0].findAll('img'))):
        if parse.select("ul.search_results")[0].findAll('img')[i]['src'] == '/images/icons/mc-mustplay-sm.svg':
            Bad_Images_List.append(i)
    for i in range(len(Bad_Images_List)):
        parse.select("ul.search_results")[0].findAll('img')[Bad_Images_List[i] - i].decompose()

    # Match images with text
    Search_Results = {}
    for i in range(len(parse.select("ul.search_results")[0].findAll('img'))):
        Image_Name = parse.select("ul.search_results")[0].findAll('img')[i]['alt'].rpartition(" ")[0]
        Image_URL =  parse.select("ul.search_results")[0].findAll('img')[i]['src']
        Search_Results[Image_Name] = [Image_URL]
        print(Image_Name, Image_URL)
        print(Search_Results)


    print(Search_Results_Keys)

update_cache()
Search_MetaCritic(input("What game do you want to find? "))
