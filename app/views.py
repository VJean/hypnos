from app import app
from flask import render_template
from fetch_posts import get_random_redditnugget


@app.route('/')
def homepage():
    n = get_random_redditnugget()
    return render_template('index.html', nugget=n)
