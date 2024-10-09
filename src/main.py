import tensorflow as tf
import numpy as np
import tensorflow_datasets as tfds
from network import normalize_database,calculate_output_data
from models import initialize_model
from adversary import generate_pertubations


adversary_string = 'test'
model_string = 'resnet'

database, info = tfds.load('imagenet_v2/topimages', split='test', shuffle_files=True, with_info=True)

normalized_database = normalize_database(database,250)

model = initialize_model(model_string)

final_database = generate_pertubations(normalized_database,model,adversary_string)

predictions = calculate_output_data(final_database,model)

print(predictions)