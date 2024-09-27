# test_sample.py

import unittest
import numpy as np
import tensorflow as tf
import sys
import numpy.testing as npt
import tensorflow_datasets as tfds

database, info = tfds.load('cifar10', split='test', with_info=True)

# adding Folder_2 to the system path
sys.path.insert(0, './src')

from network import resize_image

class BasicNetworkTests(unittest.TestCase):
    
    def test_resize_array(self):
        npt.assert_array_equal(resize_image(np.ones((32, 32,3))), tf.image.resize(np.ones((32, 32,3)), (224,224)))

if __name__ == '__main__':
    unittest.main()