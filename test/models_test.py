# test_sample.py

import unittest
import numpy as np
import tensorflow as tf
import sys
import numpy.testing as npt
import tensorflow_datasets as tfds

# adding Folder_2 to the system path
sys.path.insert(0, './src')

from models import initialize_model

class BasicModelSelectionTests(unittest.TestCase):
    
    def test_model_selection(self):
        npt.assert_array_equal(((initialize_model('resnet')).get_weights())[0],((tf.keras.applications.ResNet50(
        include_top=True,
        weights="imagenet",
        classifier_activation="softmax"
        )).get_weights())[0])
        npt.assert_array_equal(((initialize_model('efficientnet')).get_weights())[0],((tf.keras.applications.EfficientNetB0(
            include_top=True,
            weights='imagenet',
            input_tensor=None,
            classifier_activation='softmax',
        )).get_weights())[0])


if __name__ == '__main__':
    unittest.main()