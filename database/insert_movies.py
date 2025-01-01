# import
from mysql.connector import connect

# Connect to db
db_connection = connect(
    host="localhost",
    user="root",
    password="your_new_password",
    database="movies_api",
)

# create a cursor
cursor = db_connection.cursor()
if not cursor: print("No connection!")

# Run a for loop
query = """
INSERT INTO movies (title, genre, director, year, rating)
VALUES (%s, %s, %s, %s, %s);
"""
movies = [
    {
        "id": 101,
        "title": "Inception",
        "genre": "Action",
        "director": "Christopher Nolan",
        "year": 2010,
        "rating": 8.8
    },
    {
        "id": 102,
        "title": "Interstellar",
        "genre": "Sci-Fi",
        "director": "Christopher Nolan",
        "year": 2014,
        "rating": 8.6
    },
    {
        "id": 103,
        "title": "The Dark Knight",
        "genre": "Action",
        "director": "Christopher Nolan",
        "year": 2008,
        "rating": 9.0
    },
    {
        "id": 104,
        "title": "Avatar",
        "genre": "Sci-Fi",
        "director": "James Cameron",
        "year": 2009,
        "rating": 7.8
    },
    {
        "id": 105,
        "title": "Titanic",
        "genre": "Drama",
        "director": "James Cameron",
        "year": 1997,
        "rating": 7.9
    },
    {
        "id": 106,
        "title": "The Matrix",
        "genre": "Action",
        "director": "Lana Wachowski",
        "year": 1999,
        "rating": 8.7
    },
    {
        "id": 107,
        "title": "John Wick",
        "genre": "Action",
        "director": "Chad Stahelski",
        "year": 2014,
        "rating": 7.9
    },
    {
        "id": 108,
        "title": "Mad Max: Fury Road",
        "genre": "Action",
        "director": "George Miller",
        "year": 2015,
        "rating": 8.1
    },
    {
        "id": 109,
        "title": "Dune",
        "genre": "Sci-Fi",
        "director": "Denis Villeneuve",
        "year": 2021,
        "rating": 8.3
    },
    {
        "id": 110,
        "title": "The Shawshank Redemption",
        "genre": "Drama",
        "director": "Frank Darabont",
        "year": 1994,
        "rating": 9.3
    }
]

try:
    db_connection.start_transaction()
    for movie in movies:
        cursor.execute(query, (movie["title"].lower(), movie["genre"].lower(), movie["director"].lower(), movie["year"], movie["rating"]))           
except Exception as e:
    db_connection.rollback()
    print(e)    

# close cursor and db
db_connection.commit()
cursor.close()
db_connection.close()