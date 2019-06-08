# -*- coding: utf-8 -*-
# Module: default
# Author: joen, bodems
# Created on: 24.08.2017
# License: MIT
# Modified: Mario Pazmino

from __future__ import print_function

import json
import operator
import routing
import sys
import urllib
from urllib import urlencode
import urllib2
import urlparse
from urlparse import parse_qsl
import cookielib
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmc
import xbmcvfs
import shutil
import os

addon = xbmcaddon.Addon('plugin.video.streama')
streamaurl = 'http://www.tvnetplay.net:8080'
username = addon.getSetting('username')
password = addon.getSetting('password')
maxval = '20000'

# Initialize the authentication
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

VIDEOS = {  'Series': [],
            'Todas': [],
            'Destacadas': [],
            'Acción': [],
            'Infantil': [],
            'Misterio': [],
            'Drama': [],
            'Aventura': [],
            'Comedia': [],
            'Familia': [],
            'Terror': [],
            'Buscar': [],
            }


# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

# Rutas
ruta_imagenes = xbmc.translatePath('special://home/addons/plugin.video.streama/resources/media/')
urlw500 = 'http://www.tvnetplay.net/tmdb.image.0/t/p/w500//'
urlw1280 = 'http://www.tvnetplay.net/tmdb.image.0/t/p/w1280//'
url2 = 'http://www.tvnetplay.net/data.0/py/json/'

def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def listar(category, showid, genre):
    # Get the list of videos in the category.
    videos = get_videos(category, showid)
    for video in videos:
        list_item = xbmcgui.ListItem(label=video['title'])
        for film in video['genre']:
            genero = film['name']
            if (genero == genre):
                year = video['release_date']
                list_item.setInfo(
                'video', {'title': video['title'],'plot': video['overview'],'genre' : film['name'],'rating': video['vote_average'],'year': video['release_date']})
                list_item.setArt({'poster': urlw500 + video['poster_path'], 'icon': urlw500 + video['poster_path'], 'fanart': urlw1280 + video['backdrop_path']})
                list_item.setProperty('IsPlayable', 'true')
                # Create a URL for a plugin recursive call.
                id = video['id']
                url = get_url(action='play', video=id)
                #Add the list item to a virtual Kodi folder.
                is_folder = False
                xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
                break

def get_categories():
    # return the list of categories
    return VIDEOS.iterkeys()

def get_videos(category, showid):
    items_movie = opener.open(url2 + 'listMovies.json')
    videolist_movie = json.loads(items_movie.read())
    if category == 'Series':
        items = opener.open(url2 + 'listShows.json')
        videolist = json.loads(items.read())
        return videolist["list"]
    elif category == 'Episodes':
        authentication()
        cookiestring = str(cj).split(" ")
        sessionid = cookiestring[1].split("JSESSIONID=")
        try:
            remember_me = cookiestring[5].split("streama_remember_me=")
            items = opener.open(streamaurl + '/tvShow/EpisodesForTvShow.json?id=' + showid)
            videolist = json.loads(items.read())
            return videolist
        except Exception:
            errorconection()
    elif category == 'Todas':
        return videolist_movie["list"]
    elif category == 'Acción':
        return videolist_movie["list"]
    elif category == 'Aventura':
        return videolist_movie["list"]
    elif category == 'Comedia':
        return videolist_movie["list"]
    elif category == 'Drama':
        return videolist_movie["list"]
    elif category == 'Familia':
        return videolist_movie["list"]
    elif category == 'Infantil':
        return videolist_movie["list"]
    elif category == 'Misterio':
        return videolist_movie["list"]
    elif category == 'Terror':
        return videolist_movie["list"]
    elif category == 'Destacadas':
        items = opener.open(url2 + 'listNewReleases.json')
        videolist = json.loads(items.read())
        return videolist
    elif category == 'Buscar':
        dialog = xbmcgui.Dialog()
        searchstring = dialog.input('Buscar:', type=xbmcgui.INPUT_ALPHANUM)
        if len(searchstring) !=0:
            authentication()
            cookiestring = str(cj).split(" ")
            sessionid = cookiestring[1].split("JSESSIONID=")
            try:
                remember_me = cookiestring[5].split("streama_remember_me=")
                searchstring = urllib.quote_plus(searchstring)
                items = opener.open(streamaurl + '/dash/searchMedia.json?query=' + searchstring)
                videolist = json.loads(items.read())
                return videolist
            except Exception:
                errorconection()
        else:
            list_categories()
            
    else:
        items = []
        videolist = json.loads(items.read())
        return videolist


