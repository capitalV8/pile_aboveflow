import flask
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import DB_handler


DB_handler.connect()
DB_handler.create_default_table()
app=flask.Flask(__name__,template_folder='templates')

# I need an actual secret key
app.config["SECRET_KEY"] = b'f\xe9\x04\xc702\xc5\n\x83)\xe6\x1e1\xfe\x879\xc79a\xf6T\xce\x9a\xca'

login_manager = LoginManager()
login_manager.init_app(app)

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

        if DB_handler.check_if_exists("users", "username", uname):
            DB_handler.DBinsert(f"users, username, {uname}")        
            DB_handler.DBinsert(f"users, password, {pword}")        
            DB_handler.DBinsert("users, mail, mailthing@gmail.com") 
        else:
            return "failed."
        
        
#        newuser = Users(uname, pword)

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
        pword = flask.request.form['lname']
        password = DB_handler.DBexec(f"""
        SELECT password FROM users WHERE username = {uname} AND password = {pword}
        """)
        
        if password != None:
            login_user(Users(uname, password))
            return(flask.redirect(flask.url_for('secret')))
        else:
            return(flask.redirect(flask.url_for('view_signup')))



            # SELECT password FROM users WHERE username = username
            # AND 
            
            #return redirect(url_for("home"))

#        DB_handler.DBinsert("hello, col, testeroftheages")

        #return whatever is needed in the situation.

@app.route('/')
def handle_get():
    return flask.render_template(...) 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
