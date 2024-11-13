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

from adversary import generate_pertubations, AdversarialAttacks, find_logit_derivative_value,find_nearest_class_boundary

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
        dictionary = {'images': np.ones((3,224,224,3)), 'classifications': np.zeros((3))}
        AdversarialAttacks.DeepFool_iteration_step = MagicMock(return_value=(1,2))
        generate_pertubations(dictionary,tf.keras.applications.ResNet50(
        include_top=True,
        weights="imagenet",
        classifier_activation="softmax"
        ),'DeepFool')
        self.assertEqual(AdversarialAttacks.DeepFool_iteration_step.call_count,3)
        
    def test_logit_derivative_calculation(self):
        
        initializer = tf.keras.initializers.RandomNormal(
    mean=0.0, stddev=0.05, seed=42
)
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(3, input_shape=(3,), activation='linear', kernel_initializer=initializer),
            tf.keras.layers.Dense(3, activation='linear', kernel_initializer=initializer),
            tf.keras.layers.Dense(3, activation='softmax', kernel_initializer=initializer)
        ])
        npt.assert_array_almost_equal(find_logit_derivative_value(np.ones((3)),1,model),[[ 1.577095e-04,  8.044306e-06, -7.756906e-05]], decimal= 2e-07)

    def test_find_nearest_class_boundary_when_finding_new_minimum(self):

        optimizer_values = {'minimum_absolute_boundary_distance': 1e10,'minimum_euclidean_distance':1e10,'minimum_heuristic':1e10,'minimum_logit_derivative':1e10,'nearest_class':-1}

        entry_class_pair = (1,0)

        image = np.ones(3)

        initializer = tf.keras.initializers.RandomNormal(
        mean=0.0, stddev=0.05, seed=42
        )
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(3, input_shape=(3,), activation='linear', kernel_initializer=initializer),
            tf.keras.layers.Dense(3, activation='linear', kernel_initializer=initializer),
            tf.keras.layers.Dense(3, activation='softmax', kernel_initializer=initializer)
        ])


        scores = [[0.333422, 0.333361, 0.333217]]

        logit_derivative_for_true_class = [[ 1.577095e-04,  8.044306e-06, -7.756906e-05]]

        dictionary = {'minimum_absolute_boundary_distance': 6.099999999997774e-05,'minimum_euclidean_distance':0.00023850034309222826,'minimum_heuristic':0.25576483123292193,'minimum_logit_derivative':[[-5.41134759e-05,  6.78940123e-05,  1.42538847e-05]],'nearest_class':1}

        test_data = find_nearest_class_boundary(optimizer_values,entry_class_pair,image,model,scores,logit_derivative_for_true_class)
        self.assertAlmostEqual(test_data['minimum_absolute_boundary_distance'],dictionary['minimum_absolute_boundary_distance'], places=5)
        self.assertAlmostEqual(test_data['minimum_euclidean_distance'],dictionary['minimum_euclidean_distance'], places=5)
        self.assertAlmostEqual(test_data['minimum_heuristic'],dictionary['minimum_heuristic'],)
        npt.assert_array_almost_equal(test_data['minimum_logit_derivative'],dictionary['minimum_logit_derivative'], decimal = 2e-04)
        self.assertEqual(test_data['nearest_class'],dictionary['nearest_class'])



if __name__ == '__main__':
    unittest.main()