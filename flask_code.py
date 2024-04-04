import flask
from forms import RegistrationForm, LoginForm
from pymongo import MongoClient

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = '50bcbc5fcc9e893428823223ed7069cf'

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['Akasa_Air']  # Change 'user_database' to your desired database name
collection = db['users']  # Collection to store user data

@app.route("/")
def home():
    return flask.render_template('home.html', title='Home')

from flask import redirect, url_for

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print("Hello")
        user_data = {
            'username': form.username.data,
            'email': form.email.data,
            'password': form.password.data
        }
        # Insert user data into MongoDB
        result = collection.insert_one(user_data)
        if result.inserted_id:
            print("Data inserted successfully. Inserted ID:", result.inserted_id)
        else:
            print("Failed to insert data into MongoDB.")
        
        flask.flash('Account created successfully!', 'success')

        return redirect(url_for('home'))
    else:
        print("Hello")
        print(form.errors)
    return flask.render_template('register.html', title='Register', form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return flask.render_template('login.html', title='login', form=form)

if __name__ == "__main__":
    app.run(debug=False)
