from flask import Flask, render_template, redirect, url_for
from flask import request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import DB_handler


#TODO make ID for table
#TODO put DB_HANDLER.update wherever it is needed.
DB_handler.connect()
#DB_handler.create_default_table()
DB_handler.init_tables()
app=Flask(__name__,template_folder='templates2', static_folder='static')

# I need an actual secret key
app.config["SECRET_KEY"] = b'f\xe9\x04\xc702\xc5\n\x83)\xe6\x1e1\xfe\x879\xc79a\xf6T\xce\x9a\xca'

login_manager = LoginManager()
login_manager.init_app(app)

#defines the users class
class Users(UserMixin):
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
@login_required
def view_form():
    return render_template('home.html')

@app.route('/signup')
def view_signup():
    return render_template('signup.html')

@app.route('/pass_reset')
def view_pass_reset():
    return render_template('pass_reset.html')

@app.route('/profile')
def view_profile():
    return render_template('profile.html')



@app.route('/logoff')
def logoff():
    logout_user()
    return "logged off."


userlist = []
userlist.append(Users("a","b", 100))
@app.route('/signup', methods=['POST'])
def handle_thing():
    
    if request.method == 'POST':
        uname = request.form['uname']
        pword = request.form['pass']

        if DB_handler.check_if_exists("users", "username", uname):
            return "username already taken! please use another username."
        elif len(uname) > 30 or len(pword) > 30:
            return "username or password is too long!"
        else:
            DB_handler.DBexec("INSERT INTO users(username, password, mail, id) VALUES (%s, %s, 'mailthing@gmail.com', '100')", (uname, pword))        
            DB_handler.update()
            return "you're signed up!."
        
#        newuser = Users(uname, pword)
@app.route('/login')
def view_login():
    return render_template('login.html')
#DBinsert("hello", "col", "boooo")
#DBconnection.commit()
#DBselect("hello", "col")


@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html', listthing = ["a", "b", "c", "d", "e", "f"])


@app.route('/login', methods=['POST'])
#function for incoming post requests.
def handle_post():
    if request.method == 'POST':
        uname = request.form['uname']
        pword = request.form['pass']
        password = DB_handler.DBexec(f"""
        SELECT password FROM users WHERE username = %s AND password = %s;
        """, (uname, pword))
        
        if password != None:
            login_user(Users(uname, password, 100))
            return(redirect(url_for('view_form')))
        else:
            return(redirect(url_for('view_signup')))



            # SELECT password FROM users WHERE username = username
            # AND 
            
            #return redirect(url_for("home"))

#        DB_handler.DBinsert("hello, col, testeroftheages")

        #return whatever is needed in the situation.

@app.route('/')
def handle_get():
    return render_template(...) 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
