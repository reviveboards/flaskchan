import os
import psycopg2

def get_db_conn():
    db_conn = psycopg2.connect(
        host="localhost",
        database="flaskchan",
        user="postgres",
        password="SoundsLikeShit")

    return db_conn

