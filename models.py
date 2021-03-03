from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    db.app = app
    db.init_app(app)


# MODELS BELOW! 

class Photo(db.Model):

    __tablename__= 'photos'

    def __repr__(self):
        p = self
        return f"<Photo id={p.id} rover_name={p.rover_name} earth_date={p.earth_date} sol={p.sol} urls={p.urls} user_id={p.user_id}>"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    rover_name = db.Column(db.String(20),
                    nullable=False)

    earth_date = db.Column(db.String(15),
                        nullable=False)

    sol = db.Column(db.Integer,
                    nullable=False)

    urls = db.Column(db.String(500),
                    nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref="photos")

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, 
                    primary_key=True,
                    autoincrement=True)

    username = db.Column(db.Text,
                    nullable=False,
                    unique=True)

    password = db.Column(db.Text,
                    nullable=False)


    @classmethod
    def register(cls, username, pwd):
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode('utf8')
        return cls(username=username, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, pwd):
        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False