import flask
from flask import request, redirect, render_template, send_from_directory
import requests
import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import gtts
from gtts import gTTS
import re
import os
import os.path, time
from datetime import datetime
import wikipedia

#Defining the SPARQL Endopoint of Wikidata
endpoint_url = "https://query.wikidata.org/sparql"

#Extracting the results of SPARQL queries
def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

app = flask.Flask(__name__)

#Defining the home page
@app.route('/')
def home():
   return render_template('home.html')

#Adding paths of the static files
@app.route('/home/<path:path>')
def static_dir(path):
    return send_from_directory("home", path)

#Adding the error message
@app.route('/errormessage')
def home01():
   return render_template('errormessage.html')

@app.route('/link', methods=['GET', 'POST'])
def home02():
     #Getting the Wikidata item of the concerned topic
     wd = request.args.get('id')
     #Recognizing the browser language
     lg = request.args.get('lang')
     if (lg == None):
        language = str(request.accept_languages)
        languages = language.split(",")
        preflg = languages[0]
     else:
        preflg = lg
     if (preflg.find("-")>=0): preflg = preflg[:preflg.find("-")]  
     #Finding the Wikidata item of the browser language
     url = 'https://hub.toolforge.org/P305:'+preflg+'?format=json'
     wdrequest = requests.get(url)
     response = wdrequest.json()
     langitem = response["origin"]["qid"]
     #Finding the audio file about the topic in the language of the browser
     query = """SELECT * WHERE {
       wd:"""+wd+""" p:P989 [ps:P989 ?voice; pq:P407 wd:"""+langitem+"""].
       }
     LIMIT 1"""
     results = get_results(endpoint_url, query)
     video = "errormessage"
     for result in results["results"]["bindings"]:
       try:
           video = result["voice"]["value"]
       except KeyError:
           video = "errormessage"
     if (video != "errormessage"):
         req = requests.get(video).url
         video = video.replace("/wikipedia/commons/", "/wikipedia/commons/transcoded/")
         video += video[video.rfind("/"):] + ".mp3"
     if (video == "errormessage"):    
       if (preflg in gtts.lang.tts_langs()):
           #Removing MP3 Files from the Wikimedia Cloud
           now = datetime.now()
           timestamp = time.mktime(now.timetuple()) + now.microsecond/1e6
           directory = "./home"
           files = os.listdir(directory)
           filtered_files = [file for file in files if file.endswith(".mp3")]
           for file in filtered_files:
               path_to_file = os.path.join(directory, file)
               if ((timestamp - os.path.getmtime(path_to_file)) > 300): os.remove(path_to_file)
           print(filtered_files)
           #Getting the Wikipedia article in the user language
           url = requests.get("https://hub.toolforge.org/"+ wd +"?lang=" + preflg + "&format=json")
           #Getting the Lead of the Page
           try:
               title = url.json()["destination"]["preferedSitelink"]["title"]
           except:
               title = ""
           wikipedia.set_lang(preflg)
           cond = True
           try:
               page = wikipedia.summary(title)
           except:
               cond = False
           if (cond == True):
               #Cleaning the text
               text = page.replace("\n", " ")
               text = text.replace("\'", '"')
               text = text.replace('"', "'")
               text = text.replace("\xa0", " ")
               #Generating Spoken Wikipedia File 
               tts = gTTS(text, lang=preflg)
               video = "home/"+preflg+"-"+wd+".mp3"
               tts.save(video)
           else:
               video = "errormessage"
       else:
           video = "errormessage"
     return redirect(video)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
