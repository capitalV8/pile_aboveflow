from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import DB_handler
from datetime import datetime
from uuid import uuid4

# DB_handler.init_tables()
app = Flask(__name__, template_folder='templates2', static_folder='static')

app.config["SECRET_KEY"] = b'f\xe9\x04\xc702\xc5\n\x83)\xe6\x1e1\xfe\x879\xc79a\xf6T\xce\x9a\xca'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'get_login'


class Users(UserMixin):
    username = "testusernameguy"
    password = "testpasswdyay"

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
    return Users("a", "b", 1)


@app.route('/posts')
def get_posts(number):
    return None
    
    return


@app.route('/posts/<string:post_id>')
def get_post(post_id):
    title, content, user =  DB_handler.get_post(post_id)
    comments = DB_handler.get_comments(post_id)
    return render_template('post.html', title = title, post_content = content, username = user, 
                           comments = comments, CONTENT = 0, USERNAME = 1)
    post = DB_handler.get_post(post_id)
    comments = DB_handler.get_comments(post_id)




@app.route('/')
@login_required
def get_home():
    return render_template('home.html')


@app.route('/signup')
def get_signup():
    return render_template('signup.html')


@app.route('/pass_reset')
def get_pass_reset():
    return render_template('pass_reset.html')


@app.route('/profile')
def get_profile():
    return render_template('profile.html')


@app.route('/logoff')  # TODO add frontend
def logoff():
    logout_user()
    return "logged off."


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
                "INSERT INTO users(username, password, mail, name, id) VALUES (%s, %s, %s, %s, %s)", (uname, pword, email, name, uuid4()))
            return "you're signed up!."


@app.route('/login')
def get_login():
    return render_template('login.html')


@app.route('/secret')
@login_required
def get_secret():
    post_list = [item for post in DB_handler.get_short_posts(
        1) for item in post]
    return render_template('secret.html', postlist=post_list)


#create_comment('d43fbb15-9877-40c9-99fc-00f8b736a3b2', "stupid question", "commenter", datetime.now())
#create_comment('d43fbb15-9877-40c9-99fc-00f8b736a3b2', "very stupid question", "commenter2", datetime.now())


@app.route('/login', methods=['POST'])
# function for incoming post requests.
def handle_login_post():
    if request.method == 'POST':
        uname = request.form['uname']
        pword = request.form['pass']
        password, id = DB_handler.get_user(uname, pword)

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


@app.route('/')
def handle_get():
    return render_template(...)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
