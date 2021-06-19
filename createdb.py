from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'b527fd5d5d33ed876ddf9c7572840e49'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dhxlxndsawolpw:375817c990aff1e7e467ec2833ba0fe468f14ed95f3bd2a9fa9042303bc89a6e@ec2-100-25-231-126.compute-1.amazonaws.com:5432/d7r47vqv8ae2h8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)


if __name__ == '__main__':
    db.create_all()
    # db.drop_all()