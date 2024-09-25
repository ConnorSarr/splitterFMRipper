import requests
import bs4
import json
import os
url = input("Enter a splitter.fm link: ") #ask for the link to you know, rip from

request = requests.get(url) #make a GET request for it
soup = bs4.BeautifulSoup(request.text, features='html.parser') #use bs4 for parse the HTML code using the website's source code 
scripts = soup.find_all("script", string=True) #find all tags with "<script>" in it
preLoad = str(scripts[4]) #choose the 5th script tag content, this includes the song details
equalsIndex = preLoad.index("=") + 2
thing = preLoad[equalsIndex:-10] #take just the JSON info and get rid of the "window.jsonVars = " at the beginning and ";" at the end
jsonParse = json.loads(thing) #turn the json into a json object
directoryName = os.path.join(os.path.dirname(os.path.abspath(__file__)),f"{jsonParse['artist']['artistName']} - {jsonParse['song']['name']}") #propose the folder name

if not os.path.isdir(directoryName): #if the directory/folder doesn't exist
   os.makedirs(directoryName) #make the directory/folder with the name we proposed

for stem in jsonParse['stems']: #for every stem in the stems list
    fileName = stem['originalFilename'] #set the filename to be the original filename to start
    if fileName == "": #if the og filename doesn't exist
        fileName = stem['name'] #set the stem name to be the generic stem name instead
    if ".wav" in fileName: #if the stem has wav in the name, it will save as a wav which we don't want
        fileName = fileName.replace(".wav",".mp3") #replace .wav for a .mp3 instead
    if ".mp3" not in fileName: #if .mp3 still isn't in the filename
        fileName = fileName + ".mp3" #put it there
    print("Saving file: " + fileName) #indicate you are saving the file
    fileName = os.path.join(directoryName,fileName)

    with open(fileName,"wb") as f: #this creates the file 
        r = requests.get(stem['audioUrl']) #get the audio url from the json data
        f.write(r.content) #in the file we made, write the content from the audio url
