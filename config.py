from flask import Flask

# Basic schema:
# Users: id, name, preferences (JSON or text), rating_history (JSON or text)
# Movies: id, title, genre, director, year, rating
# Recommendations (optional): id, user_id, movie_list (JSON or text), timestamp

def create_app():
    server = Flask(__name__)
    server.config["MYSQL_HOST"] = "localhost"
    server.config["MYSQL_USER"] = "root"
    server.config["MYSQL_PASSWORD"] = "your_new_password"
    server.config["MYSQL_DB"] = "movies_api"

    return server