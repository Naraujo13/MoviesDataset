import http.client
import json
from pprint import pprint



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


    movie_request_url = "/3/discover/movie?api_key=287cdab5a6189edf5e200224595a40e0&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page="
    for year in range(1980, 2017):
        conn.request("GET", movie_request_url + "1&year=" + str(year), payload)
        res = conn.getresponse()
        str_res = res.read().decode('utf-8')
        page_obj = json.loads(str_res)
        total_pages = page_obj["total_pages"]
        #Itera entre páginas
        for page in range(1, total_pages):
            conn.request("GET", movie_request_url + str(page) + "&year=" + str(year), payload)
            res = conn.getresponse()
            str_res = res.read().decode('utf-8')
            page_obj = json.loads(str_res)
            #Itera entre resultados da página
            i = 0
            if page_obj and page_obj["results"]:
                for movie in page_obj["results"]:
                    pprint(movie["title"] + " Movie " + str(i) + " - Page " + str(page))
                    i = i + 1



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