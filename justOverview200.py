import csv


movies = []

f = open('dataset/moviesUnique.csv')

for row in f:
    row = row.split(";")
    movieId = row[0]
    movieTitle = (row[1])[1:-1]
    movieCover = row[-1].replace("\n", "")
    movieOverview = (", ".join(row[2:-1]))[1:-1].replace(",", "").replace("\n", "").replace("\"", "")

    if(len(movieOverview) <= 200 and ("no overview" not in movieOverview.lower()) and movieCover != "" and movieCover != None and len(movieCover) > 0):
        movies.append([movieId, movieTitle, movieOverview, movieCover])

movies200TXT = open('dataset/movies200.txt', 'w')
movies200CSV = open('dataset/movies200.csv', 'w')
movies200CoverOverview = open('dataset/movies200CoverOverview.csv', 'w')

for movie in movies:
    movies200TXT.write(movie[2] + "\n")
    movies200CSV.write(";".join(movie))
    #movies200CoverOverview.write("\"poster" + movie[3] + "\";\"" + movie[2] + "\"\n")
    movies200CoverOverview.write("poster" + movie[3] + "," + movie[2] + "\n")
    #movies200CoverOverview.write(movie[3] + ";")
