import untangle
import os
import wget
from config import *
import shutil
import pickle

filename = []
filelist = []
filelist_name_only = []
global filelist_final

# Downloads list of files available for download
def update_cache():
    shutil.rmtree("Repositories")
    os.mkdir("Repositories")
    os.chdir("Repositories")
    for list_num in range(repos_len):
        print("Downloading repository no. " + str(list_num + 1))
        # Extracts the last section of the URL
        url = repos[list_num]
        filename_internal = url.split("/")[-1]
        # Appends it to get the metadata file's name
        filename.append(filename_internal + "_files.xml")
        wget.download(url + "/" + filename[list_num], filename_internal + "_files.xml")

    # XML parsing
    for repo_num in range(repos_len):
        file_internal = untangle.parse(os.listdir()[repo_num])
        for i in range(len(file_internal.files.file)):
            if file_internal.files.file[i]['name'].split(".")[-1] != "xml" and file_internal.files.file[i]['name'].split(".")[-1] != "sqlite" and file_internal.files.file[i]['name'].split(".")[-1] != "jpg" and file_internal.files.file[i]['name'].split(".")[-1] != "torrent":
                filelist.append(url + '/' + file_internal.files.file[i]['name'].strip())
                filelist_name_only.append(file_internal.files.file[i]['name'].split("(")[0].strip())
                global filelist_final
                filelist_final = {filelist_name_only[i]: filelist[i] for i in range(len(filelist_name_only))}
    os.chdir("..")
    os.chdir("Game_Info")
    f = open("Filelist_Local.list", "wb")
    pickle.dump(filelist_final, f)
    f.close()
    os.chdir("..")

def update_cache_local():
    global filelist_final
    os.chdir("Game_Info")
    f = open("Filelist_Local.list", "rb")
    filelist_final = pickle.load(f)
    os.chdir("..")
