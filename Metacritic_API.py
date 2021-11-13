from bs4 import BeautifulSoup
import requests
import os
import cli_main
import sys

cli_main.update_cache_local()

def Get_Game_Data(url):
    os.chdir('Game_Info')
    os.chdir('HTML')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    File = requests.get(url, headers=headers)
    File = File.text
    Text_File = open(url.split("/")[-1] + '.html', "w", encoding="utf-8")
    Text_File.write(File)
    Text_File.close()
    parse = BeautifulSoup(File, 'html.parser')

    Title = parse.select('.product_title > a:nth-child(1) > h1:nth-child(1)')[0].get_text()
    Description = parse.select('.product_summary > span:nth-child(2) > span:nth-child(1) > span:nth-child(2)')[
        0].get_text()
    Release_Date = parse.select('.release_data > span:nth-child(2)')[0].get_text()
    Genres = []
    for i in range(1, len(parse.select('.product_genre')[0].contents)):
        Genres.append(parse.select('.product_genre')[0].contents[i].get_text())
        Genres = list(dict.fromkeys(Genres))
    del Genres[1]
    del Genres[-1]
    test_key = Title.replace(":", " -")
    Filename = cli_main.filelist_final[test_key]
    os.chdir("..")
    os.chdir("..")
    return {
        "Title": Title,
        "Description": Description,
        "Release_Date": Release_Date,
        "Genres": Genres,
        "Filename": Filename
    }

def Search_MetaCritic(Search_Term, platform):
    global Search_Results
    global Search_Results_Keys
    if platform == "ps1":
        platform = str(10)
    elif platform == "ps2":
        platform = str(6)
    elif platform == "psp":
        platform = str(7)
    elif platform == "ps3":
        platform = str(1)
    elif platform == "xbox":
        platform = str(12)
    elif platform == "xbox_360":
        platform = str(2)
    elif platform == "wii":
        platform = str(8)
    elif platform == "wii_u":
        platform = str(68410)
    else:
        print("Incorrect platform data")
        print("Exiting...")
        sys.exit()

    url = 'https://www.metacritic.com/search/game/' + Search_Term + '/results?search_type=advanced&plats[' + platform +']=1'
    os.chdir('D:/Python Projects/UltraEmu/Game_Info/HTML ')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    File = requests.get(url, headers=headers)
    File = File.text
    Text_File = open("Search '" + url.split("/")[-2].split("/")[0] + "'" + '.html', "w")
    Text_File.write(File)
    Text_File.close()
    parse = BeautifulSoup(File, 'html.parser')

    Search_Results_Keys = []
    if not len(parse.select("ul.search_results")) == 0:
        for i in range(len(parse.select("ul.search_results")[0].findAll('a'))):
            Search_Results_Keys.append(parse.select("ul.search_results")[0].findAll('a')[i].get_text().strip())

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

        for i in range(len(Search_Results)):
            Search_Results[Search_Results_Keys[i]].append(Search_Results_Keys[i].replace(":", " -"))

        for i in range(len(parse.select("ul.search_results")[0].findAll('a'))):
            Search_Results[Search_Results_Keys[i]].append("https://metacritic.com" + parse.select("ul.search_results")[0].findAll('a')[i]["href"].strip())

        os.chdir("..")
        os.chdir("..")
        return [Search_Results, Search_Results_Keys]

    else:
        return ["", ""]

if __name__ == "__main__":
    search_results = Search_MetaCritic("", "ps3")
    print(search_results[0])
