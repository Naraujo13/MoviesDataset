import http.client
import json
from pprint import pprint



if __name__ == "__main__":
    conn = http.client.HTTPSConnection("api.themoviedb.org")
    payload = "{}"

    conn.request("GET", "/3/configuration?api_key=287cdab5a6189edf5e200224595a40e0", payload)
    res = conn.getresponse()
    data = res.read()


    #breaks data - par1 = base_url, par2 = poster_size, par3 = movie_poster_url
    base_image_url = str(data).split(",")[1].replace("secure_base_url", "").replace("\":", "").replace("\"", "")
    #needs to be changed to get the desired poster image size
    poster_size = "w342"

    movie_request_url = "/3/discover/movie?api_key=287cdab5a6189edf5e200224595a40e0&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page="
    year = 2017
    page = 1

    #for each movie
    conn.request("GET", movie_request_url + str(page) + "&year=" + str(year), payload)
    res = conn.getresponse()
    movie_data = res.read()
    print("movie_data:")
    print(movie_data)

    #movie_poster_url = "/rXBB8F6XpHAwci2dihBCcixIHrK.jpg"

    # print("Data:")
    # print (data)
    # print("Par1:")
    # print(base_image_url)
    # print("Par2:")
    # print(poster_size)
    # print("Par3:")
    # print(movie_poster_url)
    # print("Final Image Url:")
    # print(base_image_url + poster_size + movie_poster_url)