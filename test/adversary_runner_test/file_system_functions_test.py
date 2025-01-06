# test_sample.py

import unittest
import numpy as np
import tensorflow as tf
import sys
import numpy.testing as npt
import tensorflow_datasets as tfds
from unittest.mock import patch
import os
import shutil

database, info = tfds.load('imagenette/320px-v2', split='validation', shuffle_files=True, with_info=True)

# adding Folder_2 to the system path
sys.path.insert(0, './src')

from trial_runner.file_system_functions import resize_image, normalize_database, calculate_output_data, append_images, denormalize_and_save_image, update_cumulative_metrics

class BasicNetworkTests(unittest.TestCase):
    #test that the resize function performs as expected
    def test_resize_array(self):
        npt.assert_array_equal(resize_image(np.ones((32, 32,3))), tf.image.resize(np.ones((32, 32,3)), (224,224)))

    #test that the image pre-processing function performs as expected
    def test_normalize_database(self):
        results = normalize_database(database,10,'resnet',[0,217,482,491,497,566,569,571,574,701])
        self.assertIsInstance(results, dict)
        self.assertIn('images',results)
        self.assertEqual(np.array(results['images']).shape, (10, 224, 224, 3))

    #test that the function making predictions and providing output data performs as expected
    @patch('trial_runner.file_system_functions.denormalize_and_save_image')
    def test_calculate_output_data(self,mock_denormalize_and_save_image):

        database = {'unpertubed_images': np.ones((2,224,224,3)), 'pertubations': np.zeros((2,224,224,3)), 'pertubed_images':np.ones((2,224,224,3)), 'classifications':np.ones((2,1))}
        model = tf.keras.applications.ResNet50(
        include_top=True,
        weights="imagenet",
        classifier_activation="softmax"
        )
        outer_counter = 'test_trial'
        if os.path.exists('./results'):
            shutil.rmtree('./results')
        calculate_output_data(database,model,outer_counter)
        os.path.isfile('./results/trial_test_trial/metrics.txt')

        with open(f'./results/trial_test_trial/metrics.txt', "r") as file:
            contents = file.read()
        
        self.assertEqual(contents,"{'confidences': [0.14476486, 0.14476486], 'classes': [111, 111], 'accuracy': 0.0, 'GMQ': 0.07238242775201797, 'mean_pertubation': 0.0}")

        if os.path.exists('./results'):
            shutil.rmtree('./results')

    @patch('trial_runner.file_system_functions.denormalize_and_save_image')
    def test_append_images(self,mock_denormalize_and_save_image):
        database = {'unpertubed_images' : np.random.uniform(-50,50,(224,224,3)),'pertubations':np.random.uniform(-50,50,(224,224,3)),'pertubed_images':np.random.uniform(-50,50,(224,224,3))}
        inner_counter = 0
        directory_string = f'./results/trial_test_trial'

        if os.path.exists('./results'):
            shutil.rmtree('./results')
        os.makedirs(directory_string, exist_ok=True)
        append_images(database,inner_counter,directory_string)
        self.assertTrue(os.path.isdir('./results/trial_test_trial/unpertubed'))
        self.assertTrue(os.path.isdir('./results/trial_test_trial/pertubation'))
        self.assertTrue(os.path.isdir('./results/trial_test_trial/pertubed'))
        self.assertTrue(mock_denormalize_and_save_image.call_count,3)

        if os.path.exists('./results'):
            shutil.rmtree('./results')


    def test_denormalize_and_save_image(self):
        image = np.random.uniform(-50,50,(224,224,3))
        inner_counter = 'test_image'
        destination = './results/trial_test_trial/unpertubed'
        if os.path.exists('./results'):
            shutil.rmtree('./results')
        os.makedirs(destination, exist_ok=True)
        denormalize_and_save_image(image,inner_counter,destination)
        self.assertTrue(os.path.isfile('./results/trial_test_trial/unpertubed/image_test_image.png'))
   
        if os.path.exists('./results'):
            shutil.rmtree('./results')

    def test_update_cumulative_metrics(self):
        if os.path.exists('./results'):
            shutil.rmtree('./results')

        os.makedirs('./results', exist_ok=True)
        with open(f'./results/cumulative_metrics.txt', "w") as file:
            file.write(str({'accuracy': 0, 'mean_pertubation': 0, 'GMQ': 0, 'Sharpe_ratio':0}))


        os.makedirs('./results/trial_0', exist_ok=True)
        with open(f'./results/trial_0/metrics.txt', "w") as file:
            file.write("{'confidences': [0.14476486, 0.14476486], 'classes': [111, 111], 'accuracy': 0.0, 'GMQ': 0.07238242775201797, 'mean_pertubation': 0.0}")

        counter = 0
        iteration_size = 2

        update_cumulative_metrics(counter,iteration_size)

        with open(f"./results/cumulative_metrics.txt", 'r') as file:
            lines = file.readlines()

        self.assertEqual(len(lines),2)
        self.assertEqual(lines[-1],"{'accuracy': 0.0, 'mean_pertubation': 0.0, 'GMQ': 0.07238242775201797, 'Sharpe_ratio': 0}")

if __name__ == '__main__':
    unittest.main()