import untangle
import os
import requests
from config import *

filename = []
filelist = []
filelist_name_only = []

# Downloads list of files available for download
def update_cache():
    os.chdir("Repositories")
    for list_num in range(repos_len):
        print(list_num)
        # Extracts the last section of the URL
        url = repos[list_num]
        filename_internal = url.split("/")[-1]
        # Appends it to get the metadata file's name
        filename.append(filename_internal + "_files.xml")
        print(url + "/" + filename[list_num])
        if os.path.exists(filename_internal + "_files.xml"):
            os.remove(filename_internal + "_files.xml")
        requests.get(url + "/" + filename[list_num], filename_internal + "_files.xml")

    # XML parsing
    for repo_num in range(repos_len):
        file_internal = untangle.parse(os.listdir()[repo_num])
        for i in range(len(file_internal.files.file)):
            if file_internal.files.file[i]['name'].split(".")[-1] != "xml" and file_internal.files.file[i]['name'].split(".")[-1] != "sqlite" and file_internal.files.file[i]['name'].split(".")[-1] != "jpg" and file_internal.files.file[i]['name'].split(".")[-1] != "torrent":
                print(file_internal.files.file[i]['name'].split("(")[0])
                filelist.append(file_internal.files.file[i]['name'])
                filelist_name_only.append(file_internal.files.file[i]['name'].split("(")[0])
    os.chdir("..")

