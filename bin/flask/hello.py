from flask import Flask

import os
import json
import urllib
import pprint

import facebook
import requests

os.environ['ACCESS_TOKEN'] = "EAACEdEose0cBALjazJUOfxtAzT5VkqmUFhjTnvvfQFccouFOlRvwANV5MXYMe8xZAlkQoZC4FS2dPnf4S7S7gQs76jN41Hp0Gs3IZCCxgBl16ODM3yCM3iVbF6vwGuYr4qfNhQzZCPl98eoNFWDhEp93JMBftLLWjuuSZARTiZAmCiJT5wfENUZCsCuGBQGjLgZD"

app = Flask(__name__)

@app.route('/')
def hello_world():
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
    access_token = os.environ['ACCESS_TOKEN']
    # Look at Bill Gates's profile for this example by using his Facebook id.
    user = 'BillGates'

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

app.run(port=8080)
