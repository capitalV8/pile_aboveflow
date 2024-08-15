import flask
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
#import DB_handler
#DB_handler.connect()

app=flask.Flask(__name__,template_folder='templates2',static_folder='static')

# I need an actual secret key
app.config["SECRET_KEY"] = b'f\xe9\x04\xc702\xc5\n\x83)\xe6\x1e1\xfe\x879\xc79a\xf6T\xce\x9a\xca'

login_manager = LoginManager()
login_manager.init_app(app)

info = ["",""] # do i need this?
#defines the users class
class Users(UserMixin):
    id = 100
    username = "testusernameguy"
    password = "testpasswdyay"
    def __init__(self, uname, pword, ID):
        self.username = uname
        self.password = pword
        self.id = ID




# gets users by id, i think? on connection? idk
@login_manager.user_loader
def loader_user(user_id):
#    return testuser
    for user in userlist:
        if user.get_id() == user_id:
            return user
    return "a"



# defines login page i think
login_manager.login_view = 'view_login'





@app.route('/')
def view_form():
    return flask.render_template('test.html')

@app.route("/../static/wolverine_icon.ico") # 2 add get for favicon
def fav():
    return flask.send_from_directory(app.static_folder, 'wolverine_icon.ico') # for sure return the file



@app.route('/signup')
def view_signup():
    return flask.render_template('signup')



userlist = []
userlist.append(Users("a","b", 100))
@app.route('/signup', methods=['POST'])
def handle_thing():
    if flask.request.method == 'POST':
        uname = flask.request.form['uname']
        pword = flask.request.form['pass']
        newuser = Users(uname, pword)
        userlist.append(newuser)

        return "ok"

@app.route('/login')
def view_login():
    return flask.render_template('login')
#DBinsert("hello", "col", "boooo")
#DBconnection.commit()
#DBselect("hello", "col")


@app.route('/update')
def update():
    return "bob"


@app.route('/post')
def get_post():
    return flask.render_template('post 3.html')



@app.route('/post', methods=['POST']) #TODO: connect with html
def post_post():
    is_like = flask.request.form['like']

    print(is_like)
    #isnt_like = flask.request.form['dislike']
    print(is_like)
    #print(isnt_like)
    return is_like


@app.route('/update2')
def update2():
    return "bob2"

@app.route('/secret')
def secret():
    return flask.render_template('secret.html', postlist = [("a", "b"), ("c", "d")])

@app.route('/login', methods=['POST'])
#function for incoming post requests.
def handle_post():
    if flask.request.method == 'POST':
        uname = flask.request.form['fname']
        user = userlist[0]
        if flask.request.form['lname'] == "logout":
            logout_user()
        elif user.password == flask.request.form['lname']:
            login_user(user)
            return("logged in")
            #return redirect(url_for("home"))
        #it prints whatever is written so it works, can connect to DB here for stuff.
#        DB_handler.DBinsert

#        DB_handler.DBinsert("hello, col, testeroftheages")

        #return whatever is needed in the situation.
        return(flask.redirect(flask.url_for('view_signup')))
    else: 
        return flask.render_template(...) 

#@app.route('/')
#def handle_get():
#    return flask.render_template(...) 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
