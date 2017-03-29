import http.client
import json
from pprint import pprint
import urllib.request
import os.path



if __name__ == "__main__":


    conn = http.client.HTTPSConnection("api.themoviedb.org")
    payload = "{}"

    #Gets Connection Attributes
    conn.request("GET", "/3/configuration?api_key=287cdab5a6189edf5e200224595a40e0", payload)
    res = conn.getresponse()
    str_res = res.read().decode('utf-8')
    obj = json.loads(str_res)
    pprint(obj)

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
    try:
        os.mkdir("dataset/overview")
    except Exception:
        pass

    movie_request_url = "/3/discover/movie?api_key=287cdab5a6189edf5e200224595a40e0&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page="
    #For each year
    for year in range(1980, 2017):
        conn.request("GET", movie_request_url + "1&year=" + str(year), payload)
        res = conn.getresponse()
        str_res = res.read().decode('utf-8')
        page_obj = json.loads(str_res)
        total_pages = page_obj["total_pages"]
        #For each page
        for page in range(1, total_pages):
            conn.request("GET", movie_request_url + str(page) + "&year=" + str(year), payload)
            res = conn.getresponse()
            str_res = res.read().decode('utf-8')
            page_obj = json.loads(str_res)
            i = 0
            if page_obj and page_obj["results"]:
                # For each movie result
                for movie in page_obj["results"]:
                    print(movie["title"] + " Movie " + str(i) + " - Page " + str(page))
                    i = i + 1
                    poster_path = movie["poster_path"]
                    #If movie has poster
                    if (poster_path):
                        movie_id = str(movie["id"])
                        #Downloads poster
                        urllib.request.urlretrieve(secure_base_url + poster_size + poster_path, "dataset/poster/" + movie_id + ".jpg")
                        #Downloads overview
                        overview_file = open(movie_id + ".txt", "w")
                        overview_file.write("overview/poster/" + str(movie["overview"]))
                        overview_file.close()