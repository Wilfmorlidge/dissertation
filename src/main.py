import tensorflow as tf
import numpy as np
import tensorflow_datasets as tfds
from network import normalize_database,calculate_output_data
from definitions import initialize_model, load_dataset
from adversary import generate_pertubations


print('is this instance running with cuda' + str(tf.test.is_built_with_cuda()))
print('available GPUs: ' + str(tf.config.list_physical_devices('GPU')))

#this indicates which attack is being used
adversary_string = 'Carlini_Wagner'
#this indicates which model is being used
model_string = 'resnet'
#this indicates which dataset is being used
dataset_string = 'imagenette'
#this indicates how many images are used in a trial
trial_length = 25

#this loads the database
database, info, class_list = load_dataset(dataset_string)

# this resizes and pre-processes the database images for use by the appropriate model
normalized_database = normalize_database(database,trial_length,model_string, class_list)

# this acquires the model
model = initialize_model(model_string)

# this applies adversarial pertubation
final_database = generate_pertubations(normalized_database,model,adversary_string,class_list)

# this tests the pertubed data against the network
predictions = calculate_output_data(final_database,model)

print(predictions)