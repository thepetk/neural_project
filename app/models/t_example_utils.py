from app import db
from app.models.base import BaseModel

class Answer(BaseModel):
    __tablename__ = 'te_answer'
    t_example_id = db.Column(db.Integer, db.ForeignKey('TExample.id'))
    index = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Integer, nullable=False, server_default='0')

class Sample(BaseModel):
    __tablename__ = 'te_sample'
    t_example_id = db.Column(db.Integer, db.ForeignKey('TExample.id'))
    index = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=False, server_default='0')

class Size(BaseModel):
    __tablename__ = 'te_size'
    t_example_id = db.Column(db.Integer, db.ForeignKey('TExample.id'))
    sample = db.Column(db.Integer, nullable=False, server_default='0')
    answer = db.Column(db.Integer, nullable=False, server_default='0')

class Result(BaseModel):
    __tablename__ = 'te_reuslt'
    t_example_id = db.Column(db.Integer, db.ForeignKey('TExample.id'))
    value = db.Column(db.Integer, nullable=False, server_default='0')