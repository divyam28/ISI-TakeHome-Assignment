import unittest
from flask import Flask
from models import db, Product, User, Reviews
from seed_data import fill_product,fill_user

from app import create_app

class TestSuit(unittest.TestCase):

    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client
        #Drop all tables, create them and fill user and products every test run.
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            fill_product(db)
            fill_user(db)


    #Test status code of data of User Get 
    def test_1_UserGet(self):
        print("Testing User GET")
        #Check Success - User 1 - Divyam
        result1 = self.client().get('/user/1')
        self.assertEqual(result1.status_code, 200)
        self.assertIn('Divyam', str(result1.data))

        #Check Error - User 6 - Does not exist
        result2 = self.client().get('/user/6')
        self.assertEqual(result2.status_code, 404)


    #Test status code of data of Product Get
    def test_2_ProductGet(self):
        print("Testing Product GET")

        #Check Success - Product 11 - Icecream
        result = self.client().get('/product/11')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Icecream', str(result.data))

        #Check Error - Product 2 - Does not exist
        result2 = self.client().get('/product/2')
        self.assertEqual(result2.status_code, 404)


    #Test status code of data of Review Get
    def test_3_ReviewGet(self):
        print("Testing Review GET")
        #Input random data, check success - review 13
        inp = {
            'userid': 4,
            'review': 'This is a good product.',
            'rating': 4.0
        }
        result = self.client().post('/review/13', data = inp)
        self.assertEqual(result.status_code, 201)
        result = self.client().get('/review/13')
        self.assertEqual(result.status_code, 200)
        self.assertIn('good', str(result.data))

        #Check error - Review for product 14 - no reviews
        result2 = self.client().get('/review/14')
        self.assertEqual(result2.status_code, 404)


    #Test status code of data of Review Post 
    def test_4_ReviewPost(self):
        print("Testing Review POST")
        #Check Success for Review 13
        inp = {
            'userid': 4,
            'review': 'This is a good product.',
            'rating': 4.0
        }
        result = self.client().post('/review/13', data = inp)
        self.assertEqual(result.status_code, 201)
        self.assertIn('Success', str(result.data))

        #Check to ensure one review per user per product
        extra_inp = {
            'userid': 4,
            'review': 'This is a good product again.',
            'rating': 4.5
        }
        result2 = self.client().post('/review/13', data = extra_inp)
        self.assertEqual(result2.status_code, 409)


    #Test status code of data of Review Put
    def test_5_ReviewPut(self):
        print("Testing Review PUT")
        #Input random data, check for success updating review for 13
        inp = {
            'userid': 4,
            'review': 'This is a good product.',
            'rating': 4.0
        }
        update = {
            'userid': 4,
            'review': 'This is a great product.',
            'rating': 5.0
        }

        result = self.client().post('/review/13', data = inp)
        self.assertEqual(result.status_code, 201)
        result = self.client().put('/review/13', data = update)
        self.assertEqual(result.status_code, 201)
        self.assertIn('Success', str(result.data))

        #check for review does not exist
        check = {
            'userid': 3,
            'review': 'This is an imaginary review',
            'rating': 2.0
        }
        result2 = self.client().put('/review/13', data = check)
        self.assertEqual(result2.status_code, 404)


    #Test status code of data of Review Delete
    def test_6_ReviewDelete(self):
        print("Testing Review DELETE")
        #Input random data
        inp = {
            'userid': 4,
            'review': 'This is a good product.',
            'rating': 4.0
        }

        delete = {
            'userid': 4
        }
        result = self.client().post('/review/13', data = inp)
        self.assertEqual(result.status_code, 201)
        result = self.client().delete('/review/13', data = delete)
        self.assertEqual(result.status_code, 410)
        self.assertIn('Success', str(result.data))

        #Check for review that does not exist
        check = {
            'userid': 5,
        }
        result2 = self.client().put('/review/13', data = check)
        self.assertEqual(result2.status_code, 404)


    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            # db.drop_all()


# Make the tests executable
if __name__ == "__main__":
    unittest.main()

