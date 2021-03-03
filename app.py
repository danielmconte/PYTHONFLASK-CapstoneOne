from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Photo, User
from secrets import API_SECRET_KEY
from forms import AddPhotoForm, UserForm
from sqlalchemy.exc import IntegrityError
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

# db.drop_all()
# db.create_all()


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
        if album == True and "user_id" not in session: 
            flash("Please login first!", "danger")
            return render_template('mars_form.html', form=form, data=data)
        elif album == True:
        # Uses check box to determine album save, but UI could be improved
            new_photo = Photo(rover_name = rover, earth_date=data["photos"][1]["earth_date"], sol =sol, urls=data["photos"][1]["img_src"], user_id=session['user_id'])
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


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form=UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = User.register(username, password)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append("Username taken. Please pick another.")
            return render_template('register.html', form=form)
        session['user_id'] = new_user.id
        flash('Welcome! Account Successfully Created!', 'success')
        return redirect('/mars/images')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form=UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['user_id'] = user.id
            return redirect('/mars/images')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    session.pop('user_id')
    flash("Goodbye!", "info")
    return redirect('/')


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

   






