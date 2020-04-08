from app import db
from app.models.base import BaseModel

class Size(BaseModel):
    __tablename__ = 'sn_size'

    t_simple_net_id = db.Column(db.Integer, db.ForeignKey('TSimpleNet.id'))
    index = db.Column(db.Integer, nullable=False)
    t_input = db.Column(db.Integer, nullable=False, server_default='0')
    t_output = db.Column(db.Integer, nullable=False, server_default='0')

class Evidence(BaseModel):
    __tablename__ = 'sn_evidence'

    t_simple_net_id = db.Column(db.Integer, db.ForeignKey('TSimpleNet.id'))
    index = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Integer, nullable=False, server_default='0')


class EvidenceGradient(BaseModel):
    __tablename__ = 'sn_evidence_gradient'

    t_simple_net_id = db.Column(db.Integer, db.ForeignKey('TSimpleNet.id'))
    index = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=False, server_default='0')


class Weight(BaseModel):
    __tablename__ = 'sn_weight'

    t_simple_net_id = db.Column(db.Integer, db.ForeignKey('TSimpleNet.id'))
    t_next = db.Column(db.Integer, nullable=False)
    t_prev = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=False, server_default='0')


class WeightGradient(BaseModel):
    __tablename__ = 'weight_gradient'

    t_simple_net_id = db.Column(db.Integer, db.ForeignKey('TSimpleNet.id'))
    t_next = db.Column(db.Integer, nullable=False)
    t_prev = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=False, server_default='0')