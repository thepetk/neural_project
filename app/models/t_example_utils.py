from app import db
from app.models.base import BaseModel

class ExampleAnswer(BaseModel):
    __tablename__ = 'te_answer'
    t_example_id = db.Column(db.Integer, nullable=False)
    index = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Integer, nullable=False, server_default='0')

class ExampleSample(BaseModel):
    __tablename__ = 'te_sample'
    t_example_id = db.Column(db.Integer, nullable=False)
    index = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=False, server_default='0')

class ExampleResult(BaseModel):
    __tablename__ = 'te_reuslt'
    t_example_id = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Integer, nullable=False, server_default='0')