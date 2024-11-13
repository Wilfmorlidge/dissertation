
import os
import unittest
import numpy as np
import sys


# adding Folder_2 to the system path
sys.path.insert(0, './src')

from window import denormalize_and_save_image

class window_tests(unittest.TestCase):
    def test_saving_of_normalized_image(self):
        test_image = np.random.uniform(-50,50,(224,224,3))
        denormalize_and_save_image(test_image,'test_image_please_ignore','pertubed')
        self.assertTrue(os.path.isfile('./images/pertubed/image_test_image_please_ignore.png'))
        os.remove('./images/pertubed/image_test_image_please_ignore.png')


if __name__ == '__main__':
    unittest.main()