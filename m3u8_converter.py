import glob
import os
import subprocess
import timeit
import requests

"""
Script that scans for m3u8 files in agiven directory
extracts all links from this files and downloads all m3u8 streams to mp4
and then only keeps the biggest file (aka the highest quality)
"""

#=============================================================================
# VARIABLES
DIRECT = input("please give directory e.g. /home/max/dir\n")

#STRUCTURE = input("please specify structure, multiple file or single file")
#=============================================================================

#=============================================================================
#functions
def filebrowser(direct, ext=""):
    "Returns files with an extension"
    os.chdir(direct)
    return [f for f in glob.glob(f"*{ext}")]

def download_playlist(url_playlist, output_playlist):
    "download the playlist from given url"
    r = requests.get(url_playlist, allow_redirects=True)
    open(output_playlist, 'wb').write(r.content)

def copy_links(file, expr):
    "Returns list with all lines starting with expr from given file"
    length = len(expr)
    lines = []
    for line in file.splitlines():
        if line[0:length] == expr:
            lines.append(line)
    return lines


def get_quality(file_data):
    "Looks for the quality of each stream"
    lines =  list(file_data.split())
    linkes_qual = dict()
    resolution = None
    for line in lines:
        if resolution != None:
            linkes_qual[resolution] = line
            resolution = None
        if line[0] == "#" and "RESOLUTION" in line:
            res_id = line.find("RESOLUTION")
            resolution = (line[res_id+11:]).split(',')[0]
    return(links_qual)        

def best_quality(linkes_qual)
    "determnins the best quality of given dict"
    resolution = [int(key.split('x')[0]) for key in linkes_qual.keys()]
    max_quality = str(max(resolution))
    key_max = str([key for key in linkes_qual.keys() if max_quality in key][0])
    best = linkes_qual[key_max]
    return(best)

def copy_links_names(file, seperator):
    "returns dict with key = playlist name and value = playlist url"
    dictionary = dict()
    for line in file.splitlines():
        if seperator in line:
            sep_pos = line.find(seperator)
            key = line[:sep_pos]
            http_pos = line.find("http")
            value = line[http_pos:]
            dictionary[key] = value
    return dictionary

def download(input_name, output):
    "downloads mp4 file from given m3u8 stream"
    bashCommand = "ffmpeg -i "+ input_name + " -c copy -bsf:a aac_adtstoasc " + output
    command = subprocess.run(bashCommand.split())
    
#=============================================================================
start = timeit.default_timer()


#=============================================================================
# get all m3u8 files from playlist linkes
#=============================================================================
# get links from files in directory
files_playlist = filebrowser(DIRECT, "txt")
for file in files_playlist:
    with open(file, 'r') as f:
        file_data = f.read()
    linkes_playlist = copy_links_names(file_data, "|")

    # download all the playlist info and put into file
    for key in list(linkes_playlist.keys()):
        file_name = key.replace(" ","")
        output_playlist = DIRECT +"/" + file_name + ".m3u8"
        url_playlist = linkes_playlist[key]
        download_playlist(url_playlist, output_playlist)




#=============================================================================
# download m3u8 files to mp4
#=============================================================================
# generate a list with all files 
files = filebrowser(DIRECT, "m3u8")
# generate a dict with all linkes in each file
linkes = dict()
downloads_nr = 0

# extract resolutions and linkes from each m3u8 file
# for file in files:
#     with open(file, 'r') as f:
#         file_data = f.read()

#         lines =  list(file_data.split())
#         linkes_qual = dict()
#         resolution = None
#         for line in lines:
#             if resolution != None:
#                 linkes_qual[resolution] = line
#                 resolution = None
#             if line[0] == "#" and "RESOLUTION" in line:
#                 res_id = line.find("RESOLUTION")
#                 resolution = (line[res_id+11:]).split(',')[0]

#         #find the best resolution for each video 
#         resolution = [int(key.split('x')[0]) for key in linkes_qual.keys()]
#         max_quality = str(max(resolution))
#         key_max = str([key for key in linkes_qual.keys() if max_quality in key][0])
#         linkes_qual["best"] = linkes_qual[key_max]
        
#         linkes[file] = linkes_qual

for file in files:
    with open(file, 'r') as f:
        file_data = f.read()
        linkes_qual = get_quality(file_data)
        linkes_qual["best"] = best_quality(linkes_qual)
        linkes[file] = linkes_qual


for file in files:
    file_name = file.replace(" ", "")
    last_point = file_name.rfind(".")
    file_name = file_name[:last_point] + ".mp4"
    dict_1 = linkes[file]
    linke_http = dict_1["best"]
    output = DIRECT + "/" + file_name
    download(linke_http, output)




stop = timeit.default_timer()
time = stop - start
print(f"Downloaded Successfull {downloads_nr}, in {time}")




