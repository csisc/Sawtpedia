import flask
from flask import request, redirect, render_template, send_from_directory
import requests
import sys
from SPARQLWrapper import SPARQLWrapper, JSON

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
     return redirect(video)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)














