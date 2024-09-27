import tensorflow as tf
import numpy as np
import tensorflow_datasets as tfds
from network import normalize_database,initialize_model

database, info = tfds.load('imagenet_v2', split='test', with_info=True)

normalized_database = normalize_database(database,250)

predictions = initialize_model(normalized_database,'resnet')

