from flask_mysqldb import MySQL
from flask import Flask
import redis

mysql = MySQL()
redis_conn = redis.Redis()
redis_client = redis.StrictRedis(
    host="localhost",
    port=6379,
    decode_responses=True
)

def init_mysql_database(server: Flask):
    mysql.init_app(server)