import urllib.parse, urllib.request, urllib.error, json
from flask import Flask, render_template, request

app = Flask(__name__)

import key as key
my_key = key.key
endpoint = "https://developer.nps.gov/api/v1/parks?api_key=" + my_key

response = urllib.request.urlopen(endpoint).read()
data = json.loads(response.decode('utf-8'))


def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

@app.route("/")
def main_handler():
    app.logger.info("In MainHandler")
    return render_template('home-page.html',page_title="National Park question form")


@app.route("/gresponse")
def response_handler():
    #find a specific national park
    progress = 'progress = '
    progress += '0 '
    user_NP = request.args.get('user_NP')
    app.logger.info(user_NP)
    progress += '1 '
    if user_NP:
        progress += '2a '
        #retrieve info about that national park 
        for item in data['data']:
            progress += '3a '
            if item['fullName'] == user_NP:
                progress += '4aa '
                return render_template('response.html',page_title="page 2", 
                user_NP = user_NP, 
                item = item, 
                progress = ''
                )
            else:
                progress += '4ab '
                return render_template('askNationalPark_1.html',
                page_title="Greeting Form - Error",
                prompt="Park not found, Please try again!", 
                progress = '')


    #search for national park
    user_broadSearch = request.args.get('user_broadSearch')
    if user_broadSearch:
        progress += '2b '
        searchResults = []

        #find all related items to users search
        for item in data['data']:
            progress += '3b '
            #prep dictionary item for search
            read_item = str(item)
            punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
            # Removing punctuations in string
            for ele in read_item:
                if ele in punc:
                    read_item = read_item.replace(ele, "")
            #searches if search is there
            if user_broadSearch.lower() in read_item.lower():
                progress += '4b '
                searchResults.append(item)
        if searchResults == []:
            searchResults = ['no results found, aw']

        return render_template('askNationalPark_1.html',
                    page_title="user input results",
                    searchResults=searchResults, 
                    progress = '')
    
                     
@app.route("/redirect_button")
def getNP():
    select_NP = request.args.get('select_NP')
    National_park_selected = {}
    x = 0
    for item in data['data']:
        if select_NP == data['data'][x]['parkCode']:
            National_park_selected = item
        x+= 1
    
    
    return render_template('response.html',
                page_title="Selected National Park", 
                select_NP = National_park_selected, 
                KEY = key.mapKEY
    )

if __name__ == "__main__":
# Used when running locally only. 
# When deploying to Google AppEngine, a webserver process will
# serve your app. 
    app.run(host="localhost", port=8080, debug=True)