def list_categories():
    # Get video categories
    categories = get_categories()    
    # Iterate through categories
    for category in categories:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category)
        listado = list_item.setInfo('video', {'title': category})
        listado = list_item.setArt({'fanart': ruta_imagenes + 'fanart-1.jpg'})
        list_item.setInfo('video', {'title': category})
        if (category == 'Buscar'):
            list_item.setArt({'thumb': ruta_imagenes + 'folder/search.png'})
        elif (category == 'Acción'):
            list_item.setArt({'thumb': ruta_imagenes + 'folder/accion.png'})
        elif (category == 'Aventura'):
            list_item.setArt({'thumb': ruta_imagenes + 'folder/aventura.png'})
        elif (category == 'Comedia'):
            list_item.setArt({'thumb': ruta_imagenes + 'folder/comedia.png'})
        elif (category == 'Drama'):
                list_item.setArt({'thumb': ruta_imagenes + 'folder/drama.png'})
        elif (category == 'Familia'):
            list_item.setArt({'thumb': ruta_imagenes + 'folder/familia.png'})
        elif (category == 'Infantil'):
            list_item.setArt({'thumb': ruta_imagenes + 'folder/infantil.png'})
        elif (category == 'Misterio'):
            list_item.setArt({'thumb': ruta_imagenes + 'folder/misterio.png'})
        elif (category == 'Terror'):
            list_item.setArt({'thumb': ruta_imagenes + 'folder/terror.png'})
        elif (category == 'Destacadas'):
            list_item.setArt({'thumb': ruta_imagenes + 'folder/destacadas.png'})
        elif (category == 'Todas'):
            list_item.setArt({'thumb': ruta_imagenes + 'folder/todas.png'})
        elif (category == 'Series'):
            list_item.setArt({'thumb': ruta_imagenes + 'folder/series.png'})
        else:
            list_item.setArt({'thumb': ruta_imagenes + 'folder/star1.png'})
        url = get_url(action='listing', category=category, showid=0)
            # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
            # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    xbmcplugin.endOfDirectory(_handle)


