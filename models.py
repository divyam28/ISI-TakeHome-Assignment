from flask_sqlalchemy import SQLAlchemy
import uuid
db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text, nullable = False)
    description = db.Column(db.Text)

    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description
        

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'description' : self.description
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text, nullable = False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
        }

class Reviews(db.Model):
    rev_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id), nullable=False)
    review = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __init__(self,user_id,product_id,review,rating):
        # self.rev_id = rev_id
        self.user_id = user_id
        self.product_id = product_id
        self.review = review
        self.rating = rating

    @property
    def serialize(self):
        return {
            # 'id' : rev_id,
            'user_id' : self.user_id,
            'product_id' : self.product_id,
            'review' : self.review,
            'rating' : self.rating
        }