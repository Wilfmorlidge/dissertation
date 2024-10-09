# test_sample.py

import unittest
import numpy as np
import tensorflow as tf
import sys
import numpy.testing as npt
import tensorflow_datasets as tfds

database, info = tfds.load('imagenet_v2/topimages', split='test', with_info=True)

# adding Folder_2 to the system path
sys.path.insert(0, './src')

from network import resize_image, normalize_database, calculate_output_data

class BasicNetworkTests(unittest.TestCase):
    #test that the resize function performs as expected
    def test_resize_array(self):
        npt.assert_array_equal(resize_image(np.ones((32, 32,3))), tf.image.resize(np.ones((32, 32,3)), (224,224)))

    #test that the image pre-processing function performs as expected
    def test_normalize_database(self):
        results = normalize_database(database,10)
        self.assertIsInstance(results, dict)
        self.assertIn('images',results)
        self.assertEqual(np.array(results['images']).shape, (10, 224, 224, 3))

    #test that the function making predictions and providing output data performs as expected
    def test_run_prediction(self):
        results = calculate_output_data({'images':np.ones((2,224,224,3)), 'classifications':np.ones((2,1))},'resnet')
        self.assertIsInstance(results, dict)
        self.assertIn('confidences',results)
        self.assertIn('classes',results)
        self.assertIn('accuracy',results)


if __name__ == '__main__':
    unittest.main()