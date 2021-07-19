from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page', text='Welcome to the Squirrel Finder!')

@app.route("/about")
def second_page():
    return render_template('about-page.html', subtitle='About', text='This is the about page')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")