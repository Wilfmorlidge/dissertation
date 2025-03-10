# test_sample.py

import unittest
from unittest.mock import MagicMock, patch
import numpy as np
import tensorflow as tf
import sys
import numpy.testing as npt
import tensorflow_datasets as tfds

database, info = tfds.load('imagenette/320px-v2', split='validation', shuffle_files=True, with_info=True)

# adding Folder_2 to the system path
sys.path.insert(0, './src')

from adversary import generate_pertubations, AdversarialAttacks, find_logit_derivative_value,find_nearest_class_boundary, calculate_cumulative_pertubation_for_deepfool, calculate_euclidean_term_derivative_for_carlini_wagner_loss_function, calculate_class_term_derivative_for_carlini_wagner_loss_function, optimal_image_calculator, update_loss_function_for_carlini_wagner

class adversary_tests(unittest.TestCase):
    # test that passing a different model name to the function causes the corresponding model to be returned
    def test_generate_pertubations_with_none(self):
        initial_dictionary = {'images': np.ones((10,224,224,3)), 'classifications': np.ones((1,10))}

        test_data = generate_pertubations(initial_dictionary,tf.keras.applications.ResNet50(
        include_top=True,
        weights="imagenet",
        classifier_activation="softmax"
        ),'none',[0,217,482,491,497,566,569,571,574,701])
        npt.assert_array_equal(test_data['unpertubed_images'],np.ones((10,224,224,3)))
        npt.assert_array_equal(test_data['pertubed_images'],np.ones((10,224,224,3)))
        npt.assert_array_equal(test_data['pertubations'],np.zeros((10,224,224,3)))
        npt.assert_array_equal(test_data['classifications'],np.ones((1,10)))

    
    def test_generate_pertubations_with_value(self):
        dictionary = {'images': np.ones((3,224,224,3)), 'classifications': np.zeros((3))}
        AdversarialAttacks.DeepFool_iteration_step = MagicMock(return_value=(1,2))
        generate_pertubations(dictionary,tf.keras.applications.ResNet50(
        include_top=True,
        weights="imagenet",
        classifier_activation="softmax"
        ),'DeepFool',[0,217,482,491,497,566,569,571,574,701])
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

    def test_find_nearest_class_boundary(self):

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

    def test_calculate_cumulative_pertubation_for_deepfool(self):
        np.set_printoptions(precision=20)
        optimizer_values = {'minimum_absolute_boundary_distance': 6.099999999997774e-05,'minimum_euclidean_distance':0.00023850034309222826,'minimum_heuristic':0.25576483123292193,'minimum_logit_derivative':np.array([[-5.41134759e-05,  6.78940123e-05,  1.42538847e-05]]),'nearest_class':1}
        image = np.ones(3)
        cumulative_pertubation = np.zeros((3))
        logit_derivative_for_true_class = np.array([[ 1.577095e-04,  8.044306e-06, -7.756906e-05]])
        overshoot_scalar = 0.02
        test_data = calculate_cumulative_pertubation_for_deepfool(optimizer_values,image,cumulative_pertubation,logit_derivative_for_true_class,overshoot_scalar)
        npt.assert_array_equal(test_data[0],[-0.00454312702278743, 0.001283641761910593, 0.0019693959052649013])
        npt.assert_array_equal(test_data[1],[0.9954568729772125, 1.0012836417619106, 1.001969395905265 ])
    
    def test_deepfool_iteration_step_is_deterministic(self):
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
        test_data = AdversarialAttacks.DeepFool_iteration_step(self,image,classification,model,class_list)
        npt.assert_array_almost_equal(test_data[0], [ 7.760640e-01,  1.063276e+00,  1.097073e+00],decimal=1e-02)
        npt.assert_array_almost_equal(test_data[1],[-2.332242e-21,  6.590697e-22,  1.010983e-21], decimal=1e-26)
    
    def test_deepfool_pertubations_approach_zero_when_class_boundaries_are_not_well_defined(self):
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
        test_data1 = AdversarialAttacks.DeepFool_iteration_step(self,image,classification,model,class_list)
        test_data2 = AdversarialAttacks.DeepFool_iteration_step(self,image,classification,model,class_list,maximal_loop=1000)
        npt.assert_array_almost_equal(test_data1[0], test_data2[0],decimal=1e-02)
        npt.assert_array_almost_equal(test_data2[1], [0,0,0],decimal=1e-50)

    def test_calculate_euclidean_term_derivative_for_carlini_wagner_loss_function(self):
        image = np.ones((5))
        pertubed_image = np.full((5),2)
        npt.assert_array_almost_equal(calculate_euclidean_term_derivative_for_carlini_wagner_loss_function(image,pertubed_image),[-0.447214, -0.447214, -0.447214, -0.447214, -0.447214],decimal=6)
    
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
        npt.assert_array_almost_equal(calculate_class_term_derivative_for_carlini_wagner_loss_function(image,model,learning_rate,target_class,k),[[16.97172 , -4.789984, -7.357985]],decimal=6)

    def test_optimal_image_calculator(self):
        image_1 = (np.full((1,224,224,3), 7),64.3,np.full((1,224,224,3),1))
        image_2 = (np.full((1,224,224,3), 11),114.7,np.full((1,224,224,3),2))
        outputs = [image_1,image_2]
        test_data_1,test_data_2 = optimal_image_calculator(outputs)
        npt.assert_array_equal(test_data_1, np.full((224,224,3),7))
        npt.assert_array_equal(test_data_2, np.full((224,224,3),1))


    @patch('adversary.calculate_euclidean_term_derivative_for_carlini_wagner_loss_function', return_value = np.full((1,3),1.3416))
    @patch('adversary.calculate_class_term_derivative_for_carlini_wagner_loss_function', return_value = np.full((1,3),1.018))
    def test_update_loss_function_for_carlini_wagner(self,mock_calculate_euclidean_term_derivative_for_carlini_wagner_loss_function,mock_calculate_class_term_derivative_for_carlini_wagner_loss_function):
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
        test_data_1,test_data_2,test_data_3,test_data_4, test_data_5 = update_loss_function_for_carlini_wagner(image,pertubed_image,model,learning_rate,target_class,k)
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
        test_data_1,test_data_2 = AdversarialAttacks.Carlini_Wagner_iteration_step(self,image,classification,model,class_list, 50, temperature)
        self.assertEqual(test_data_1.shape, (3,))
        self.assertEqual(test_data_2.shape, (3,))



        


if __name__ == '__main__':
    unittest.main()