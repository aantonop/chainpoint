from datetime import datetime
from chainpoint.run import db
from sqlalchemy import DateTime


class Receipt(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    # header
    chainpoint_version = db.Column(db.Integer, primary_key=True)
    hash_type = db.Column(db.String(35))
    merkle_root = db.Column(db.String(64))
    local_time = db.Column(DateTime, default=datetime.utcnow)

    # target
    target_hash = db.Column(db.String(64))
    target_proof = db.Column(db.LargeBinary)
    uri = db.Column(db.String(2083))  # max length of URL - 2,083 characters

    def __init__(self):
        pass
