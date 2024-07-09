import psycopg2


#import docker
#client = docker.DockerClient()
#container = client.containers.get("wolverine_overflow-database-1")
#IP = container.attrs['NetworkSettings']['IPAddress']

def connect():
    DBconnection = psycopg2.connect("dbname='postgres' host='database' user='username' password='password' port='5432'")
    DBcursor = DBconnection.cursor()

#IMPORTANT use docker init scripts
connect()

def DBselect(table, column):
    DBcursor.execute("SELECT {} FROM {};".format(column,table))

def DBinsert(table, column, val):
    DBcursor.execute("""INSERT INTO {} ({}) \
                     VALUES('{}');
                     """.format(table, column, val))

def DBnewtable(table_name):
    DBcursor.execute("CREATE TABLE {}();".format(table_name))


def DBdrop_column(table_name, column_name):
    DBcursor.execute("""ALTER TABLE {}
                     DROP COLUMN {};""".format(table_name, column_name))

def DBnewcolumn(table_name, column_name, type):
    DBcursor.execute("""ALTER TABLE {}
                     ADD {} {}""".format(table_name, column_name, type))

print("s")

def update():
    DBconnection.commit()

def disconnect():
    DBcursor.close()
    DBconnection.close()


#print(DBcursor.fetchall())
#DBconnection.commit()


#print(DBcursor.execute("SELECT * FROM thing"))

#DBcursor.execute("""INSERT INTO thing(thingcolumn, thingcolumn2)
#                 VALUES('hello', 'hello2');
#                 """)


#DBconnection = psycopg2.connect("dbname='new_testdb' user='dbuser' host='localhost' password='Bsmch@500K!'")


#DBcursor.execute("""UPDATE thing
#                 SET thingcolumn = 'hello';
#                 
#                 
#                 """)
