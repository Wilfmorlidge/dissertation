import tensorflow as tf
import numpy as np
import tensorflow_datasets as tfds
from network import normalize_database,calculate_output_data
#from definitions import initialize_model, load_dataset
from adversary import generate_pertubations


print('is this instance running with cuda' + str(tf.test.is_built_with_cuda()))
print('available GPUs: ' + str(tf.config.list_physical_devices('GPU')))


def run_adversarial_trial(iteration_size,selected_attack,selected_model,trial_hyperparameters):
    #this loads the database
    database, info = tfds.load('imagenette/320px-v2', split='validation', shuffle_files=True, with_info=True)
    class_list = [0,217,482,491,497,566,569,571,574,701]
    #database, info, class_list = load_dataset('imagenette')

    # this resizes and pre-processes the database images for use by the appropriate model
    normalized_database = normalize_database(database,iteration_size,selected_model[0], class_list)

    # this acquires the model

    # this applies adversarial pertubation
    print(selected_attack[1])
    print(selected_model[1])
    final_database = generate_pertubations(normalized_database,selected_model[1],selected_attack[1]['algorithm'],class_list,trial_hyperparameters)

    # this tests the pertubed data against the network
    predictions = calculate_output_data(final_database,selected_model[1])

    print(predictions)
    