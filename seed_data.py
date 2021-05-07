from models import User,Product

def fill_user(db):
    data = [
        User(1, 'Divyam'),
        User(2, 'Jennifer'),
        User(3, 'Karen'),
        User(4, 'Marcin'),
        User(5, 'Li')
    ]

    db.session.add_all(data)
    db.session.commit()

def fill_product(db):
    data = [
        Product(11,'Icecream','Cookies n cream flavour'),
        Product(12,'Potato Chips','Barbeque flavour'),
        Product(13,'Bucket','5 gallons'),
        Product(14,'Bottle','32 oz'),
        Product(15,'Laptop','RTX 2070, 32GB RAM'),
        Product(16,'Guitar',''),
        Product(17,'Beer','24 pack'),
        Product(18,'Microwave','1100W'),
        Product(19,'Monitor','240Hz, 24 Inches'),
        Product(20,'Table','')
    ]

    db.session.add_all(data)
    db.session.commit()