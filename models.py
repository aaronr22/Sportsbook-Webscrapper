from app import db
from sqlalchemy.dialects.postgresql import JSON
import datetime
from sqlalchemy import DateTime, ForeignKey

class Result(db.Model):
    __tablename__ = 'results'

    name = db.Column(db.String(), primary_key=True)
    lines = db.Column(db.String())

    def __init__(self, name, lines):
        self.name = name
        self.lines = lines

    def __repr__(self):
        return '<name {}>'.format(self.name)

class Lines(db.Model):
    __tablename__ = 'lines'

    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.String, ForeignKey('batch.batch_id'))
    website = db.Column(db.String())
    sport = db.Column(db.String())
    lines = db.Column(db.String())

    def __init__(self, batch, website, sport, lines):
        self.batch_id = batch
        self.website = website
        self.sport = sport
        self.lines = lines

    def __repr__(self):
        return '<website {}>'.format(self.sport)

class Batch(db.Model):
    __tablename__ = 'batch'

    created_time = db.Column(DateTime, default=datetime.datetime.utcnow)
    batch_id = db.Column(db.String(), primary_key=True)
    sport = db.Column(db.String())

    def __init__(self, batch, sport):
        self.batch_id = batch
        self.sport = sport

    def __repr__(self):
        return 'batch_id {}'.format(self.batch_id)

class Aggregated(db.Model):
    __tablename__ = 'aggregated_lines'

    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.String, ForeignKey('batch.batch_id'))
    # batch = relationship("Batch", backref=backref("batch", uselist=False))
    lines = db.Column(db.String())

    def __init__(self, batch, lines):
        self.batch_id = batch
        self.lines = lines

    def __repr__(self):
        return 'batch {}'.format(self.batch_id)

class BookRecords(db.Model):
    __tablename__ = 'book_records'

    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(DateTime, default=datetime.datetime.utcnow)
    book = db.Column(db.String())
    lines = db.Column(db.String())

    def __init__(self, book, lines):
        self.book = book
        self.lines = lines

    def __repr__(self):
        return 'book {}'.format(book)