def list_videos(category, showid):
    # Get the list of videos in the category.
    videos = get_videos(category, showid)
    if category == 'Series':
        for video in videos:
            list_item = xbmcgui.ListItem(label=video['name'])
            listado = list_item.setArt({'fanart': ruta_imagenes + 'fanart-1.jpg'})
            try:
                list_item.setArt({'thumb': urlw500 + video['poster_path'], 'icon': urlw500 + video['poster_path']})
                list_item.setInfo('video', {'plot': video['overview'], 'year': video['first_air_date'], 'rating': video['vote_average']})
            except:
                foo = 23
            id = video['id']
            url = get_url(action='listing', category='Episodes', showid=id)
            is_folder = True
            xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    elif category == 'Episodes':
        for video in videos:
            list_item = xbmcgui.ListItem(label=video['name'])
            #listado = 'https://image.tmdb.org/t/p/w300//' + video['still_path']
            listado = urlw500 + video['still_path']

            if video['hasFile'] == 1:
                list_item = xbmcgui.ListItem(label='S'+str(video['season_number'])+'E'+str(video['episode_number'])+' '+video['name'])
                list_item.setInfo('video', {'title': 'S'+str(video['season_number'])+'E'+str(video['episode_number'])+' '+video['name'], 'plot': video['overview']})
                list_item.setArt({'poster': listado, 'icon': listado})
                list_item.setProperty('IsPlayable', 'true')
                id = video['id']
                url = get_url(action='play', video=id)
                is_folder = False
                xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    elif category == 'Todas':
        # Iterate through videos.
        for video in videos:
            # Create a list item with a text label and a thumbnail image.
            list_item = xbmcgui.ListItem(label=video['title'])
            # Set additional info for the list item.
            for film in video['genre']:
                year = video['release_date']
                list_item.setInfo(
                'video', {'title': video['title'],'plot': video['overview'],'genre' : film['name'],'rating': video['vote_average'],'year': video['release_date']
                })
            # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
            # Here we use the same image for all items for simplicity's sake.
            # In a real-life plugin you need to set each image accordingly.
            try:
                list_item.setArt({'poster': urlw500 + video['poster_path'], 'icon': urlw500 + video['poster_path'], 'fanart': urlw1280 + video['backdrop_path']})
            except:
                foo = 23
            # Set 'IsPlayable' property to 'true'.
            list_item.setProperty('IsPlayable', 'true')
            # Create a URL for a plugin recursive call.
            id = video['id']
            url = get_url(action='play', video=id)
            # Add the list item to a virtual Kodi folder.
            is_folder = False
            # Add our item to the Kodi virtual folder listing.
            xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
            #break

    elif category == 'Acción':
        genre = u'Acción'
        listar(category, showid, genre)

    elif category == 'Aventura':
        genre = 'Aventura'
        listar(category, showid, genre)

    elif category == 'Comedia':
        genre = 'Comedia'
        listar(category, showid, genre)

    elif category == 'Drama':
        genre = 'Drama'
        listar(category, showid, genre)

    elif category == 'Familia':
        genre = 'Familia'
        listar(category, showid, genre)

    elif category == 'Infantil':
        genre = u'Animación'
        listar(category, showid, genre)
    
    elif category == 'Misterio':
        genre = 'Misterio'
        listar(category, showid, genre)

    elif category == 'Terror':
        genre = 'Terror'
        listar(category, showid, genre)

    elif category == 'Destacadas':
        for video in videos:
            try:
                list_item = xbmcgui.ListItem(label=video['movie']['title'])
                list_item.setInfo(
                'video', {'title': video['movie']['title'],'plot': video['movie']['overview'],'rating': video['movie']['vote_average'],'year': video['movie']['release_date'],'votes' : video['movie']['vote_count']}            
                )
                list_item.setArt({'poster': urlw500 + video['movie']['poster_path'], 'icon': urlw500 + video['movie']['poster_path'], 'fanart': urlw1280 + video['movie']['backdrop_path']})
                id = video['movie']['id']
                url = get_url(action='play', video=id)
                is_folder = False
                list_item.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
            except:
                foo = 23
            try:
                list_item = xbmcgui.ListItem(label=video['tvShow']['name'])
                list_item.setInfo(
                'video', {'title': video['tvShow']['name'],'plot': video['tvShow']['overview'],'year': video['tvShow']['first_air_date'],'rating': video['tvShow']['vote_average'],'votes' : video['tvShow']['vote_count']}            
                )
                #list_item.setArt({'poster': 'https://image.tmdb.org/t/p/w500//' + video['tvShow']['poster_path'], 'icon': 'https://image.tmdb.org/t/p/w500//' + video['tvShow']['poster_path'], 'fanart': 'https://image.tmdb.org/t/p/w1280//' + video['tvShow']['backdrop_path']})
                list_item.setArt({'poster': urlw500 + video['tvShow']['poster_path'], 'fanart': ruta_imagenes + 'fanart-1.jpg'})
                id = video['tvShow']['id']
                url = get_url(action='listing', category='Episodes', showid=id)
                is_folder = True
                xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
            except:
                foo = 42

    elif category == 'Buscar':
        if len(videos['shows']) != 0:
            for i in range (0, len(videos['shows'])):
                list_item = xbmcgui.ListItem(label=videos['shows'][i]['name'] + ' - Serie')
                list_item.setArt({'thumb': urlw500 + videos['shows'][i]['poster_path'], 'icon': urlw500 + videos['shows'][i]['poster_path']})
                id = videos['shows'][i]['id']
                url = get_url(action='listing', category='Episodes', showid=id)
                is_folder = True
                xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
        if len(videos['movies']) !=0:
            for i in range (0, len(videos['movies'])):
                list_item = xbmcgui.ListItem(label=videos['movies'][i]['title'])
                list_item.setInfo(
                'video', {'title': videos['movies'][i]['title'],
                'plot': videos['movies'][i]['overview'],'rating': videos['movies'][i]['vote_average']}            
                )
                list_item.setArt({'poster': urlw500 + videos['movies'][i]['poster_path']})
                list_item.setProperty('IsPlayable', 'true')
                id = videos['movies'][i]['id']
                url = get_url(action='play', video=id)
                is_folder = False                
                xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)            
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


