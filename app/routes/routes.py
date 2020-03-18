from app.models.t_examples import TExamples
from app.models.t_data_sets import TDataSets

# Constants - Fixed vaules for examples:
ICON_SIDE_SIZE = 8
ICON_MAX_LENGTH = SIDE_SIZE ** 2
NETWORK_MAX_DEPTH = 6

# Network settings
BIAS = -1.8
WEIGHT_LOW = 0.9
WEIGHT_HIGH = 1.8

# Basic settings of learning
ERROR_THRESHOLD = 5.0
INFLATION = 1.25
DEFLATION = 0.8
MIN_DESCENT_RATE = 0.00001
MAX_DESCENT_RATE = 50.0
MAX_ITERATIONS = 5000

# Public Variables
t_values_array = []

