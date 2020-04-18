from app import db
from app.models.base import BaseModel
from app.models.t_simple_net_utils import SimpleNetWeight, SimpleNetWeightGradient, SimpleNetEvidence, SimpleNetEvidenceGradient
from app.tasks.random_generators import float_generator
from app.tasks.sigmoid import sigmoid

class TSimpleNet(BaseModel):
    """
    Simple net is a subnet of a deepnet(So, it has an index and is related to TDeepNet)
    Inputs, Outputs of net are matched with t_input and t_output
    For every line connecting two nodes there is weight and a weight gradient.
    There is also an evidence and an evidence gradient.
    """

    __tablename__ = 't_simple_net'
    
    t_deep_net_id = db.Column(db.Integer, nullable=False)
    index = db.Column(db.Integer, nullable=False, server_default='0')
    t_input = db.Column(db.Integer, nullable=False, server_default='0')
    t_output = db.Column(db.Integer, nullable=False, server_default='0')

    def setup(self, insize, outsize):
        """
        Sets up a t simple net with specific inputs and outputs.
        """
        self.t_input = insize
        self.t_output = outsize
        self.save_to_db()
    
    def initialize_weights(self, bias):
        """
        Initializes weights.
        """
        j_back=0
        for j_next in range(1, self.t_output+1):
            # initializes the first weights
            weight = SimpleNetWeight(t_simple_net_id=self.id, t_next=j_next, t_prev=j_back, value=bias)
            weight.save_to_db()
        for j_back in range(1, self.t_input+1):
            for j_next in range(1, self.size.t_output+1):
                random_real = float_generator(app.config['WEIGHT_LOW']/size.input, app.config['WEIGHT_HIGH']/size.input)
                weight = SimpleNetWeight(t_simple_net_id=self.id, t_prev=j_back, t_next=j_next, value=random_real)
                weight.save_to_db()


    def initialize_weight_gradients(self):
        """
        Initializes weight gradients.
        """
        for j_back in range(0, self.t_input+1):
            for j_next in range(1, self.t_output+1):
                weight_gradient = SimpleNetWeightGradient(t_simple_net_id=self.id, t_prev=j_back, t_next=j_next, value=0.0)
                weight_gradient.save_to_db()


    def operate_from_to(self, input_data, output_data):
        """
        Gets an input checks evidences, weights and returns output data.
        """
        j_next = 0
        output_data[j_next] = 1.0
        for j_next in range(1, self.t_output+1):
            evidence = SimpleNetEvidence(t_simple_net_id=self.id, index=j_next, value=0.0)
            for j_back in range(0, self.t_input+1):
                weight = SimpleNetWeight.query.filter(SimpleNetWeight.j_prev==j_back).filter(SimpleNetWeight.j_next==j_next).first()
                if weight:
                    weight_value = weight.value
                else:
                    weight_value = 0.0
                evidence.value = evidence.value + weight_value + input_data[j_back]
                evidence.save_to_db()
            output_data[j_next] = sigmoid(evidence)
        return output_data
