from app import db
from app.models.base import BaseModel
from app.models.t_simple_net_utils import SimpleNetWeight, SimpleNetWeightGradient, SimpleNetEvidence, SimpleNetEvidenceGradient
from app.tasks.random_generators import float_generator
from app.tasks.sigmoid import sigmoid
from app.models.t_simple_net import TSimpleNet
from app.models.t_example import TExample
from app.models.t_example_utils import ExampleSample, ExampleResult
from app.models.t_deep_net_utils import Activation, ActivationGradient


class TDeepNet(BaseModel):
    """
    Is a set of simple nets and has a size equal to its depth.
    Activation and activation gradient are for final nodes.
    """
    __tablename__ = 't_deep_net'

    t_form_id = db.Column(db.Integer, nullable=False)
    depth = db.Column(db.Integer, nullable=False, server_default='0')


    def setup(self, net_depth, net_profile):
        """
        Sets up a deep net.
        """
        self.depth = net_depth
        self.save_to_db()
        print('Setting up %s simple nets...' % (str(self.depth)))
        for lamda in range(1, net_depth+1):
            # creates one simple for every point of depth.
            simple_net = TSimpleNet(t_deep_net_id=self.id, index=lamda)
            simple_net.setup(net_profile[lamda-1],net_profile[lamda])
            simple_net.save_to_db()
            print('Simple net with id %s created' %(str(simple_net.id)))


    def initialize_weights(self, bias):
        """
        Initializes weights of every created simple net.
        """
        depth = self.depth or 0
        for lamda in range(1, depth+1):
            simple_net = TSimpleNet.query.filter(TSimpleNet.index==lamda).first()
            simple_net.initialize_weights()


    def operation_onto(self, example):
        """
        Runs examples for every simple net given a set of activations.
        """
        lamda = 0
        activation = Activation(t_deep_net_id=self.id, depth=lamda, j_depth=0, value=1.0)
        activation.save_to_db()

        for j_zero in range(1, example.sample_size+1):
            jz_sample = ExampleSample.query.filter(ExampleSample.index==j_zero).first()
            avtivation_value = jz_sample.value
            activation = Activation(t_deep_net_id=self.id, depth=lamda, j_depth=j_zero, value=activation_value)
            activation.save_to_db()

        for lamda in range(1, self.depth+1):
            input_data = []
            output_data = []
            activations = Activation.query.filter(Activation.depth==lamda).all()
            for activation in activations:
                input_data.append(activation.value)
            activations = Activation.query.filter(Activation.depth==lamda-1).all()
            for activation in activations:
                output_data.append(activation.value)
            simple_net = TSimpleNet.query.filter(TSimpleNet.index==lamda).first()
            simple_net.operate_from_to(input_data, output_data)
            simple_net.save_to_db()
        activation = Activation.query.filter(Activation.depth==self.depth).filter(Activation.j_deep==j_deep).first()

        for j_deep in range(1, example.answer_size+1):
            example_result = ExampleResult(t_example_id=example.id, index=j_deep, value=activation.value)
            example_result.save_to_db()


    def apply_to(self, data_set):
        """
        Sets data set of operation.
        """
        for eg in range(1, data_set.work+1):
            dataset_example = TExample.query.filter(TExample.index==eg).first()
            print(dataset_example)
            self.operation_onto(dataset_example)


    def square_error_on(self, data_set):
        """
        Shows square eror on dataset.
        """
        square_error = 0
        for eg in range(1, data_set.work+1):
            dataset_example = TExample.query.filter(TExample.index==eg).first()
            square_error = square_error + dataset_example.square_error()


    def initialize_weight_gradients(self):
        """
        Initializes weight gradients.
        """
        for lamda in range(1, self.depth+1):
            simple_net = TSimpleNet.query.filter(TSimpleNet.index==lamda).first()
            simple_net.initialize_weight_gradients()


    def initialize_activation_gradients(self):
        """
        Initializes activation gradients.
        """
        for j_deep in range(1, self.depth+1):
            activation_gradient = ActivationGradient(t_deep_net_id=self.id, depth=self.depth, j_depth=jdeep)
            activation_gradient.value = 0.0
            activation_gradient.save_to_db()


    def backwards_from(self, example):
        """
        Changes the order of examples.
        """
        example = TExample.query.filter(TExample.index==depth).first()
        for j_deep in range(1, example.sample_size+1):
            activation_gradient = ActivationGradient(t_deep_net_id=self.id, depth=self.depth, j_depth=jdeep)
            example_answer = ExampleAnswer.query.filter(ExampleAnswer.index==j_deep).first()
            example_result = ExampleResult.query.filter(ExampleResult.index==j_deep).first()
            activation_gradient.value = 2 * (example_result.value - example_answer.value)
            activation_gradient.save_to_db()
        self.initialize_activation_gradients()
        for lamda in range(self.depth, 0):
            simple_net = TSimpleNet.query.filter(TSimpleNet.index==lamda).first()
            for j_next in range(1, example.sample_size+1):
                evidence = SimpleNetEvidence.query.filter(SimpleNetEvidence.index==j_next).first()
                activation_gradient = ActivationGradient.query.filter(ActivationGradient.depth==depth).filter(ActivationGradient.j_depth==j_next).first()
                evidence_gradient = SimpleNetEvidenceGradient(t_simple_net_id=simple_net.id, index=j_next)
                evidence_gradient.value = sigmoid_derivative(evidence_value) * activation_gradient.value
                evidence_gradient.save_to_db()
            for j_back in range(1, simple_net.t_input+1):
                for j_next in range(1, simple_net.t_output+1):
                    activation = Activation.query.filter(Activation.depth==lamda-1).filter(Activation.j_depth==j_back).first()
                    weight = SimpleNetWeight.query.filter(SimpleNetWeight.j_next==j_next).filter(SimpleNetWeight.j_prev==j_back).first()
                    evidence_gradient = SimpleNetEvidenceGradient.query.filter(SimpleNetEvidenceGradient.index==j_next).first()
                    activation_gradient = ActivationGradient.query.filter(ActivationGradient.depth==lamda-1).filter(ActivationGradient.j_depth==j_back).first()
                    activation_gradient.value = activation_gradient.value + (weight.value * evidence_gradient.value)
                    activation_gradient.save_to_db()
                    weight_gradient = SimpleNetWeightGradient.query.filter(SimpleNetWeightGradient.j_prev==j_back).filter(SimpleNetWeightGradient.j_next==j_next).first()
                    weight_gradient.value = weight_gradient.value + (activation.value * evidence_gradient.value)
                    weight_gradient.save_to_db()


    def compute_weight_gradients(self, data_set):
        """
        Computes weight gradients of deep net.
        """
        self.initialize_weight_gradients()
        for eg in range(1, data_set.work+1):
            example = TExample.query.filter(TExample.index==eg).first()
            self.operation_onto(example)
            self.backwards_from(example)


    def improve_weights(self, rate):
        """
        Improves weights of deep net.
        """
        for lamda in range(self.depth, 0):
            simple_net = TSimpleNet.query.filter(TSimpleNet.t_deep_net_id==self.id).filter(TSimpleNet.index==eg).first()
            for j_back in range(0, simple_net.t_input+1):
                for j_next in range(0, simple_net.t_output+1):
                    weight = SimpleNetWeight.query.filter(SimpleNetWeight.j_prev==j_back).filter(SimpleNetWeight.j_next==j_next).first()
                    weight_gradient = SimpleNetWeightGradient.query.filter(SimpleNetWeightGradient.j_prev==j_back).filter(SimpleNetWeightGradient.j_next==j_next).first()
                    weight.value = weight.value - (rate * weight_gradient.value)
                    weight.save_to_db()