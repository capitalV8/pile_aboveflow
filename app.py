from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import DB_handler
from datetime import datetime
from uuid import uuid4

# TODO: use aborts instead of returning weird stuff 
# TODO: check if user inputs is valid on client side.

DB_handler.init_tables()
app = Flask(__name__, template_folder='templates2', static_folder='static')

app.config["SECRET_KEY"] = b'f\xe9\x04\xc702\xc5\n\x83)\xe6\x1e1\xfe\x879\xc79a\xf6T\xce\x9a\xca'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'get_login'


class Users(UserMixin):

    def get_username(self): #TODO: i dont think this is neccesary.
        return self.username


    def __init__(self, uname, pword, ID):
        self.username = uname
        self.password = pword
        self.id = ID


def create_post(content, username, title, ):
    DB_handler.create_post(uuid4(), content, username, title, datetime.now())


def create_comment(post_id, content, username, creation_time):
    DB_handler.create_comment(
        uuid4(), post_id, content, username, creation_time)


@login_manager.user_loader
def loader_user(user_id):
    uname = DB_handler.get_user_by_id(user_id)[0]
    return Users(uname, "b" , user_id) # TODO: this


@app.route('/posts/<string:page_number>') #TODO: this
def get_posts(page_number):
    if len(page_number) > 5: # This means that the request is for a specific post, not multiple posts. TODO: better implementation?
        title, content, user, creation_time =  DB_handler.get_post(page_number)
        comments = DB_handler.get_comments(page_number)
        likes = DB_handler.get_likes_post(page_number)[0]
        return render_template('post 3.html', title = title, post_content = content, username = user, creation_time = creation_time, likes = likes,
                           comments = comments, CONTENT = 0, USERNAME = 1, CREATION_TIME = 2, ID = 3, LIKES = 4)
    # Code from here on is for getting a page of posts.
    try:
        posts = DB_handler.get_short_posts(page_number)
    except:
        return "invalid url!"
    return render_template('posts.html', posts = posts, TITLE = 0, USERNAME = 1, CONTENT = 2, DATE = 3, ID = 4)






@app.route('/posts/<string:post_id>', methods=['POST']) #TODO: connect with html
def post_post(post_id):


    if "answer" in request.form.keys():
        reply = request.form['answer']
        DB_handler.create_comment(uuid4(), post_id, reply, current_user.username, datetime.now())
    else:
        is_like = request.form['like']
        print(is_like)
        try:
            username = current_user.username
        except:
            return "log in to like posts!"
        comment_id = request.form['comment_id']
        if is_like == "like": #TODO: lambda this
            is_like = True
        else:
            is_like = False
        if comment_id == "0":
            DB_handler.alter_like_post(post_id, is_like, username)
        else:
            DB_handler.alter_like_comment(comment_id, is_like, username)
        return "success"
    return "success2"





@app.route('/')
@login_required
def get_home():
    posts = DB_handler.get_short_posts(1)
    return render_template('home 3.html', posts=posts, TITLE = 0, USERNAME = 1, CONTENT = 2, DATE = 3, ID = 4)

@app.route('/home')
@login_required
def get_home2():
    return render_template('home 3.html', )

@app.route('/', methods=['POST'])
@login_required
def post_home():
    post_content = request.form["post content"]
    post_title = request.form["post title"]
    DB_handler.create_post(uuid4(), post_content, current_user.username, post_title, datetime.now())
    return "Uploaded question!"


@app.route('/signup')
def get_signup():
    return render_template('signup.html')


@app.route('/pass_reset')
def get_pass_reset():
    return render_template('pass_reset.html')


@app.route('/profile')
def get_profile():
    return render_template('profile.html')

@app.route('/profile/<string:user_id>') #TODO: this, add bio?
def get_user_profile(user_id):
    user = DB_handler.get_user_by_id(user_id)
    return render_template('profile.html', username = user[0], firstname = user[1], lastname = user[2])


@app.route('/logoff')  # TODO add frontend
def logoff():
    logout_user()
    return (redirect(url_for('get_home')))



@app.route('/signup', methods=['POST'])
def handle_signup_post():

    if request.method == 'POST':
        uname = request.form['uname']
        pword = request.form['pass']
        email = request.form['email']
        retype_pword = request.form['rpass']
        name = request.form['name']

        if DB_handler.check_if_exists("users", "username", uname):
            return "username already taken! please use another username."
        elif len(uname) > 30 or len(pword) > 30:
            return "username or password is too long!"
        elif pword != retype_pword:
            return "password not identical in both fields."
        else:
            DB_handler.DBexec(
                "INSERT INTO users(username, password, mail, name, id, creationtime) VALUES (%s, %s, %s, %s, %s, %s)", (uname, pword, email, name, uuid4(), datetime.now()))
            return "you're signed up!."

@app.route('/login')
def get_login():
    return render_template('login.html')


@app.route('/secret')
@login_required
def get_secret():
    post_list = [item for post in DB_handler.get_short_posts(
        1) for item in post]
    return render_template('secret.html', postlist=post_list, username=current_user.username)


#create_comment('d43fbb15-9877-40c9-99fc-00f8b736a3b2', "stupid question", "commenter", datetime.now())
#create_comment('d43fbb15-9877-40c9-99fc-00f8b736a3b2', "very stupid question", "commenter2", datetime.now())


@app.route('/login', methods=['POST'])
# function for incoming post requests.
def handle_login_post():
    if request.method == 'POST':
        uname = request.form['uname']
        pword = request.form['pass']
        try:
            password, id = DB_handler.get_user(uname, pword)
        except:
            return "incorrect username or password!"

        if password != None:
            login_user(Users(uname, password, id))
            return (redirect(url_for('get_home')))
        else:
            return (redirect(url_for('get_signup')))

            # SELECT password FROM users WHERE username = username
            # AND

            # return redirect(url_for("home"))

#        DB_handler.DBinsert("hello, col, testeroftheages")

        # return whatever is needed in the situation.


#@app.route('/')
#def handle_get():
#    return render_template(...)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
