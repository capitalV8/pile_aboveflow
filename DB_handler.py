import psycopg2
from uuid import uuid4
from datetime import datetime
import psycopg2.extras


def connect():
    DBconnection = psycopg2.connect(
        "dbname='wolverine_overflow' host='database' user='username' password='password' port='5432'")
    DBcursor = DBconnection.cursor()
    DBconnection.autocommit = True
    return DBconnection, DBcursor


DBconnection, DBcursor = connect()  # not good, should be in other file.
psycopg2.extras.register_uuid()


def check_if_exists(table, column, val):
    DBcursor.execute("""SELECT EXISTS(
        SELECT 1 FROM {} WHERE {} = '{}'
         LIMIT 1);""".format(table, column, val))
    return DBcursor.fetchone()[0]


def DBexec(query, vals):
    DBcursor.execute(query, vals)
    try:
        return DBcursor.fetchone()
    except:
        return None


def DBselect(table, column):
    DBcursor.execute("SELECT {} FROM {};".format(column, table))
    return DBcursor.fetchone()


def DBinsert(table, columns, vals):
    DBcursor.execute("""INSERT INTO {}({})
                     VALUES(%s);
                     """.format(table, columns), vals)


def DBnewtable(table_name):
    DBcursor.execute("CREATE TABLE {}();".format(table_name))


def DBdrop_column(table_name, column_name):
    DBcursor.execute("""ALTER TABLE {}
                     DROP COLUMN {};""".format(table_name, column_name))


def DBnewcolumn(table_name, column_name, type):
    DBcursor.execute("""ALTER TABLE {}
                     ADD {} {}""".format(table_name, column_name, type))
    return DBcursor.fetchall()


def get_user(username, password):
    DBcursor.execute("""
        SELECT password, id FROM users WHERE username = %s AND password = %s;
        """, (username, password))
    return DBcursor.fetchone()  # [0] means it returns only tuple of password, id.


def get_user_by_id(id):
    DBcursor.execute("""
        SELECT username, firstname, lastname FROM users WHERE id = %s;
        """, (id,))
    return DBcursor.fetchone()

def get_short_posts(page_number):
    DBcursor.execute(f"""
                     SELECT title, postuser, LEFT(content, 50), creationtime
                     FROM posts ORDER BY creationtime LIMIT 15 OFFSET {(page_number-1)*15}""")
    return DBcursor.fetchall()


def get_comments(post_id):
    DBcursor.execute("""SELECT comments.content, commentuser
        FROM posts
        INNER JOIN comments ON comments.postid = posts.postid;""")
    return DBcursor.fetchall()



def get_posts(page_number):
    DBcursor.execute(
        f"SELECT * FROM posts ORDER BY creationtime LIMIT 15 OFFSET {(page_number-1)*15}")
    return DBcursor.fetchall()


def get_post(post_id):
    DBcursor.execute(
        "SELECT title, content, user FROM posts WHERE postid = %s", (post_id,))
    return DBcursor.fetchone()




def disconnect():
    DBcursor.close()
    DBconnection.close()


def create_default_table():
    DBcursor.execute("""
                     CREATE TABLE users (
                        username VARCHAR(31),
                        password VARCHAR(31),
                        mail VARCHAR(127),
                        name VARCHAR(31),
                        id UUID,
                        creationtime DATE,
                        firstname TEXT, 
                        lastname TEXT,
                        CONSTRAINT primaryk PRIMARY KEY (username)
                     );
                     """)

def alter_like_comment(comment_id, add_like, user): # TODO: can this and add_like_post be done in one?
    """ If add_like is True, adds a like, reduces if False. """
    action = lambda num: "+ 1 " if add_like else "- 1"
    if check_user_liked_comments(user):
        DBcursor.execute("UPDATE comments SET likes = likes %s, users_liked = array_append(users_liked, %s) WHERE commentid = %s", (action, user, comment_id))


def check_user_liked(user):
    DBcursor.execute("""SELECT EXISTS (SELECT 1 FROM posts WHERE users_liked @> ARRAY[%s]::varchar[]);""", user)
    return DBcursor.fetchone()[0]


def check_user_liked_comments(user):
    DBcursor.execute("""SELECT EXISTS (SELECT 1 FROM posts WHERE users_liked @> ARRAY[%s]::varchar[]);""", user)
    return DBcursor.fetchone()[0]



def alter_like_post(post_id, add_like, user):
    """ If add_like is True, adds a like, reduces if False. """

    action = lambda num: "+ 1 " if add_like else "- 1"
    if check_user_liked(user):
        DBcursor.execute("UPDATE posts SET likes = likes %s, users_liked = array_append(users_liked, %s) WHERE postid = %s", (action, user, post_id))


def create_posts_table():
    DBcursor.execute("""
    CREATE TABLE posts(
        postid UUID,
        content TEXT,
        likes INTEGER, 
        title TEXT,
        postuser VARCHAR(31),
        creationtime TIMESTAMP,
        users_liked VARCHAR(31)[],
        PRIMARY KEY (postid)
    );
    """)


def create_post(post_id, content, username, title, creation_time):
    DBcursor.execute("INSERT INTO posts(postid, content, postuser, title, creationtime, likes) VALUES(%s, %s, %s, %s, %s, 0)",
                     (post_id, content, username, title, creation_time))


def get_likes_post(post_id):
    DBcursor.execute("SELECT likes FROM posts WHERE postid = %s", (post_id,))
    return DBcursor.fetchone()


def get_likes_comment(comment_id):
    DBcursor.execute("SELECT likes FROM posts WHERE postid = %s", (comment_id,))
    return DBcursor.fetchone()



def auto_create_post():
    create_post(uuid4(), "this is a post", "Bobby",
                "title for post", datetime.now())
                


def create_comment(comment_id, post_id, content, username, creation_time):
    DBcursor.execute("INSERT INTO comments(commentid, postid, content, commentuser, creationtime, likes) VALUES(%s, %s, %s, %s, %s, 0)",
                     (comment_id, post_id, content, username, creation_time))


def create_comments_table():
    DBcursor.execute("""
    CREATE TABLE comments(
        postid UUID,
        commentid UUID,
        content TEXT,
        likes INTEGER,
        commentuser VARCHAR(31),
        creationtime TIMESTAMP,
        users_liked VARCHAR(31)[],
        CONSTRAINT postfkey
            FOREIGN KEY(postid)
                REFERENCES posts(postid)
    );
                    """)


def init_tables():
    print("shut up, bub!")
    try:
        create_posts_table()
        create_default_table()
        create_comments_table()

    except:
        pass
