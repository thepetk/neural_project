from app import db
from app.models.base import BaseModel
from app.models.t_simple_net_utils import Size, Weight, WeightGradient, Evidence, EvidenceGradient
from app.tasks.random_generators import float_generator
from app.tasks.sigmoid import sigmoid

class TSimpleNet(BaseModel):
    __tablename__ = 't_simple_nets'
    
    size = db.relationship('Size', backref='tsimplenet', lazy='dynamic')
    weight = db.relationship('Weight', backref='tsimplenet', lazy='dynamic')
    weight_gradient = db.relationship('WeightGradient', backref='tsimplenet', lazy='dynamic')
    evidence = db.relationship('Evidence', backref='tsimplenet', lazy='dynamic')
    evidence_gradient = db.relationship('EvidenceGradient', backref='tsimplenet', lazy='dynamic')

    def setup(self, insize, outsize):
        """
        Sets up t simple net.
        """
        size = Size(t_simple_net_id=self.id, t_input=insize, t_output=outsize)
        size.save_to_db()
    
    def initialize_weights(self, bias):
        """
        Initializes weights.
        """
        j_back=0
        size = Size.query.filter(Size.t_simple_net_id==self.id).first()
        for j_next in range(1, self.size.t_output+1):
            weight = Weight(t_simple_net_id=self.id, t_next=j_next, t_prev=j_back, value=app.config['BIAS'])
        for j_back in range(1, self.size.t_input+1):
            for j_next in range(1, self.size.t_output+1):
                random_real = float_generator(app.config['WEIGHT_LOW']/size.input, app.config['WEIGHT_HIGH']/size.input)
                weight = Weight(t_simple_net_id=self.id, t_prev=j_back, t_next=j_next, value=random_real)


    def initialize_weight_gradients(self):
        """
        Initializes weight gradients.
        """
        size = Size.query.filter(Size.t_simple_net_id==self.id).first()
        for j_back in range(0, size.t_input+1):
            for j_next in range(1, size.t_output+1):
                weight_gradient = WeightGradient(t_simple_net_id=self.id, t_prev=j_back, t_next=j_next, value=0.0)


    def operate_from_to(self, input_data, output_data):
        """
        Sets limits of operation.
        """
        j_next = 0
        output_data[J_next] = 1.0
        size = Size.query.filter(Size.t_simple_net_id==self.id).first()
        for j_next in range(1, size.t_output+1):
            evidence = Evidence(t_simple_net_id=self.id, index=j_next, value=0.0)
            for j_back in range(0, size.t_input+1):
                weight = Weight.query.filter(j_prev==j_back).filter(j_next==j_next).first()
                evidence.value = evidence.value + weight.value + input_data[j_back]
                evidence.save_to_db()
            output_data[j_next] = sigmoid(evidence)
