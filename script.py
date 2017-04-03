"""
    29/03/2017 - Lorenzo and Nicolas
    This script download all the data from themoviedb and saves it as our dataset
"""

import httplib
import json
import requests
import os.path
from subprocess import call

def fetch_movies(first_year, last_year, total_movies, total_noPoster):
    current_year = first_year

    try:
        #For each year
        for year in range(first_year, last_year):
            current_year = year
            print(str(year) + ":")

            #Do the request for the first page of each year
            #conn.set_debuglevel(1)
            conn = httplib.HTTPSConnection("api.themoviedb.org")
            request_url = movie_request_url + "1&year=" + str(year);
            conn.request("GET", request_url.replace("\n", ""), payload)
            res = conn.getresponse()
            str_res = res.read()
            page_obj = json.loads(str_res)
            noPoster = 0

            movies = [] #list with all the movies from an year

            if page_obj and page_obj.has_key('total_pages') and page_obj.has_key('total_results'):

                total_pages = page_obj["total_pages"]
                total_results = page_obj["total_results"]

                #print(page_obj.keys())
                #print("TOTAL PAGES: " + str(total_pages))
                #print("TOTAL RESULTS: " + str(total_results))

                #For each page
                for page in range(1, total_pages):
                    #print(page)
                    #Get a page
                    #conn.set_debuglevel(1)
                    request_url = movie_request_url + str(page) + "&year=" + str(year)
                    conn.request("GET", request_url, payload)
                    res = conn.getresponse()
                    str_res = res.read().decode('utf-8')
                    page_obj = json.loads(str_res)

                    #print(request_url)

                    if page_obj and page_obj.has_key('results'):
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

                            #print(movie['title'])
                            movies.append(movie)

            #verify if a movie has overview and downloads its poster and saves it in a csv file
            for movie in movies:
                if(movie['overview']):
                    attempt = 0
                    while attempt < 3:
                        try:
                            #If movie has poster
                            if (movie['poster_path'] != ""):
                                #Downloads poster
                                image = requests.get(secure_base_url + poster_size + movie['poster_path'], timeout=1).content

                                if(image != ""):
                                    f = open("dataset/poster" + movie['poster_path'], 'wb')
                                    f.write(image)
                                    f.close()
                            else:
                                    noPoster += 1

                            moviesIndex.write(str(movie['id']) +  ";'" + movie['title'] + "';'" + movie['overview'] + "';" + movie['poster_path'] + "\n")
                            attempt = 3
                        except Exception, e:
                            attempt = attempt + 1
                            print(e)

            print("\tMovies with poster: " + str(total_results - noPoster) + "/" + str(total_results))
            total_movies += total_results
            total_noPoster += noPoster

    except Exception as e:
        print(repr(e))
        return current_year

    return last_year

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
    movie_request_url = "/3/discover/movie?api_key=287cdab5a6189edf5e200224595a40e0&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&with_genres=16&page="

    moviesIndex = open('dataset/movies.csv', 'w')

    total_movies= 0
    total_noPoster = 0
    #first_year = 1892
    first_year = 2003
    #last_year = 2018
    last_year = 2005
    stopped_year = first_year

    while stopped_year != last_year:
        print("Starting to fetch movies from " + str(first_year) + " to " + str(last_year))
        first_year = stopped_year
        stopped_year = fetch_movies(first_year, last_year, total_movies, total_noPoster)
        print("Stopped at: " + str(stopped_year))

    print("Total Movies with Poster: " + str(total_movies - total_noPoster) + "/" + str(total_movies))

    #remove duplicates in the csv file, those are caused because of an api problem
    call(['sort', '-u', 'dataset/movies.csv', '-o', 'dataset/moviesUnique.csv'])
