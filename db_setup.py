import psycopg2
import functools
from config import *

#create table decorator
def create_table(query):
    @functools.wraps(query)
    def connect_run_close():
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            for sql in query():
                cur.execute(sql)
            conn.commit()
            msg = cur.statusmessage
            #print msg
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print error
        finally:
            if conn is not None:
                conn.close()
                #print('Database connection ended.')
    return connect_run_close


#table query
@create_table
def create_table():
    query = ["""
            CREATE TABLE baby_names(
            rank SERIAL PRIMARY KEY,
            male_name VARCHAR(100) NOT NULL,
            female_name VARCHAR(100) NOT NULL
            )
    """]
    return query


if __name__ == '__main__':
    create_table()
