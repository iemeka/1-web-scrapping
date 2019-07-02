import urllib
import os
import re
import json
from query_runner import *


linkToCdir = os.path.dirname(__file__) # link to the current directory

def extract(filename):
    path = 'files/' # directory of all html files
    justFileName = filename.split(".")[0] # split file name into two taking the first part

    #add file format
    textFileName = justFileName+".txt" 
    jsonFileName = justFileName+".json"

    #part to html files
    filepath= path+filename

    #part to newly created files
    pathToTextFiles = os.path.dirname(os.path.join(linkToCdir, 'text-files/'+textFileName+'/'))
    pathToJsonFiles = os.path.dirname(os.path.join(linkToCdir, 'json-files/'+jsonFileName+'/'))
    pathToAllNames = os.path.dirname(os.path.join(linkToCdir, 'all_names/'))

    #opens html file
    html_files = urllib.urlopen(filepath)

    ranksOfNames = [] # to contain a series of dictionary, each dictionary represent a row in the html table

    #open text file in writable mode
    g = open(pathToTextFiles,"w")
    h = open(pathToAllNames, "a")

    for line in html_files.readlines(): # read each lines in the html file
        if '<tr align="right"><td>' in line: # if a line contains this string findall and print strings between this html tag <td></td>
            data = re.findall('(?<=<td>).*?(?=</td>)', line)
            # text file
            space = " "
            bigData = data[0] + space + data[1]+ space + data[2] + "\n" # gets element of the list ending with a newline character
            g.write(bigData)
            h.write(data[1]+ space + data[2] + "\n") # all names are saved here

        
            #json file
            row = {}
            names = {"male name":data[1],"female name":data[2]}
            row[data[0]] =  names # rank number is the key while names is the value
            ranksOfNames.append(row) #append rows of data to the list

            #database
            @insert_names_deco
            def insert_query():
                query = """INSERT INTO baby_names(male_name,female_name) 
                VALUES('%s','%s') RETURNING rank;""" % (data[1],data[2])
                return query
            insert_query()

    holder = {"data":ranksOfNames} # main dictionary

    #open json file in writable mode
    f = open(pathToJsonFiles, "w") 
    json.dump(holder, f) # write to json file



html_file_directory = os.path.dirname(os.path.join(linkToCdir, 'files/'))# link to folder containing html files
all_html_files = os.listdir(html_file_directory) # list of html files in the folder

for filename in all_html_files: # looping through all files and extracting data from them
    extract(filename)
