# SI-507-final-project
my final project - movie filter system 


This is a movie filter system that asks for users' preference and according to their preferences, recommend them Oscar Best Picture nominees or winners they can watch.

I created a class "Movie," scrape one Wikipedia page and extract the titles of every Oscar Best picture nominee and winner, and store the titles and in class object attribute.  Then I queried the OMDB API using movie titles, store more information like genre, year, ratings etc for each movie and again, store them into more "Movie" object attributes.  

After constructing the “Movie” objects, I built a three layer tree to filter the movie results for users. The first layer will ask users for a "genre" they want, second layer for a range of "imdb rating," third layer for a range of "released year".

API key:
This code uses OMDB API to get information for movies. However, this code also uses caching to store the retrieved API data. I have uploaded the "movie_cache.json" file, which is the cache file that this code uses. If this cache file is present, you don't need the API key to run the code. But if you want to call the API on your own, you will need to create a python file "api_key.py" and in it, there must be a string called "KEY" that has your OMDB API key. 

To obtain OMDB API key, go to https://www.omdbapi.com/apikey.aspx and generate your API key. 

Required packages: 
- requests
- pandas
- bs4
- api_key.py -> create this if you want to call the API instead of using the cache file I provided


How to interact with this code: 
The program will ask users 3 questions: the genre you want, the range of imdb rating, the range of year the movies were released. The allowed answers for each question is provided in the question. Don't include quotation marks, but type exactly as it appears in the question (e.g., capitalize first letter in genre, include dash in ranges) 
