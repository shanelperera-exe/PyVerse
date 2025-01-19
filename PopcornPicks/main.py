from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
import requests
from dotenv import load_dotenv
from os import environ

load_dotenv()

MOVIE_DB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TV_DB_SEARCH_URL = "https://api.themoviedb.org/3/search/tv"
MOVIE_DB_INFO_URL = "https://api.themoviedb.org/3/movie"
TV_DB_INFO_URL = "https://api.themoviedb.org/3/tv"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"
MOVIE_DB_API_KEY = environ["MOVIE_DB_API_KEY"]

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///TopMovies&TV.db"
db.init_app(app)

class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(400), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    ranking: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(300), nullable=False)

    def __repr__(self):
        return f'<Movie {self.title}>'

class TVShow(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    ranking: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(300), nullable=False)

    def __repr__(self):
        return f'<TVShow {self.title}>'
    
class RateMovieForm(FlaskForm):
    rating = StringField('Your Rating Out of 10')
    review = TextAreaField('Your Review', validators=[Length(max=500)], render_kw={"rows": 4})
    submit = SubmitField('Submit')

class AddMediaForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Add')

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/movies")
def movies():
    movies = db.session.execute(db.select(Movie).order_by(Movie.rating.desc())).scalars().all()
    
    # Update rankings for movies
    for i in range(len(movies)):
        movies[i].ranking = i + 1
    
    db.session.commit()
    
    return render_template("movies.html", movies=movies)

@app.route("/tv")
def tv():
    tv_shows = db.session.execute(db.select(TVShow).order_by(TVShow.rating.desc())).scalars().all()
    
    # Update rankings for TV shows
    for i in range(len(tv_shows)):
        tv_shows[i].ranking = i + 1
    
    db.session.commit()
    
    return render_template("tv.html", shows=tv_shows)

@app.route("/edit", methods=["GET", "POST"])
def rate_media():
    form = RateMovieForm()
    media_type = request.args.get("type")
    media_id = request.args.get("id")
    
    if media_type == "movie":
        media = db.get_or_404(Movie, media_id)
    elif media_type == "tv":
        media = db.get_or_404(TVShow, media_id)
    else:
        return redirect(url_for('home'))
    
    if form.validate_on_submit():
        media.rating = float(form.rating.data)
        media.review = form.review.data
        db.session.commit()
        if media_type == "movie":
            return redirect(url_for('movies'))
        elif media_type == "tv":
            return redirect(url_for('tv'))
    
    return render_template('edit.html', media=media, form=form)

@app.route("/delete")
def delete_media():
    media_type = request.args.get("type")
    media_id = request.args.get("id")
    
    if media_type == "movie":
        media_to_delete = db.get_or_404(Movie, media_id)
    elif media_type == "tv":
        media_to_delete = db.get_or_404(TVShow, media_id)
    else:
        return redirect(url_for('home'))
    
    db.session.delete(media_to_delete)
    db.session.commit()
    
    if media_type == "movie":
        return redirect(url_for('movies'))
    elif media_type == "tv":
        return redirect(url_for('tv'))

@app.route("/add", methods=["GET", "POST"])
def add_media():
    media_type = request.args.get("type")
    form = AddMediaForm()
    
    if form.validate_on_submit():
        media_title = form.title.data
        if media_type == "movie":
            data = search_movie(media_title)
        elif media_type == "tv":
            data = search_tv_show(media_title)
        return render_template("select.html", options=data, media_type=media_type)
    
    return render_template("add.html", form=form, media_type=media_type)

@app.route("/add_selected", methods=["GET"])
def add_selected_media():
    media_type = request.args.get("type")
    media_id = request.args.get("id")
    
    if media_type == "movie":
        # Fetch movie details using the movie ID
        response = requests.get(f"{MOVIE_DB_INFO_URL}/{media_id}", params={"api_key": MOVIE_DB_API_KEY})
        data = response.json()
        new_media = Movie(
            title=data["title"],
            year=data["release_date"].split("-")[0],
            description=data["overview"],
            rating=0,
            ranking=0,
            review="",
            img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}"
        )
    elif media_type == "tv":
        # Fetch TV show details using the TV show ID
        response = requests.get(f"{TV_DB_INFO_URL}/{media_id}", params={"api_key": MOVIE_DB_API_KEY})
        data = response.json()
        new_media = TVShow(
            title=data["name"],
            year=data["first_air_date"].split("-")[0],
            description=data["overview"],
            rating=0,
            ranking=0,
            review="",
            img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}"
        )
    else:
        return redirect(url_for('home'))
    
    db.session.add(new_media)
    db.session.commit()
    
    return redirect(url_for('rate_media', type=media_type, id=new_media.id))

def search_movie(title):
    response = requests.get(MOVIE_DB_SEARCH_URL, params={"api_key": MOVIE_DB_API_KEY, "query": title})
    data = response.json()
    results = []
    for movie in data["results"]:
        results.append({
            "id": movie["id"],
            "title": movie["title"],
            "year": movie["release_date"].split("-")[0],
            "overview": movie["overview"],
            "poster_path": f"{MOVIE_DB_IMAGE_URL}{movie['poster_path']}" if movie["poster_path"] else None
        })
    return results

def search_tv_show(title):
    response = requests.get(TV_DB_SEARCH_URL, params={"api_key": MOVIE_DB_API_KEY, "query": title})
    data = response.json()
    results = []
    for show in data["results"]:
        results.append({
            "id": show["id"],
            "title": show["name"],
            "year": show["first_air_date"].split("-")[0],
            "overview": show["overview"],
            "poster_path": f"{MOVIE_DB_IMAGE_URL}{show['poster_path']}" if show["poster_path"] else None
        })
    return results

if __name__ == '__main__':
    app.run(debug=True)