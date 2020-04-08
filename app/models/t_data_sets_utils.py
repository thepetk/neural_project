from app import db
from app.models.base import BaseModel

class Size(BaseModel):
    __tablename__ = 'td_size'
    
    t_data_set_id = db.Column(db.Integer, db.ForeignKey('TDataSet.id'))
    index = db.Column(db.Integer, nullable=False)
    full = db.Column(db.Integer, nullable=False, server_default='0')
    work = db.Column(db.Integer, nullable=False, server_default='0')