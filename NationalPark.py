import urllib.parse, urllib.request, urllib.error, json
from flask import Flask, render_template, request
import logging

app = Flask(__name__)


# print(type(req))
import key as key
my_key = key.key
endpoint = "https://developer.nps.gov/api/v1/parks?api_key=" + my_key
# HEADERS = {"Authorization":"mse4vGTif7zJqKLNMobA04oeixJzk1Lly949UA8V"}
# req = urllib.request.Request(endpoint,headers=HEADERS)

# Execute request and parse response
response = urllib.request.urlopen(endpoint).read()
data = json.loads(response.decode('utf-8'))


def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

@app.route("/")
def main_handler():
    app.logger.info("In MainHandler")
    return render_template('askNationalPark_1.html',page_title="National Park question form")


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
                progress = progress
                )
            else:
                progress += '4ab '
                return render_template('askNationalPark_1.html',
                page_title="Greeting Form - Error",
                prompt="Park not found, Please try again!", 
                progress = progress)


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
            if user_broadSearch in read_item:
                progress += '4b '
                searchResults.append(item['fullName'])
        if searchResults == []:
            searchResults = ['no results found, aw']

        return render_template('askNationalPark_1.html',
                    page_title="user input results",
                    searchResults=searchResults, 
                    progress = progress)





if __name__ == "__main__":
# Used when running locally only. 
# When deploying to Google AppEngine, a webserver process will
# serve your app. 
    app.run(host="localhost", port=8080, debug=True)

# for item in data['data']:
#         print(item['fullName'])