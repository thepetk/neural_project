from app.models.t_example import TExample
from app.models.t_data_set import TDataSet
from app.models.t_simple_net import TSimpleNet
from app.models.t_deep_net import TDeepNet
from app.models.t_form import TForm
from app.tasks.random_generators import integer_generator, float_generator
from app.tasks.sigmoid import sigmoid, sigmoid_derivative


t_learning_form = TForm()
t_learning_form.save_to_db()

data_set = TDataSet(t_form_id=t_learning_form.id)
data_set.save_to_db()
deep_net = TDeepNet(t_form_id=t_learning_form.id)
deep_net.save_to_db()
incorrect_data = True

while incorrect_data:
    raw_data = input('Options\n\n1.Perform Learning\n\nInput: ')
    if int(raw_data) == 1:
        t_learning_form.perform_learning(data_set, deep_net)
        incorrect_data = False
    else:
        print('Wrong option. Please try again\n')
