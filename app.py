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
     language = str(request.accept_languages)
     languages = language.split(",")
     preflg = languages[0]
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
               if (timestamp - os.path.getmtime(path_to_file)) > 300): os.remove(path_to_file)
           print(filtered_files)
           #Getting the Wikipedia article in the user language
           url = requests.get("https://hub.toolforge.org/"+ wd +"?lang=" + preflg)
           #Getting the Lead of the Page
           txt = url.text
           if (txt.find('<div id="siteSub" class="noprint">From Wikidata</div>') < 0):
               print(txt)
               txt = txt[txt.find('<div id="mw-content-text"'):]
               print(txt)
               if (txt.find("<h2")>=0):
                   txt = txt[txt.find("<p"):txt.find("<h2")]
               else:
                   txt = txt[txt.find("<p"):]
               #Eliminating References
               clean = re.compile('<sup id="cite.*?sup>')
               txt = re.sub(clean, '', txt)
               #Eliminating Styles
               clean = re.compile('<style.*?style>')
               txt = re.sub(clean, '', txt)
               #Eliminating DIV
               b = True
               while (txt.find("<div") >= 0) and (b == True):
                   div = txt[txt.find("<div"):]
                   if (div.find("/div>") >= 0):
                       div = div[:div.find("/div>")+5]
                       print(div)
                       txt = txt.replace(div, "")
                       print(txt)
                   else:
                       b = False
               #Eliminating Links
               clean = re.compile('<a class="mw-jump-link".*?a>')
               txt = re.sub(clean, '', txt)
               #Eliminating Special Characters
               clean = re.compile('&#.*?;')
               txt = re.sub(clean, '', txt)
               #Eliminating Tables and Infoboxes
               if (txt.find("<table")>=0): txt = txt[:txt.find("<table")]+txt[txt.find("</table>"):]
               #Stripping HTML Tags
               clean = re.compile('<.*?>')
               txt = re.sub(clean, '', txt)
               print(txt)
               #Generating Spoken Wikipedia File 
               tts = gTTS(txt, lang=preflg)
               video = "home/"+preflg+"-"+wd+".mp3"
               tts.save(video)
           else:
               video = "errormessage"
       else:
           video = "errormessage"
     return redirect(video)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
