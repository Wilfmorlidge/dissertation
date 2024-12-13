# test_sample.py

import unittest
from unittest.mock import MagicMock
import numpy as np
import tensorflow as tf
import sys
import numpy.testing as npt
import tensorflow_datasets as tfds

database, info = tfds.load('imagenette/320px-v2', split='validation', shuffle_files=True, with_info=True)

# adding Folder_2 to the system path
sys.path.insert(0, './src')

from trial_runner.adversary_handler import generate_pertubations

class adversary_tests(unittest.TestCase):
    # test that passing a different model name to the function causes the corresponding model to be returned 
    def test_generate_pertubations_with_value(self):
        def test_adversary_function():
            return 1

        dictionary = {'images': np.ones((3,224,224,3)), 'classifications': np.zeros((3))}
        test_adversary_function = MagicMock(return_value=(1,2))
        generate_pertubations(dictionary,tf.keras.applications.ResNet50(
        include_top=True,
        weights="imagenet",
        classifier_activation="softmax"
        ),test_adversary_function,[0,217,482,491,497,566,569,571,574,701],[None])
        self.assertEqual(test_adversary_function.call_count,3)





        


if __name__ == '__main__':
    unittest.main()