import tensorflow as tf
import numpy as np
import tensorflow_datasets as tfds
from network import normalize_database,run_prediction
from adversary import generate_pertubations


adversary = 'none'
model = 'resnet'

database, info = tfds.load('imagenet_v2/topimages', split='test', shuffle_files=True, with_info=True)

normalized_database = normalize_database(database,250)

normalized_database = generate_pertubations(normalized_database,model,adversary)

predictions = run_prediction(normalized_database,model)

print(predictions)