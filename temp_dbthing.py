import psycopg2
def connect():
    DBconnection = psycopg2.connect("dbname='wolverine_overflow' host='127.0.0.1' user='username' password='password' port='5433'")
    DBcursor = DBconnection.cursor()
    return DBconnection, DBcursor

DBconnection, DBcursor = connect() # not good, should be in other file.


def create_default_table():
    DBcursor.execute("""
                     CREATE TABLE users (
                        username VARCHAR(31),
                        password VARCHAR(31),
                        mail VARCHAR(127),
                        CONSTRAINT primaryk PRIMARY KEY (username)
                     );
                     """)
    
create_default_table()
    
DBconnection.commit()
DBconnection.close()
DBcursor.close()