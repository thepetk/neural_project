from app import db
from app.models.base import BaseModel


class SimpleNetEvidence(BaseModel):
    __tablename__ = 'sn_evidence'

    t_simple_net_id = db.Column(db.Integer, nullable=False)
    index = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Integer, nullable=False, server_default='0')


class SimpleNetEvidenceGradient(BaseModel):
    __tablename__ = 'sn_evidence_gradient'

    t_simple_net_id = db.Column(db.Integer, nullable=False)
    index = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=False, server_default='0')


class SimpleNetWeight(BaseModel):
    __tablename__ = 'sn_weight'

    t_simple_net_id = db.Column(db.Integer, nullable=False)
    j_next = db.Column(db.Integer, nullable=False)
    j_prev = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=False, server_default='0')


class SimpleNetWeightGradient(BaseModel):
    __tablename__ = 'weight_gradient'

    t_simple_net_id = db.Column(db.Integer, nullable=False)
    j_next = db.Column(db.Integer, nullable=False)
    j_prev = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=False, server_default='0')