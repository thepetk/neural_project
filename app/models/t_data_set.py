from app import db, app
from app.models.base import BaseModel
from app.models.t_example import TExample
from app.tasks.random_generators import check_random_int, integer_generator


class TDataSet(BaseModel):
    __tablename__ = 't_data_set'

    t_form_id = db.Column(db.Integer, nullable=False)
    full = db.Column(db.Integer, nullable=False, server_default='0')
    work = db.Column(db.Integer, nullable=False, server_default='0')

    def setup(self, dataset_size):
        """
        Sets up the data set.
        """
        # Initialize data set full example size and work example size.
        self.work = dataset_size
        self.full = dataset_size
        print('Setting up dataset with size %s. Please wait' % (str(dataset_size)))
        for eg in range(1, self.full+1):
            # For full size setup equal length of examples 
            example = TExample(t_data_set_id=self.id, index=eg)
            example.setup(app.config['ICON_MAX_LENGTH'], 3)
            example.save_to_db()
            print('Example with id %s created' % (str(example.id)))
        self.save_to_db()

    def work_with_subset(self, percent):
        """
        Change your size to work size in order to have less examples.
        """
        # reduce work length of examples according to given percent
        self.work = min(round(self.full * (percent/100)), self.full)

        for index in range(1, self.work+1):
            # randomize the index of every example in order to have random work examples.
            eg = integer_generator(index, self.full)
            some_example = TExample.query.filter(TExample.t_data_set_id==self.id).filter(TExample.index == eg).first()
            index_example = TExample.query.filter(TExample.t_data_set_id==self.id).filter(TExample.index == index).first()
            # Change index with random example.
            temp_index = some_example.index
            some_example.index = index_example.index
            index_example.index = temp_index

            some_example.save_to_db()
            index_example.save_to_db()
        self.save_to_db()