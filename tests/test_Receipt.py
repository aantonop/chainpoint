import unittest
from chainpoint.run import db
from chainpoint.Receipt import Receipt


class ReceiptTest(unittest.TestCase):

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_new_receipt(self):
        raw_rec = """"""
        rec = Receipt()
