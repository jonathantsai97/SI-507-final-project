import requests
import pandas as pd
import bs4
import json
import webbrowser
import api_key

class Movie:
    def __init__(self, title, year, genre, imdb_rating, box_office, plot):
        self.title = title
        self.year = year
        self.genre = genre
        self.imdb_rating = imdb_rating
        self.box_office = box_office
        self.plot = plot

class Node:
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)



def fetch_data(json_cache, movie_list):
    """
    Accepts a list of movie names, fetches the data from the OMDB API and stores it in a json file. If the json file already exists, it reads the data from the json file and returns it.

    Parameters:
        json_cache (str): name of the json file
        movie_list (list): list of movie names that are to be fetched from the OMDB API
    Returns:
        list: list of dictionaries containing the data of all movies
    """
    try:
        with open(json_cache, 'r') as file_obj:
            data = json.load(file_obj)
            print('Using cached data...')
            return data

    except FileNotFoundError:
        print('Fetching data...')
        url = f'http://www.omdbapi.com/?apikey={api_key.KEY}&t='
        data = []
        for movie in movie_list:
            transformed_movie = movie.lower().replace(' ', '+')
            response = requests.get(url + transformed_movie)
            data.append(response.json())
        with open(json_cache, 'w') as file_obj:
            json.dump(data, file_obj, indent=4)

        return data

def get_wiki_data(url):
    """
    Accepts a url, get the web data and turn them into beautiful soup objects. Extract only the wikitables and turn them into pandas dataframes. Parse the dataframes and return a list of all movies that won/were nominated for Oscars Best Picture.
    """
    response = requests.get(url)
    html = response.text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table', {'class': "wikitable"})[:-1] # drop the last table because it doesn't contain movie nominees/winners
    dataframes = []
    df = pd.read_html(str(tables))
    for dataframe in df:
        dataframes.append(dataframe)
    for dataframe in dataframes:
        dataframe.columns = dataframe.iloc[0] # set the first row as the column names
    data = []
    for dataframe in dataframes:
        data.append(dataframe.iloc[:, 1].tolist())  # extract the data from second column (movie names) of all dataframes and store it in a list of lists
    for i in range(len(data)):
        data[i] = [x for x in data[i] if str(x) != 'nan'] # remove nan of each list in the list of lists
    movie_list = [item for sublist in data for item in sublist] # flatten the list of lists

    return movie_list

def convert_genre_into_list(data):
    """
    Accepts a data (list of dictionaries), converts the genre string into a list and returns the updated list of dictionaries. If the genre is not available (movie was not found from OMDB API), it returns an empty list.
    """
    for movie in data:
        try:
            movie['Genre'] = movie['Genre'].split(', ')
        except:
            movie['Genre'] = []
    return data

def convert_year(data):
    """
    Accepts a data (list of dictionaries), converts the year string into an integer and returns the updated list of dictionaries. If the year is not available (movie was not found from OMDB API), it returns 0.
    """
    for movie in data:
        try:
            movie['Year'] = int(movie['Year'])
        except:
            movie['Year'] = 0
    return data

def covert_title(data):
    """
    Accepts a data (list of dictionaries), if the title is not available (movie was not found from OMDB API), it returns an empty string.
    """
    for movie in data:
        try:
            movie['Title'] = str(movie['Title'])
        except:
            movie['Title'] = ''

    return data

def delete_error_movies(data):
    """
    Accepts a data (list of dictionaries), removes the movies that were not found from OMDB API and returns the updated list of dictionaries.
    """
    for movie in data:
        if movie['Title'] == '':
            data.remove(movie)
    return data

def convert_imdb_rating(data):
    """
    Accepts a data (list of dictionaries), converts the imdb rating string into a float and returns the updated list of dictionaries. If the imdb rating is not available (movie was not found from OMDB API) or N/A, it returns 0.
    """
    for movie in data:
        try:
            movie['imdbRating'] = float(movie['imdbRating'])
        except:
            movie['imdbRating'] = 0
    return data

def convert_box_office(data):
    """
    Accepts a data (list of dictionaries), converts the box office string into an integer and returns the updated list of dictionaries. If the box office is not available (movie was not found from OMDB API) or N/A, it returns 0.
    """
    for movie in data:
        try:
            movie['BoxOffice'] = int(movie['BoxOffice'].replace('$', '').replace(',', ''))
        except:
            movie['BoxOffice'] = 0
    return data

def convert_plot(data):
    """
    Accepts a data (list of dictionaries), if the plot is not available (movie was not found from OMDB API), it returns an empty string.
    """
    for movie in data:
        try:
            movie['Plot'] = str(movie['Plot'])
        except:
            movie['Plot'] = ''

    return data

def convert_imdb_id(data):
    """
    Accepts a data (list of dictionaries), if the imdb id is not available (movie was not found from OMDB API), it returns an empty string.
    """
    for movie in data:
        try:
            movie['imdbID'] = str(movie['imdbID'])
        except:
            movie['imdbID'] = ''

    return data

