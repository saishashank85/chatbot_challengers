import logging, pprint
from rasa_nlu import config
from rasa_nlu.training_data import load_data
from rasa_nlu.model import Interpreter, Trainer
from rasa_nlu.test import run_evaluation

logfile = "rasa_trippy.log"

# set logging level
logging.basicConfig(filename=logfile, level=logging.DEBUG)

# load the training data
train_data = load_data("./data/nlu.md")

# create Trainer object using the config file to define the pipeline
trainer = Trainer(config.load("config.yml"))

# train the model
trainer.train(train_data)

# persist the model to store it for future use
model_directory = trainer.persist("./models/nlu", fixed_model_name="current")

# load the model from the file
interpreter = Interpreter.load("./models/nlu/default/current")

# perform few tests
pprint.pprint(interpreter.parse("hey there"))
pprint.pprint(interpreter.parse("find trains from bangalore to mumbai"))
# perform a complete evaluation
run_evaluation("./data/nlu.md", model_directory)