def play_video(id):
    # Validate conection
    authentication()
    cookiestring = str(cj).split(" ")
    sessionid = cookiestring[1].split("JSESSIONID=")
    try:
        remember_me = cookiestring[5].split("streama_remember_me=")
    # Get the JSON for the corresponding video from Streama
        movie = opener.open(streamaurl + '/video/show.json?id=' + id)
    # Create the path from resulting info
        movie_json = json.loads(movie.read())
        path = streamaurl + movie_json['files'][0]['src']

    # if path contains streamaurl, append sessionid-cookie and remember_me-cookie for auth
        if path.find(streamaurl) != -1:
            path = path + '|Cookie=JSESSIONID%3D' + sessionid[1] + '%3Bstreama_remember_me%3D' + remember_me[1] + '%3B'
    # Create a playable item with a path to play.
        play_item = xbmcgui.ListItem(path=path)
    # Pass the item to the Kodi player.
        xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)
    except Exception:
        errorconection()


def router(paramstring):
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'listing':
            # Display the list of videos in a provided category.
            list_videos(params['category'], params['showid'])
        elif params['action'] == 'play':
            # Play a video from a provided URL.
            play_video(params['video'])
        else:
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_categories()

def kodiIncludes():
    Includes_Home = xbmc.translatePath('special://home/addons/skin.eminence.2/16x9/Includes_Home.xml')
    xmlconfirm="skin.eminence.2-kodi-8.2" 
    f=open(Includes_Home)  
    contador=f.read()  
    n=contador.count(xmlconfirm)  
    f.close()
    if n == 0:
        os.remove(Includes_Home)
        SrcIncludes_Home = xbmc.translatePath('special://home/addons/plugin.video.streama/addons/skin.eminence.2/Includes_Home.xml')
        SrcIncludes_Furniture = xbmc.translatePath('special://home/addons/plugin.video.streama/addons/skin.eminence.2/Includes_Furniture.xml')
        SrcViewtype_List = xbmc.translatePath('special://home/addons/plugin.video.streama/addons/skin.eminence.2/Viewtype_List.xml')
        DstIncludes_Home = xbmc.translatePath('special://home/addons/skin.eminence.2/16x9/Includes_Home.xml')
        DstIncludes_Furniture = xbmc.translatePath('special://home/addons/skin.eminence.2/16x9/Includes_Furniture.xml')
        DstViewtype_List = xbmc.translatePath('special://home/addons/skin.eminence.2/16x9/Viewtype_List.xml')
        shutil.copy(SrcIncludes_Home, DstIncludes_Home)
        shutil.copy(SrcIncludes_Furniture, DstIncludes_Furniture)
        shutil.copy(SrcViewtype_List, DstViewtype_List)
    else:
        sys.exit

def update_file():
    
    destacadasDATA = xbmc.translatePath('special://home/userdata/addon_data/script.skinshortcuts/destacadas.DATA.xml')
    skinshortcuts = xbmc.translatePath('special://home/userdata/addon_data/script.skinshortcuts/')
    if xbmcvfs.exists(destacadasDATA):
        kodiIncludes()
        sys.exit
    else:
        kodiIncludes()
        shutil.rmtree(skinshortcuts, ignore_errors=True)
        SrcSkinshortcuts = xbmc.translatePath('special://home/addons/plugin.video.streama/addon_data/script.skinshortcuts.eminence')
        DstSkinshortcuts = xbmc.translatePath('special://home/userdata/addon_data/script.skinshortcuts')
        shutil.copytree(SrcSkinshortcuts, DstSkinshortcuts, symlinks=False, ignore=None)

def errorconection():
    failed = xbmcgui.Dialog()
    failed.ok("Error de Autenticación","Comprobar datos de conexión!","")
    sys.exit

def authentication():
    login_data = urllib.urlencode({'username' : username, 'password' : password, 'remember_me' : 'on'})
    opener.open(streamaurl + '/login/authenticate', login_data)

if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    try:
        update_file()       
        router(sys.argv[2][1:])
    except Exception:
        sys.exit