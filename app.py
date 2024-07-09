import flask
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
#import DB_handler
#DB_handler.connect()

app=flask.Flask(__name__,template_folder='templates')

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

@app.route('/signup')
def view_signup():
    return flask.render_template('signup.html')



userlist = []
userlist.append(Users("a","b", 100))
@app.route('/signup', methods=['POST'])
def handle_thing():
    if flask.request.method == 'POST':
        uname = flask.request.form['fname']
        pword = flask.request.form['lname']
        print(uname, pword)
        newuser = Users(uname, pword)
        userlist.append(newuser)
        
        return "ok"

@app.route('/login')
def view_login():
    return flask.render_template('login.html')
#DBinsert("hello", "col", "boooo")
#DBconnection.commit()
#DBselect("hello", "col")


@app.route('/secret')
@login_required
def secret():
    return flask.render_template('secret.html')

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

@app.route('/')
def handle_get():
    return flask.render_template(...) 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
