from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Photo
from secrets import API_SECRET_KEY
from forms import AddPhotoForm
import requests


app = Flask(__name__)

key = API_SECRET_KEY


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///mars_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)


API_BASE_URL_PHOTO = "https://api.nasa.gov/mars-photos/api/v1/rovers"

API_BASE_URL_WEATHER = "https://api.nasa.gov/insight_weather"

books= []
isbn = ["0030461669", "0810972743", "1250256887"]

def make_books():
    for i in isbn:
        res = requests.get(f'https://openlibrary.org/api/books?bibkeys=ISBN:{i}&jscmd=data&format=json')
        data = res.json()
        books.append(data)
    return books
    
#VIEWS BELOW: 

@app.route('/')
def landing_page():
    return render_template("landing.html")

# Show list (album) of photos
@app.route('/mars/images')
def get_images():
    photos = Photo.query.all()
    return render_template('mars_images.html', photos=photos)

 
@app.route('/mars/images/<int:id>')
def show_image(id):
    photo = Photo.query.get_or_404(id)
    return render_template('mars_image.html', photo=photo) 


@app.route('/mars/images/new', methods = ['GET', 'POST'])
def see_image():
    form = AddPhotoForm()
    if form.validate_on_submit():
        rover = form.rover.data 
        sol = form.sol.data
        res = requests.get(f"{API_BASE_URL_PHOTO}/{rover}/photos?sol={sol}&api_key={key}")
        data = res.json() 
        album = form.album.data
        if album == True:
        # Uses check box to determine album save, but UI could be improved
            new_photo = Photo(rover_name = rover, earth_date=data["photos"][1]["earth_date"], sol =sol, urls=data["photos"][1]["img_src"])
            db.session.add(new_photo)
            db.session.commit()
        return render_template('mars_form.html', form=form, data=data)
    else:
        return render_template('mars_form.html', form=form)

@app.route('/delete/<int:id>', methods = ['GET'])
def delete_image(id):
    # Made this a GET rather than DELETE because DELETE would not work, not great
    photo = Photo.query.get_or_404(id)
    db.session.delete(photo)
    db.session.commit()
    photos = Photo.query.all()
    return render_template('mars_images.html', photos=photos)


@app.route('/mars/forecast')
def get_forecast():
    res = requests.get(f"{API_BASE_URL_WEATHER}/?api_key={key}&feedtype=json&ver=1.0")
    data = res.json()
    return render_template('mars_weather.html', data = data)


@app.route('/mars/books')
def get_books():
    string_isbn = [f"ISBN:{isbn[0]}", f"ISBN:{isbn[1]}", f"ISBN:{isbn[2]}"]
    make_books()
    return render_template('mars_books.html', books=books, string_isbn=string_isbn)

   






