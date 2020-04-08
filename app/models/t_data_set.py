from app import db, app
from app.models.base import BaseModel
from app.models.t_data_sets_utils import Size


class TDataSet(BaseModel):
    __tablename__ = 't_data_set'

    size = db.relationship('Size', backref='texamples', lazy='dynamic')
    examples = db.relationship('TExample', backref='tdatasets', lazy='dynamic')

    def setup(self, dataset_size):
        """
        Sets up the data set.
        """

        size = Size(t_data_set_id=self.id, work=dataset_size, full=dataset_size)
        size.save_to_db()

        for eg in range(1, size.full):
            example = TExample(t_data_set_id=self.id)
            example.setup(app.config['ICON_MAX_LENGTH'], 3)

    def work_with_subset(self, percent):
        size = Size.query.filter(Size.t_data_set_id==self.id).first()
        size.work = min(round(size.full * (percent/100)), size.full)
        size.save_to_db()

        for index in range(1, size.work):
            eg = integer_generator(index, size.full)
            some_example = TExample.query.filter(TExample.t_data_set_id==self.id).filter(TExample.index == eg).first()
            index_example = TExample.query.filter(TExample.t_data_set_id==self.id).filter(TExample.index == index).first()
            # Change index with random example.
            temp_index = some_example.index
            some_example.index = index_example.index
            index_example.index = temp_index

            some_example.save_to_db()
            index_example.save_to_db()
        