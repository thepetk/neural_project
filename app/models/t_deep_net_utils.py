from app import db
from app.models.base import BaseModel

class Activation(BaseModel):
    __tablename__ = 'dn_activation'

    t_deep_net_id = db.Column(db.Integer, nullable=False)
    depth = db.Column(db.Integer, nullable=False)
    j_depth = db.Column(db.Integer, nullable=False, server_default='0')
    value = db.Column(db.Float, nullable=False, server_default='0')

class ActivationGradient(BaseModel):
    __tablename__ = 'dn_activation_gratient'

    t_deep_net_id = db.Column(db.Integer, nullable=False)
    depth = db.Column(db.Integer, nullable=False)
    j_depth = db.Column(db.Integer, nullable=False, server_default='0')
    value = db.Column(db.Float, nullable=False, server_default='0')