def get_all_genres(data):
    """
    Accepts a data (list of dictionaries), returns a list of all genres.
    """
    genres = []
    for movie in data:
        genres.extend(movie['Genre'])
    genres = list(set(genres))
    return genres

def find_max_and_min_imdb_rating(data):
    """
    Accepts a data (list of dictionaries), returns the max and min imdb rating as a tuple.
    """
    imdb_ratings = []
    for movie in data:
        if movie['imdbRating'] != 0:
            imdb_ratings.append(movie['imdbRating'])
    return (max(imdb_ratings), min(imdb_ratings))

def find_duplicate_movies_in_json(file):
    """
    Accepts a json file, returns a list of duplicate movies.
    """
    with open(file, 'r') as f:
        data = json.load(f)
    movies = []
    for movie in data:
        try:
            movies.append(movie['Title'])
        except:
            pass
    duplicates = []
    for movie in movies:
        if movies.count(movie) > 1:
            duplicates.append(movie)
    return duplicates




if __name__ == "__main__":
    cache_file = 'movie_cache.json'

    wikiurl = 'https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture'
    movie_list = get_wiki_data(wikiurl)


    # clean the movie list before creating Movie objects
    data = fetch_data(cache_file, movie_list)
    data = convert_genre_into_list(data)
    data = convert_year(data)
    data = covert_title(data)
    data = delete_error_movies(data)
    data = convert_imdb_rating(data)
    data = convert_box_office(data) # there are too many 0s in the box office data, so I decided to not use this attribute to filter my movie recommendation
    data = convert_plot(data)

    all_genres = ['Mystery', 'Film-Noir', 'Sci-Fi', 'Western', 'Romance', 'Music', 'Animation', 'Thriller', 'Crime', 'History', 'Biography', 'Family', 'Adventure', 'Sport', 'Drama', 'Documentary', 'Action', 'Musical', 'Horror', 'Short', 'Comedy', 'War', 'Fantasy']

    imdb_rating_category = ['5-6', '6-7', '7-8', '8-9', '9-10']

    year_category = ['1927-1937', '1938-1948', '1949-1959', '1960-1970', '1971-1981', '1982-1992', '1993-2003', '2004-2014', '2015-2022']

    # print(set(find_duplicate_movies_in_json(cache_file))) - 9 movies are duplicated in the json file

    # create Movie objects and store them in a list called "movies"
    movies = []
    for movie in data:
        movies.append(Movie(movie['Title'], movie['Year'], movie['Genre'], movie['imdbRating'], movie['BoxOffice'], movie['Plot']))


    # create a tree structure
    # first layer of tree would be genre, second layer would be imdb rating, third layer would be year
    root = Node('root')
    for genre in all_genres:
        genre_node = Node(genre)
        root.add_child(genre_node)
        for imdb_rating in imdb_rating_category:
            imdb_rating_node = Node(imdb_rating)
            genre_node.add_child(imdb_rating_node)
            for year in year_category:
                year_node = Node(year)
                imdb_rating_node.add_child(year_node)
                for movie in movies:
                    # the movie should be in the genre, the imdb rating should be in the range, the year should be in the range, and the movie should not be already in the year node's children (prevent duplicates for the 9 duplicated movies)
                    if genre in movie.genre and movie.imdb_rating >= float(imdb_rating.split('-')[0]) and movie.imdb_rating <= float(imdb_rating.split('-')[1]) and movie.year >= int(year.split('-')[0]) and movie.year <= int(year.split('-')[1]) and movie.title not in [child.title for child in year_node.children]:
                        year_node.add_child(movie)

    # Greet the user
    print('Welcome to the movie recommendation system!')

    # Ask the user to choose a genre, a year range, and a imdb Rating range. Search the tree and return a list of movies that match the user's choices.
    genre = input(f'Choose a genre in {all_genres}: ')
    imdb_rating_range = input(f'Choose a imdb rating range in {imdb_rating_category}: ')
    year_range = input(f'Choose a year range in {year_category}: ')

    for child in root.children:
        if genre == child.data:
            genre_node = child

    for child in genre_node.children:
        if imdb_rating_range == child.data:
            imdb_rating_node = child

    for child in imdb_rating_node.children:
        if year_range == child.data:
            year_node = child

    print('This is your movie recommendation:')
    recommendation = [movie for movie in year_node.children]
    if len(recommendation) == 0:
        print('Sorry, there is no movie that matches your choices.')
    else:
        print(f'There are {len(recommendation)} movies that match your choices:')
        for i in range (len(recommendation)):
            print(f'{i+1}. {recommendation[i].title}')
        movie_to_show = input('Which movie do you want to see the details? We will provide you the plot and a website preview of the movie. Please enter the number of the movie: ')
        print(f'Here is the plot: {recommendation[int(movie_to_show)-1].plot}')
        for movie in data:
            if recommendation[int(movie_to_show)-1].title == movie['Title']:
                imdb_id = movie['imdbID']
                url = f'https://www.imdb.com/title/{imdb_id}/'
        print(f'Here is the website preview: ')
        webbrowser.open(url, new=2)








