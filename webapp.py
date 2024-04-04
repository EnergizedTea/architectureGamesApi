from flask import Flask, render_template
import psycopg2
from app import app

app = Flask(__name__)

@app.route('/')
def index():
    peliculas = app.getGames
    if peliculas:
        return render_template('index.html', peliculas=peliculas)
    else:
        return render_template('index.html', peliculas=None, generos=None)


if __name__  == '__main__':
    app.run(debug=True)