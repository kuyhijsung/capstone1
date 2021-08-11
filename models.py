from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Cocktail(db.Model):
    __tablename__ = "cocktails"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.Text, nullable=False)

    image_url = db.Column(db.Text, nullable=False)

    recipe = db.Column(db.JSON, nullable=False)

    instructions = db.Column(db.Text, nullable=False)

    glass = db.Column(db.Text, nullable=False)
