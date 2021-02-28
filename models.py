from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


# MODELS BELOW! 

class Photo(db.Model):

    __tablename__= 'photos'

    def __repr__(self):
        p = self
        return f"<Photo id={p.id} rover_name={p.rover_name} earth_date={p.earth_date} sol={p.sol} urls={p.urls}>"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    rover_name = db.Column(db.String(20),
                    nullable=False,
                    unique=True)

    earth_date = db.Column(db.String(15),
                        nullable=False)

    sol = db.Column(db.Integer,
                    nullable=False)

    urls = db.Column(db.String(500),
                    nullable=False)

