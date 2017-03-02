from flask import Flask, render_template, request

import os
import json
import urllib
import pprint

import facebook
import requests
import re
from bs4 import BeautifulSoup
from gmascraper import gmascraper
from rapplerscraper import rapplerscraper
from cnnscraper import cnnscraper
from manilabulletinscraper import manilabulletinscraper
from philstarscraper import philstarscraper
from createdb import db, Newslink, Word
from functions import *
#from sklearn.feature_extraction.text import TfidfVectorizer
#import numpy

os.environ['ACCESS_TOKEN'] = "EAACEdEose0cBAOZBTyWh3nULVojEUAZB01ZBt6QZBkf86hIz26PDNZB2DOdEpm0VPPhWfTg31nEyG2MJsRVzqxrRbffADtbIBwlYw4jVQpSJjZBI6qdU88qlYVRnQAF2RsyNi34PplbMwyNmPU8fK2ZCFBMAHBPG5WGf0oPoJXMZCvwlaAtCKY8IxSOPDskP2K8ZD"
os.environ['APP_ID'] = "417532035253979"
os.environ['APP_SECRET'] = "bdabd42f7762399c3bdc91ebbb336178"

app = Flask(__name__)

#add here all the legitimate news sites, we will scrape their posts and will be the baseline/standard of a reliable news
legitnews = ['ABSCBN', 'GMA', 'RAPPLER', 'CNN'];

@app.route('/')
def home():
    return 'This is the homepage!'


#this is to check the reliability of an inputted news site.
@app.route('/input')
def input():
    # Add an input form getting the facebook url of the news site
    return render_template('/input.html');


@app.route('/check', methods=['POST', 'GET'])
def check():
    result = request.form;
    
    fbname = ''

    if(result['url'] != ''):
        #do something with url, only get the group name
        found = re.search('facebook.com/([a-zA-Z0-9]+)/*?',  result['url']).group(1);
        fbname = found;
        
    elif(result['fbname'] != ''):
        fbname= result['fbname'];

    print(fbname);
    user= fbname;
    
    # You'll need an access token here to do anything. You can get a temporary one
    # here: https://developers.facebook.com/tools/explorer/
    access_token = get_fb_token()
    

    graph = facebook.GraphAPI(access_token)
    profile = graph.get_object(user)
    posts = graph.get_connections(profile['id'], 'posts', fields='id, message, created_time, link')
    print(posts)
    #posts = graph.get_connections(profile['id'], 'url')

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

    #get all posts which are news related, checks if the words are used formally, and no grammar issues
    for post in posts['data']:
        #print(post);
        if('message' in list(post)):  #only include 'message' not story. message are the one the user posted. 
            post['message'] = re.sub(r'([^a-zA-Z\d\s])+', '', post['message']); #remove stray characters
            #TODO: remove meaningless words, typo, etc.
        #print("#########################");
        
    return render_template("output.html", posts = posts['data']);
    #return str(posts['data'])
        

@app.route('/scrape', methods=["POST", "GET"])
def scrapedata():
    channel = request.form['channel']

    if(channel == 'GMA'):
        gmascraper()
    elif(channel == 'RAPPLER'):
        rapplerscraper()
    elif(channel == 'CNN'):
        cnnscraper()
    elif(channel == 'MANILABULLETIN'):
        manilabulletinscraper()
    elif(channel == 'PHILSTAR'):
        philstarscraper()

    return "SEE LOGS " + request.form['channel'];


@app.route('/selectworddb', methods=["POST", "GET"])
def selectworddb():
    print(Word.query.all())
    return "SEE LOG FOR THE DB CONTENTS: WORDS"

@app.route('/selectnewslinkdb', methods=["POST", "GET"])
def selectnewslinkdb():
    print(Newslink.query.all())
    return "SEE LOG FOR THE DB CONTENTS: NEWSLINK"

@app.route('/deletedb', methods=["POST", "GET"])
def deletedb():
    db.drop_all(bind=None) #delete contents of db
    db.create_all()
    return str(Word.query.all())

@app.route('/token')
def get_fb_token():           
    payload = {'grant_type': 'client_credentials', 'client_id': os.environ['APP_ID'], 'client_secret': os.environ['APP_SECRET']}
    file = requests.post('https://graph.facebook.com/oauth/access_token?', params = payload)
    #print file.text #to test what the FB api responded with    
    result = file.text.split("=")[1]
    #print file.text #to test the TOKEN
    return result




if __name__ == "__main__":
    app.run()

#app.run(debug=True)
#app.run(port=8082)

