"""
    29/03/2017 - Lorenzo and Nicolas
    This script download all the data from themoviedb and saves it as our dataset
"""

import httplib
import json
#import urllib2
import requests
import os.path
from pprint import pprint

if __name__ == "__main__":

    conn = httplib.HTTPSConnection("api.themoviedb.org")
    payload = "{}"

    #Gets Connection Attributes
    conn.request("GET", "/3/configuration?api_key=287cdab5a6189edf5e200224595a40e0", payload)
    res = conn.getresponse()
    str_res = res.read().decode('utf-8')
    obj = json.loads(str_res)
    #pprint(obj)

    #Base URL
    secure_base_url = obj["images"]["secure_base_url"]
    #Poster_Size
    poster_size = obj["images"]["poster_sizes"][3]

    #creates directories
    try:
        os.mkdir("dataset")
    except Exception:
        pass
    try:
        os.mkdir("dataset/poster")
    except Exception:
        pass

    #Base url
    movie_request_url = "/3/discover/movie?api_key=287cdab5a6189edf5e200224595a40e0&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page="

    moviesIndex = open('dataset/movies.csv', 'w')

    noPoster = 0

    #For each year
    #for year in range(1980, 2017):
    for year in range(2016, 2018):
        print(year)
        #Do the request for the first page of each year
        conn.request("GET", movie_request_url + "1&year=" + str(year), payload)
        res = conn.getresponse()
        str_res = res.read()
        page_obj = json.loads(str_res)
        total_pages = page_obj["total_pages"]

        #print(page_obj.keys())
        #print("TOTAL PAGES: " + str(total_pages))
        #print("TOTAL PAGES: " + str(page_obj["total_results"]))

        #For each page
        for page in range(0, total_pages):
            #Get a page
            conn.request("GET", movie_request_url + str(page) + "&year=" + str(year), payload)
            res = conn.getresponse()
            str_res = res.read().decode('utf-8')
            page_obj = json.loads(str_res)

            if page_obj and page_obj.has_key('results'):

                movies = []

                # For each movie result
                for _ in page_obj['results']:
                    movie = dict({
                        'id': 0,
                        'title': "",
                        'overview': "",
                        'poster_path': ""
                    })

                    if(_.has_key('id')):
                        movie['id'] = _['id']
                    if(_.has_key('title')):
                        movie['title'] = _['title'].encode("utf-8")
                    if(_.has_key('overview')):
                        movie['overview'] = _['overview'].encode("utf-8")
                    if(_.has_key('poster_path') and _['poster_path'] is not None):
                        movie['poster_path'] = _['poster_path'].encode("utf-8")
                        #print(type(_['poster_path']))

                    movies.append(movie)

                    #print(movie['title'])
                    #print(movie['overview'])
                    #print(movie['poster_path'])
                    #print("\n")


                    #If movie has poster
                    if (movie['poster_path'] != ""):
                        #Downloads poster
                        image = requests.get(secure_base_url + poster_size + movie['poster_path']).content

                        if(image != ""):
                            f = open("dataset/poster" + movie['poster_path'] + ".jpg", 'wb')
                            f.write(image)
                            f.close()
                    else:
                        if(movie['overview']):
                            print(movie['title'])
                            print(movie['overview'])
                            noPoster += 1

                for movie in movies:
                    if(movie['overview']):
                        moviesIndex.write(str(movie['id']) +  ";'" + movie['title'] + "';'" + movie['overview'] + "';" + movie['poster_path'] + "\n")
        print(noPoster)
