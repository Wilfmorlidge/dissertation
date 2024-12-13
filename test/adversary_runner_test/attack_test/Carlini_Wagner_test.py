import unittest
from unittest.mock import patch
import numpy as np
import tensorflow as tf
import sys
import numpy.testing as npt

sys.path.insert(0, './src')

from trial_runner.attacks.Carlini_Wagner import calculate_euclidean_term_derivative, calculate_class_term_derivative, optimal_image_calculator, update_loss_function, Carlini_Wagner_iteration_step

class CarliniWagnerTests(unittest.TestCase):


    def test_calculate_euclidean_term_derivative_for_carlini_wagner_loss_function(self):
        image = np.ones((5))
        pertubed_image = np.full((5),2)
        npt.assert_array_almost_equal(calculate_euclidean_term_derivative(image,pertubed_image),[-0.447214, -0.447214, -0.447214, -0.447214, -0.447214],decimal=6)
    
    def test_calculate_class_term_derivative_for_carlini_wagner_loss_function(self):
        initializer = tf.keras.initializers.RandomNormal(
        mean=0.0, stddev=0.1, seed=42
        )
        image = np.ones((1,3))
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(3, input_shape=(3,), activation='linear', kernel_initializer=initializer),
            tf.keras.layers.Dense(3, activation='linear', kernel_initializer=initializer),
            tf.keras.layers.Dense(3, activation='softmax', kernel_initializer=initializer)
        ])
        learning_rate = 10000.0
        target_class = 1
        k = -0.5
        npt.assert_array_almost_equal(calculate_class_term_derivative(image,model,learning_rate,target_class,k),[[16.97172 , -4.789984, -7.357985]],decimal=6)

    def test_optimal_image_calculator(self):
        image_1 = (np.full((1,224,224,3), 7),64.3,np.full((1,224,224,3),1))
        image_2 = (np.full((1,224,224,3), 11),114.7,np.full((1,224,224,3),2))
        outputs = [image_1,image_2]
        test_data_1,test_data_2 = optimal_image_calculator(outputs)
        npt.assert_array_equal(test_data_1, np.full((224,224,3),7))
        npt.assert_array_equal(test_data_2, np.full((224,224,3),1))


    @patch('trial_runner.attacks.Carlini_Wagner.calculate_euclidean_term_derivative', return_value = np.full((1,3),1.3416))
    @patch('trial_runner.attacks.Carlini_Wagner.calculate_class_term_derivative', return_value = np.full((1,3),1.018))
    def test_update_loss_function_for_carlini_wagner(self,mock_calculate_euclidean_term_derivative,mock_calculate_class_term_derivative):
        initializer = tf.keras.initializers.RandomNormal(
        mean=0.0, stddev=0.1, seed=42
        )
        image = np.ones((1,3))
        pertubed_image = np.full((1,3), 1.118)
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(3, input_shape=(3,), activation='linear', kernel_initializer=initializer),
            tf.keras.layers.Dense(3, activation='linear', kernel_initializer=initializer),
            tf.keras.layers.Dense(3, activation='softmax', kernel_initializer=initializer)
        ])
        learning_rate = 10000.0
        target_class = 1
        k = -0.5
        test_data_1,test_data_2,test_data_3,test_data_4, test_data_5 = update_loss_function(image,pertubed_image,model,learning_rate,target_class,k)
        npt.assert_array_equal(test_data_1, pertubed_image)
        npt.assert_array_equal(test_data_2, np.full((1,3),-1.2416))
        npt.assert_array_equal(test_data_3, np.full((1,3),2.3596))
        self.assertAlmostEqual(test_data_4.numpy().item(),18.437957763671875, places=7)
        npt.assert_array_almost_equal(test_data_5, [[0.332457, 0.333054, 0.334489]], decimal = 3)


    def test_Carlini_Wagner_iteration_step_is_non_crashing(self):
        np.set_printoptions(precision=20)
        image = np.ones(3)
        classification = 0
        initializer = tf.keras.initializers.RandomNormal(
        mean=0.0, stddev=0.1, seed=42
        )
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(3, input_shape=(3,), activation='linear', kernel_initializer=initializer),
            tf.keras.layers.Dense(3, activation='linear', kernel_initializer=initializer),
            tf.keras.layers.Dense(3, activation='softmax', kernel_initializer=initializer)
        ])

        class_list = [0,1,2]
        temperature = 1
        test_data_1,test_data_2 = Carlini_Wagner_iteration_step(image,classification,model,class_list, 50.0, None,temperature,None,None,None)
        self.assertEqual(test_data_1.shape, (3,))
        self.assertEqual(test_data_2.shape, (3,))

if __name__ == '__main__':
    unittest.main()