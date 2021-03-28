from flask import Flask, render_template, url_for, request, redirect, flash
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.secret_key = 'fady'
app.sqlalchemy_database_uri = 'sqlite:///data.db'
db = SQLAlchemy(app)

api = Api(app)
jwt = JWT(app, authenticate, identity) #create /auth endpoint


posts = [
    {
        
    },
    {
        
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm ()
    if form.validate_on_submit(): #no syntax errors
        flash(f'Account created for {form.username.data}!', 'success') #success is a bootstrap class to show success of creating a user
        return redirect(url_for('home'))    
    return render_template('register.html', form=form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): #no syntax errors
        if form.email.data == "admin@fadytawfeek.com" and form.password.data == "asdfasdf":
            flash('You are logged in now', 'success') #success is a bootstrap class to show success of creating a user
            return redirect(url_for('home'))
        else:
            flash('Wrong credentials, please try again', 'danger')
        
    return render_template('login.html', form=form)
    

#api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port = 5000, debug=True)