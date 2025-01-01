import tensorflow as tf
import numpy as np
import tensorflow_datasets as tfds
from trial_runner.network_functions import normalize_database,calculate_output_data, update_cumulative_metrics
#from definitions import initialize_model, load_dataset
from trial_runner.adversary_handler import generate_pertubations
import itertools
import os
import threading
from threading import Event


print('is this instance running with cuda' + str(tf.test.is_built_with_cuda()))
print('available GPUs: ' + str(tf.config.list_physical_devices('GPU')))

def back_end_main_loop(iteration_size,iteration_number,selected_attack,selected_model,hyperparameter_settings,image_queue,graph_queue,progress_bar_queue,thread_killing_event):
    # this section clips the input hyperparameters, so that if not enough values are provided they cycle,
    # and if to many values are provided the ones at positions greater than iteration number get removed
    # and empty fields are filled with Nones to specify that default values should be used
    for counter in range (0,len(hyperparameter_settings)):
        if len(hyperparameter_settings[counter]) != 0:
            if len(hyperparameter_settings[counter]) > iteration_number:
            # Cut out all values right of position n-1
                hyperparameter_settings[counter] = hyperparameter_settings[counter][:iteration_number]
            elif len(hyperparameter_settings[counter]) < iteration_number:
            # Repeat the existing values until the list's length is n
                hyperparameter_settings[counter] = list(itertools.islice(itertools.cycle(hyperparameter_settings[counter]), iteration_number))
        else:
            hyperparameter_settings[counter] = [None] * iteration_number

    os.makedirs('./results', exist_ok=True)
    with open(f'./results/cumulative_metrics.txt', "w") as file:
        file.write(str({'accuracy': 0, 'mean_pertubation': 0, 'GMQ': 0, 'Sharpe_ratio':0}))

    for counter in range(0,iteration_number):
            run_adversarial_trial(iteration_size,selected_attack,selected_model,[sublist[counter] for sublist in hyperparameter_settings],counter)
            image_queue.put(counter)
            graph_queue.put(counter)
            progress_bar_queue.put(counter)
            update_cumulative_metrics(counter,iteration_size)
            if thread_killing_event.is_set():
                break


def run_adversarial_trial(iteration_size,selected_attack,selected_model,trial_hyperparameters,counter):
    print(trial_hyperparameters)
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
    calculate_output_data(final_database,selected_model[1],counter)



