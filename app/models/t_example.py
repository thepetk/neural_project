from app import db, app
from app.models.base import BaseModel
from app.models.t_example_utils import ExampleSample, ExampleAnswer, ExampleResult
from app.tasks.random_generators import check_random_int, integer_generator


class TExample(BaseModel):
    """
    size_sample, size_answer = the length of sample and answer of this example.
    sample, answer = The values of sample and the correct answer of this sample. For this project we make samples
    of black white or grey boxes.
    result = After computations if the prediction for sample is equal to answer the result is correct. 
    """

    __tablename__ = 't_example'
    t_data_set_id = db.Column(db.Integer, nullable=False)
    sample_size = db.Column(db.Integer, nullable=False, server_default='0')
    answer_size = db.Column(db.Integer, nullable=False, server_default='0')
    index = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Texample {}>'.format(self.id)

    def setup(self, insize, outsize):
        sample_value = 128/255
        self.sample = insize
        self.answer = outsize
        self.save_to_db()
        r = integer_generator(0,100)
        # takes a random number and according to check random int, sets the value of sample.
        instance = check_random_int(r)
        sample = ExampleSample(t_example_id=self.id, value=1, index=0)
        sample.save_to_db()
        for i in range(1, insize+1):
            # initialize all samples of this example with grey color
            sample = ExampleSample(t_example_id=self.id, value=sample_value, index=i)
            sample.save_to_db()

        ox = integer_generator(0, ((app.config['ICON_SIDE_SIZE']-1)-(app.config['ICON_MAX_LENGTH']-1)))
        oy = integer_generator(0, ((app.config['ICON_SIDE_SIZE']-1)-(app.config['ICON_MAX_LENGTH']-1)))
        # ox, oy are the axis of icon sample. According to them tries to make white and black some samples.
        if instance == 2:
            # instance 2 means draw white color for this index
            for x in range(ox, ox+(app.config['ICON_MAX_LENGTH'])+1):
                for y in range(oy, oy+(app.config['ICON_MAX_LENGTH'])+1):
                    index = 1 + (app.config['ICON_MAX_LENGTH']*x + y)
                    sample = ExampleSample.query.filter(ExampleSample.t_example_id==self.id).filter(ExampleSample.index==index).first()
                    if not(sample):
                        sample = ExampleSample(t_example_id=self.id, index=index)
                    sample.value = 0
                    sample.save_to_db()

        elif instance == 3:
            # instance 3 means draw black color.
            for x in range(ox, ox+(app.config['ICON_MAX_LENGTH'])+1):
                for y in range(oy, oy+(app.config['ICON_MAX_LENGTH'])+1):
                    index = 1 + (app.config['ICON_MAX_LENGTH']*x + y)
                    sample = ExampleSample.query.filter(ExampleSample.t_example_id==self.id).filter(ExampleSample.index==index).first()
                    if not(sample):
                        sample = ExampleSample(t_example_id=self.id, index=index)
                    sample.value = 1
                    sample.save_to_db()

        else:
            pass
        
        for j_deep in range(1,outsize+1):
            answer = ExampleAnswer(t_example_id=self.id, value=1, index=instance)
            answer.save_to_db()
            print('answer saved')

    def square_error(self):
        """
        Returns square error of TExample
        """
        j_deep = 0
        square_error = 0
        for j_deep in range(1, self.answer+1):
            result = ExampleResult.query.filter(ExampleResult.index == j_deep).first()
            answer = ExampleAnswer.query.filter(ExampleAnswer.index == j_deep).first()
            # compares answers with results and returns square error of this example.
            square_error = square_error + ((result.value - answer.value)*(result.value - answer.value))
        
        return square_error
