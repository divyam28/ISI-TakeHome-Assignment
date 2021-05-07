from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from models import db, Product, User, Reviews
from seed_data import fill_product,fill_user
from config import *


def create_app():
    #Initialize App 
    app = Flask(__name__)

    #Database Connection
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False
    db.init_app(app)

    with app.app_context():
        db.drop_all()
        db.create_all()
        fill_product(db)
        fill_user(db)


    @app.route('/user/<id>', methods = ['GET'])
    def get_user(id):
        result = User.query.get(id)
        if not result:
            return make_response(jsonify({'Error': 'There is no User with id={}'.format(id)}), 404)
        return make_response(jsonify(result.serialize),200)


    @app.route('/product/<product_id>', methods = ['GET'])
    def get_product(product_id):
        result = Product.query.get(product_id)
        if not result:
            return make_response(jsonify({'Error': 'There is no Product with id={}'.format(product_id)}), 404)
        return make_response(jsonify(result.serialize),200)


    @app.route('/review/<pid>', methods = ['GET','POST','PUT','DELETE'])
    def review(pid):
        #If product does not exist, throw Not found error with status code 404
        check_product = Product.query.get(pid)
        if not check_product:
            return make_response(jsonify({'Error': 'There is no Product with id={}'.format(pid)}), 404)


        if request.method == 'GET':
            results = Reviews.query.filter_by(product_id = pid).all()
            if not results:
                return make_response(jsonify({'Error': 'There are no reviews for the product with product_id = {}'.format(pid)}), 404)
            else:
                final = {}
                for i,result in enumerate(results):
                    final[i] = result.serialize
                    final[i]['rev_id'] = result.rev_id
                return make_response(jsonify(final),200)

        if request.method == 'POST':
            userid = request.form['userid']
            review = request.form['review']
            rating = request.form['rating']

            check_reviews = Reviews.query.filter_by(product_id = pid, user_id = userid).all()

            if not check_reviews:
                newReview = Reviews(user_id = userid, product_id = pid, review = review, rating = rating)
                db.session.add(newReview)
                db.session.commit()
                return make_response(jsonify({
                    'Status' :'Success',
                    'Message':'Review Successfully Posted'
                }),201)

            else:
                users = [review.user_id for review in check_reviews]
                if int(userid) in users:
                    return make_response(jsonify({
                        'Status': 'Failed',
                        'Message' : 'You can only put one review for this product!'
                    }),409)


        if request.method == 'PUT':
            uid = request.form['userid']
            exisReview = Reviews.query.filter_by(product_id = pid, user_id=uid).first()

            if not exisReview:
                return make_response(jsonify({
                    'Status': 'Failed',
                    'Message': 'This review does not exist!'
                }), 404)

            else:
                exisReview.user_id = int(uid)
                exisReview.review = str(request.form['review'])
                exisReview.rating = float(request.form['rating'])
                db.session.commit()

                return make_response(jsonify({
                    'Status': 'Success',
                    'Message': 'Review successfully updated.'
                }),201)
        
        if request.method == 'DELETE':
            uid = request.form['userid']
            delReview = Reviews.query.filter_by(product_id=pid,user_id=uid).first()

            if not delReview:
                return make_response(jsonify({
                    'Status': 'Failed',
                    'Message': 'This review does not exist!'
                }), 404)
            else:
                db.session.delete(delReview)
                db.session.commit()

                return make_response(jsonify({
                    'Status': 'Success',
                    'Message': 'Review successfully deleted.'
                }),410)

    return app
