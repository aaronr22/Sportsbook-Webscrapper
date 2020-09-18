from app import db
from sqlalchemy.dialects.postgresql import JSON

class Result(db.Model):
    __tablename__ = 'results'

    name = db.Column(db.String(), primary_key=True)
    lines = db.Column(db.String())

    def __init__(self, lines):
        self.lines = lines

    def __repr__(self):
        return '<name {}>'.format(self.name)