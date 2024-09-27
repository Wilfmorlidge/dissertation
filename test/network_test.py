# test_sample.py

import unittest
import numpy as np
import tensorflow as tf
import sys
import numpy.testing as npt
import tensorflow_datasets as tfds

database, info = tfds.load('mnist', split='test', with_info=True)

# adding Folder_2 to the system path
sys.path.insert(0, './src')

from network import resize_image, normalize_database, run_prediction

class BasicNetworkTests(unittest.TestCase):
    
    def test_resize_array(self):
        npt.assert_array_equal(resize_image(np.ones((32, 32,3))), tf.image.resize(np.ones((32, 32,3)), (224,224)))

    def test_normalize_database(self):
        self.assertIsInstance(normalize_database(database,10), np.ndarray)
        self.assertEqual(normalize_database(database,10).shape, (10, 224, 224, 1))

    def test_run_prediction(self):
        self.assertIsInstance(run_prediction(np.ones((2,224,224,3)),'resnet'), np.ndarray)
        self.assertEqual((run_prediction(np.ones((2,224,224,3)),'resnet')).shape, (2,1000))


if __name__ == '__main__':
    unittest.main()