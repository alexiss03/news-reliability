from flask import Flask

import os
import json
import urllib
import pprint

import facebook
import requests
from bs4 import BeautifulSoup


os.environ['ACCESS_TOKEN'] = "EAACEdEose0cBAOZBTyWh3nULVojEUAZB01ZBt6QZBkf86hIz26PDNZB2DOdEpm0VPPhWfTg31nEyG2MJsRVzqxrRbffADtbIBwlYw4jVQpSJjZBI6qdU88qlYVRnQAF2RsyNi34PplbMwyNmPU8fK2ZCFBMAHBPG5WGf0oPoJXMZCvwlaAtCKY8IxSOPDskP2K8ZD"
os.environ['APP_ID'] = "417532035253979"
os.environ['APP_SECRET'] = "bdabd42f7762399c3bdc91ebbb336178"

app = Flask(__name__)

@app.route('/')
def scrape():
    #soup = BeautifulSoup(open("index.html"))  #make these set of codes dynamic (to faceboook)
    #BE CAREFUL, python is sensitive to indentation
    soup = BeautifulSoup("<html>data</html>")

    #LOOP ALL POSTS IN FACEBOOK
        #CHECK IF A POST CONTAINS "NEWS" KEYWORDS (declare a list variable of all keywords)
            #IF HAS
                #GET THESE DETAILS:  details of one poster, date, keywords matched and text in the post
                    #CLEAN THE DATA by removing unnecessary characters

    print (soup.html);
    return 'This is a sample Flask application!'

@app.route('/fb')
def fb_scrapper():
    # get Facebook access token from environment variable
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

    # build the URL for the API endpoint
    host = "https://graph.facebook.com"
    path = "/me"
    params = urllib.urlencode({"access_token": ACCESS_TOKEN})

    url = "{host}{path}?{params}".format(host=host, path=path, params=params)

    # open the URL and read the response
    resp = urllib.urlopen(url).read()

    # convert the returned JSON string to a Python datatype 
    me = json.loads(resp)

    # display the result
    return resp

@app.route('/posts')
def some_action():
    
    """ Here you might want to do something with each post. E.g. grab the
    post's message (post['message']) or the post's picture (post['picture']).
    In this implementation we just print the post's created time.
    """
    # print(post['created_time'])

    # You'll need an access token here to do anything.  You can get a temporary one
    # here: https://developers.facebook.com/tools/explorer/
    access_token = get_fb_token()
    # Look at Bill Gates's profile for this example by using his Facebook id.
    user = 'TaylorSwift'

    graph = facebook.GraphAPI(access_token)
    profile = graph.get_object(user)
    posts = graph.get_connections(profile['id'], 'posts')

    # Wrap this block in a while loop so we can keep paginating requests until
    # finished.
#    while True:
#        try:
#            # Perform some action on each post in the collection we receive from
#            # Facebook.
#            [some_action(post=post) for post in posts['data']]
#            # Attempt to make a request to the next page of data, if it exists.
#            posts = requests.get(posts['paging']['next']).json()
#        except KeyError:
#            # When there are no more pages (['paging']['next']), break from the
#            # loop and end the script.
#            break
    post_text = ""
    #for post in posts['data']:
    #    post_text = post_text + str(post)
    return str(posts['data'])

@app.route('/token')
def get_fb_token():           
    payload = {'grant_type': 'client_credentials', 'client_id': os.environ['APP_ID'], 'client_secret': os.environ['APP_SECRET']}
    file = requests.post('https://graph.facebook.com/oauth/access_token?', params = payload)
    #print file.text #to test what the FB api responded with    
    result = file.text.split("=")[1]
    #print file.text #to test the TOKEN
    return result

app.run(debug=True)
app.run(port=8082)
