# test_sample.py

import unittest
import numpy as np
import tensorflow as tf
import sys
import numpy.testing as npt
import tensorflow_datasets as tfds
from unittest.mock import MagicMock, patch

database, info = tfds.load('imagenette/320px-v2', split='validation', shuffle_files=True, with_info=True)

# adding Folder_2 to the system path
sys.path.insert(0, './src')

from network import resize_image, normalize_database, calculate_output_data
from window import denormalize_and_save_image

class BasicNetworkTests(unittest.TestCase):
    #test that the resize function performs as expected
    def test_resize_array(self):
        npt.assert_array_equal(resize_image(np.ones((32, 32,3))), tf.image.resize(np.ones((32, 32,3)), (224,224)))

    #test that the image pre-processing function performs as expected
    def test_normalize_database(self):
        results = normalize_database(database,10,'resnet')
        self.assertIsInstance(results, dict)
        self.assertIn('images',results)
        self.assertEqual(np.array(results['images']).shape, (10, 224, 224, 3))

    #test that the function making predictions and providing output data performs as expected
    @patch('network.denormalize_and_save_image')
    def test_calculate_output_data(self,mock_denormalize_and_save_image):
        results = calculate_output_data({'unpertubed_images': np.ones((2,224,224,3)), 'pertubations': np.zeros((2,224,224,3)), 'pertubed_images':np.ones((2,224,224,3)), 'classifications':np.ones((2,1))},tf.keras.applications.ResNet50(
        include_top=True,
        weights="imagenet",
        classifier_activation="softmax"
        ))
        self.assertIsInstance(results, dict)
        self.assertEqual(mock_denormalize_and_save_image.call_count,6)
        self.assertIn('confidences',results)
        self.assertIn('classes',results)
        self.assertIn('accuracy',results)


if __name__ == '__main__':
    unittest.main()