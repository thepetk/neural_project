from app import db, app
from app.models.base import BaseModel
from app.models.t_example_utils import Size, Sample, Answer, Result
from app.tasks.random_generators import check_random_int, integer_generator


class TExample(BaseModel):
    __tablename__ = 't_example'
    t_data_set_id = db.Column(db.Integer, db.ForeignKey('TDataSet.id'))
    size = db.relationship('Size', backref='texamples', lazy='dynamic')
    sample = db.relationship('Sample', backref='texamples', lazy='dynamic')
    answer = db.relationship('Answer', backref='texamples', lazy='dynamic')
    result = db.relationship('Result', backref='texamples', lazy='dynamic')

    def __repr__(self):
        return '<Texample {}>'.format(self.id)

    def setup(self, insize, outsize):
        sample_value = 128/255
        size = Size(t_example_id=self.id, sample=insize, answer=outsize)
        size.save_to_db()
        r = integer_generator(0,100)
        instance = check_random_int(r)
        sample = Sample(t_example_id=self.id, value=1, index=0)
        sample.save_to_db()
        for i in range(insize):
            sample = Sample(t_example_id=self.id, value=sample_value)
            sample.save_to_db()
        
        ox = integer_generator(0, ((app.config['ICON_SIDE_SIZE']-1)-(app.config['ICON_MAX_LENGTH']-1)))
        oy = integer_generator(0, ((app.config['ICON_SIDE_SIZE']-1)-(app.config['ICON_MAX_LENGTH']-1)))

        if instance == 2:
            for x in range(ox, ox+(app.config['ICON_MAX_LENGTH'])):
                for y in range(oy, oy+(app.config['ICON_MAX_LENGTH'])):
                    index = 1 + (app.config['ICON_MAX_LENGTH']*x + y)
                    sample = Sample(t_example_id=self.id, index=index, value=0)
        elif instance == 3:
            for x in range(ox, ox+(app.config['ICON_MAX_LENGTH'])):
                for y in range(oy, oy+(app.config['ICON_MAX_LENGTH'])):
                    index = 1 + (app.config['ICON_MAX_LENGTH']*x + y)
                    sample = Sample(t_example_id=self.id, index=index, value=1)
        else:
            pass
        
        for j_deep in range(1,outsize+1):
            answer = Answer(t_example_id=self.id, value=1, index=instance)

    def square_error(self):
        """
        Returns square error of TExample
        """
        j_deep = 0
        square_error = 0
        # Get the size.Answer of this example.
        size = Size.query.filter(t_example_id=self.id).first()
        if not(size):
            print('You have to set up your TExample first')
            self.setup

        for j_deep in range(1, size.answer):
            result = Result.query.filter(Result.index == j_deep).first()
            answer = Answer.query.filter(Answer.index == j_deep).first()
            square_error = square_error + ((result.value - answer.value)*(result.value - answer.value))
        
        return square_error
