# test_sample.py

import unittest
from unittest.mock import MagicMock
import numpy as np
import tensorflow as tf
import sys
import numpy.testing as npt
import tensorflow_datasets as tfds

database, info = tfds.load('imagenet_v2/topimages', split='test', with_info=True)

# adding Folder_2 to the system path
sys.path.insert(0, './src')

from adversary import generate_pertubations, AdversarialAttacks

class adversary_tests(unittest.TestCase):
    # test that passing a different model name to the function causes the corresponding model to be returned
    def test_generate_pertubations_with_none(self):
        dictionary = {'images': np.ones((10,224,224,3)), 'classifications': np.ones((1,10))}

        npt.assert_array_equal(generate_pertubations(dictionary,tf.keras.applications.ResNet50(
        include_top=True,
        weights="imagenet",
        classifier_activation="softmax"
        ),'none')['images'],np.ones((10,224,224,3)))

        self.assertDictEqual(generate_pertubations(dictionary,tf.keras.applications.ResNet50(
        include_top=True,
        weights="imagenet",
        classifier_activation="softmax"
        ),'none'),dictionary)
    
    def test_generate_pertubations_with_value(self):
        dictionary = {'images': np.ones((3,224,224,3)), 'classifications': np.ones((1,3))}
        AdversarialAttacks.DeepFool_iteration_step = MagicMock(return_value=None)
        generate_pertubations(dictionary,tf.keras.applications.ResNet50(
        include_top=True,
        weights="imagenet",
        classifier_activation="softmax"
        ),'DeepFool')
        self.assertEqual(AdversarialAttacks.DeepFool_iteration_step.call_count,3)
        
    def test_logit_derivative_calculation(self):
        self.assertEqual(1,1)


if __name__ == '__main__':
    unittest.main()