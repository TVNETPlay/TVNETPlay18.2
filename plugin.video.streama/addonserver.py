# -*- coding: utf-8 -*-
# Module: default
# Author: joen, bodems
# Created on: 24.08.2017
# License: MIT

import json
import urllib
import sys
from urllib import urlencode
import urllib2
import urlparse
from urlparse import parse_qsl
import cookielib
import os

streamaurl = 'http://localhost:8080'
username = 'mario'
password = 'mario88'
maxval = '20000'

# Initialize the authentication
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = urllib.urlencode({'username' : username, 'password' : password, 'remember_me' : 'on'})
# Authenticate
opener.open(streamaurl + '/login/authenticate', login_data)

cookiestring = str(cj).split(" ")
sessionid = cookiestring[1].split("JSESSIONID=")
remember_me = cookiestring[5].split("streama_remember_me=")

urljson = '/data/w1004r/data.0/py/json/'

def get_shows():
    items = opener.open(streamaurl + '/dash/listShows.json?max=' + maxval)
    videolist = json.loads(items.read())
    return videolist["list"]

def get_movies():
    items = opener.open(streamaurl + '/dash/listMovies.json?max=' + maxval)
    videolist = json.loads(items.read())
    return videolist["list"]

def shows():
    videos = get_shows()
    for video in videos:
        try:
            urlremotaw500 = 'https://image.tmdb.org/t/p/w500//' + video['poster_path']
            urlw500 = '/data/w1004r/tmdb.image.0/t/p/w500/' + video['poster_path']
            # Download Image
            if os.path.isfile(urlw500):
                sys.exit
            else:
                urllib.urlretrieve(urlremotaw500, urlw500)
        except:
            foo = 23

def movies():
    videos = get_movies()
    for video in videos:
        try:
            urlremotaw500 = 'https://image.tmdb.org/t/p/w500//' + video['poster_path']
            urlw500 = '/data/w1004r/tmdb.image.0/t/p/w500/' + video['poster_path']
            urlremotaw1280 = 'https://image.tmdb.org/t/p/w1280//' + video['backdrop_path']
            urlw1280 = '/data/w1004r/tmdb.image.0/t/p/w1280/' + video['backdrop_path']
            # Download Image
            if os.path.isfile(urlw500):
                sys.exit
            else:
                urllib.urlretrieve(urlremotaw500, urlw500)
            if os.path.isfile(urlw1280):
                sys.exit
            else:
                urllib.urlretrieve(urlremotaw1280, urlw1280)
        except:
            foo = 23

def jsonfile():
    listMovies = urljson + 'listMovies.json'
    items = opener.open(streamaurl + '/dash/listMovies.json?max=' + maxval)
    videolist = json.loads(items.read())
    with open(listMovies, 'w') as json_file:  
        json.dump(videolist, json_file)

    listShows = urljson + 'listShows.json'
    items = opener.open(streamaurl + '/dash/listShows.json?max=' + maxval)
    videolist = json.loads(items.read())
    with open(listShows, 'w') as json_file:  
        json.dump(videolist, json_file)

    listNewReleases = urljson + 'listNewReleases.json'
    items = opener.open(streamaurl + '/dash/listNewReleases.json?max=' + maxval)
    videolist = json.loads(items.read())
    with open(listNewReleases, 'w') as json_file:  
        json.dump(videolist, json_file)

jsonfile()
shows()
movies()
