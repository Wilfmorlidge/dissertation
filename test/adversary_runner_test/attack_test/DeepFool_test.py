import unittest
import numpy as np
import tensorflow as tf
import sys
import numpy.testing as npt

sys.path.insert(0, './src')

from trial_runner.attacks.DeepFool import find_logit_derivative_value,find_nearest_class_boundary, DeepFool_iteration_step, calculate_cumulative_pertubation

class DeepFoolTests(unittest.TestCase):
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

    def test_calculate_cumulative_pertubation(self):
        np.set_printoptions(precision=20)
        optimizer_values = {'minimum_absolute_boundary_distance': 6.099999999997774e-05,'minimum_euclidean_distance':0.00023850034309222826,'minimum_heuristic':0.25576483123292193,'minimum_logit_derivative':np.array([[-5.41134759e-05,  6.78940123e-05,  1.42538847e-05]]),'nearest_class':1}
        image = np.ones(3)
        cumulative_pertubation = np.zeros((3))
        logit_derivative_for_true_class = np.array([[ 1.577095e-04,  8.044306e-06, -7.756906e-05]])
        overshoot_scalar = 0.02
        test_data = calculate_cumulative_pertubation(optimizer_values,image,cumulative_pertubation,logit_derivative_for_true_class,overshoot_scalar)
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
        test_data = DeepFool_iteration_step(image,classification,model,class_list,None,None,None)
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
        test_data1 = DeepFool_iteration_step(image,classification,model,class_list,None,None,None)
        test_data2 = DeepFool_iteration_step(image,classification,model,class_list,None,None,1000)
        npt.assert_array_almost_equal(test_data1[0], test_data2[0],decimal=1e-02)
        npt.assert_array_almost_equal(test_data2[1], [0,0,0],decimal=1e-50)

if __name__ == '__main__':
    unittest.main()