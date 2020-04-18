from app import db, app
from app.models.base import BaseModel

class TForm(BaseModel):
    __tablename__ = 't_form'

    learning_steps = db.Column(db.Integer, nullable=False, server_default='0')
    error = db.Column(db.Float, nullable=False, server_default='0')
    success = db.Column(db.SmallInteger, nullable=False, server_default='0')

    def initialize(self, data_set, deep_net):
        """
        Initializes a dataset and a deep net for this form
        """
        data_set.setup(1)
        print('DataSet Complete')
        data_set.work_with_subset(100)
        data_set.save_to_db()

        net_profile = [int(app.config['ICON_MAX_LENGTH']), 24, 12, 3]
        net_depth = 3
        deep_net.setup(net_depth, net_profile)
        deep_net.save_to_db()

        return data_set, deep_net


    def apply_and_calculate_error(self, data_set, deep_net):
        """
        Applies dataset to deep_net and calculates error. Returns error_percent.
        """
        print('calculates error')
        deep_net.apply_to(data_set)
        deeper_simple_net = TSimpleNet.query.filter(TSimpleNet.t_deep_net_id==deep_net.id).filter(TSimpleNet.index==deep_net.depth).first()
        answers = deep_net.work * deeper_simple_net.t_out_put
        error_percent = 100 * (deep_net.square_erron_on(data_set)/answers)
        
        return error_percent
    
    def check_rate_of_descend(self, descend_rate, new_error, old_error, deep_net):
        """
        Checks descend rate
        """
        if (new_error < old_error):
            descend_rate = min(app.config['INFLATION']*descend_rate, app.config['MAX_DESCENT_RATE'])
        else:
            deep_net.improve_weights((-1)*descend_rate)
            new_error = old_error
            descend_rate = app.config['DEFLATION']*descend_rate
        return new_error, descend_rate

    def perform_learning(self, data_set, deep_net):
        """
        Performs a learning cycle for this form.
        """
        print('Learning cycle started..')
        self.initialize(data_set, deep_net)
        print('DataSet and DeepNet initialized')
        new_error = self.apply_and_calculate_error(data_set, deep_net)
        descend_rate = 1.0
        learning_steps = 0
        while result or (descend_rate > app.config['MIN_DESCENT_RATE']) or (learning_steps <= app.config['MAX_ITERATIONS']):
            learning_steps += 1
            print(learning_steps)
            old_error = new_error
            deep_net.compute_weight_gradients(data_set)
            deep_net.improve_weights(descend_rate)
            new_error = self.apply_and_calculate_error(data_set, deep_net)
            result = (new_error <= app.config['ERROR_THRESHOLD'])
            new_error, descend_rate = self.check_rate_of_descend(descend_rate, new_error, old_error, deep_net)
            if result or (learning_steps % 10 == 0):
                print('Learning Steps: %s\nError: %s (Goal %s)' %(str(learning_steps, str(new_error), str(app.config['ERROR_THRESHOLD']))))
        self.learning_steps = learning_steps
        self.new_error = new_error
        self.result = result
        self.save_to_db()
        print('Learning cycle complete')