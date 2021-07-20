from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page', text='Welcome to the Squirrel Finder!')

@app.route("/learn")
def learn():
    return render_template('learn.html', subtitle='Learn', text='This is where you can learn about the squirrels around you')

@app.route("/listen")
def learn():
    return render_template('listen.html', subtitle='Listen', text='This is where you can listen to different squirrels')

@app.route("/login/register")
def login():
    return render_template('login-register.html', subtitle='Login/Register')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
