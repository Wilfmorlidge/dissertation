import tensorflow as tf
import numpy as np
import tensorflow_datasets as tfds
from PIL import Image
import os
import ast

#resize the image to the size expected by the network

def update_cumulative_metrics(counter,iteration_size):
    current_cumulative_values = None
    last_trials_values = None

    # this extracts the runnning value for our metrics, and the value for our metrics retrieved from the most recent trial
    # from the files where they are stored.
    with open(f"./results/cumulative_metrics.txt", "r") as file:
        # Read all lines into a list
        lines = file.readlines()
        current_cumulative_values = ast.literal_eval(lines[-1])
    with open(f"./results/trial_{counter}/metrics.txt", "r") as file:
        # Read all lines into a list
        lines = file.readlines()
        last_trials_values = ast.literal_eval(lines[-1])


    # this section calculates updates to the running values for our metrics

    current_cumulative_values['accuracy'] = ((current_cumulative_values['accuracy'] * (iteration_size * counter)) + (last_trials_values['accuracy'] * iteration_size)) / (iteration_size * (counter+1))
    current_cumulative_values['mean_pertubation'] = ((current_cumulative_values['mean_pertubation'] * (iteration_size * counter)) + (last_trials_values['mean_pertubation'] * iteration_size)) / (iteration_size * (counter+1))
    current_cumulative_values['GMQ'] = ((current_cumulative_values['GMQ'] * (iteration_size * counter)) + (last_trials_values['GMQ'] * iteration_size)) / (iteration_size * (counter+1))
    
    mean_for_trials = 0
    sum_mean_deviation_for_trials = 0

    inner_counter = 0
    for counter in range (0,(counter+1)):
        inner_counter = counter
        with open(f"./results/trial_{counter}/metrics.txt", "r") as file:
        # Read all lines into a list
            lines = file.readlines()
        entry_trial_values = ast.literal_eval(lines[-1])
        mean_for_trials += entry_trial_values['accuracy'] * iteration_size
    mean_for_trials = mean_for_trials / ((inner_counter+1)*iteration_size)

    
    for counter in range (0,(counter+1)):
        with open(f"./results/trial_{counter}/metrics.txt", "r") as file:
        # Read all lines into a list
            lines = file.readlines()
        entry_trial_values = ast.literal_eval(lines[-1])

        sum_mean_deviation_for_trials += (entry_trial_values['accuracy'] - mean_for_trials) ** 2


    if sum_mean_deviation_for_trials != 0:
        current_cumulative_values['Sharpe_ratio'] = (mean_for_trials /  (((1/(counter+1))*sum_mean_deviation_for_trials) ** 0.5))
    else:
        current_cumulative_values['Sharpe_ratio'] = 0

    with open(f"./results/cumulative_metrics.txt", 'a') as file:
        file.write(f'\n{current_cumulative_values}')




def append_images(database,inner_counter, outer_counter,directory_string):
    os.makedirs(directory_string, exist_ok=True)
    os.makedirs(f'{directory_string}/unpertubed', exist_ok=True)
    os.makedirs(f'{directory_string}/pertubation', exist_ok=True)
    os.makedirs(f'{directory_string}/pertubed', exist_ok=True)
    denormalize_and_save_image(database['unpertubed_images'][inner_counter],inner_counter,f'{directory_string}/unpertubed')
    denormalize_and_save_image(database['pertubations'][inner_counter],inner_counter,f'{directory_string}/pertubation')
    denormalize_and_save_image(database['pertubed_images'][inner_counter],inner_counter,f'{directory_string}/pertubed')



def denormalize_and_save_image(image,ident,destination):
    display_2 = Image.fromarray(((image - image.min()) / (image.max() - image.min()) * 255).astype(np.uint8))
    display_2.save(f'{destination}/image_{ident}.png')


def resize_image(image):
    image = tf.image.resize(image, (224,224))
    return image

def re_label_image(label,class_list):
    mapping = {i: class_list[i] for i in range(0,len(class_list))}
    return mapping.get(label,label)

def normalize_database(unnormalised_database,length,model_string,class_list, info='info not provided'):
    # shuffle the dataset and extract a subset for processing
    database = tfds.as_numpy((unnormalised_database.shuffle(buffer_size=1000)).take(length))
    normalized_database = {'images': [], 'classifications': []}
    counter = 0
    # extract and pre-process each image in the dataset
    for entry in database:
        pre_processing_method_name = f"tensorflow.keras.applications.{model_string}"
        module = __import__(pre_processing_method_name, fromlist=['preprocess_input'])
        # Get the preprocess_input function
        pre_processing_method = getattr(module, 'preprocess_input')
        counter += 1
        print('currently processing image #' + str(counter))
        normalized_database['images'].append(np.array(pre_processing_method(resize_image(entry['image']))))
        fixed_label = re_label_image(entry['label'], class_list)
        normalized_database['classifications'].append(fixed_label)
    return normalized_database



def calculate_output_data(database,model,outer_counter):

    scores = model.predict(np.array(database['pertubed_images']))
    # provide human readable results
    confidences = []
    classes = []
    accuracy = 0
    misplaceed_confidence_sum = 0
    pertubation_sum = 0
    directory_string = f'./results/trial_{outer_counter}'
    for inner_counter in range(0,len(scores)):
        append_images(database,inner_counter,outer_counter,directory_string)
        confidences.append(np.max(scores[inner_counter]))
        this_class = np.argmax(scores[inner_counter])
        pertubation_sum += np.linalg.norm(database['pertubed_images'][inner_counter]-database['unpertubed_images'][inner_counter])
        if this_class == database['classifications'][inner_counter]:
            accuracy += 1
        else:
            misplaceed_confidence_sum = np.max(scores[inner_counter])
        classes.append(this_class)


    accuracy = accuracy / len(scores)
    GMQ = misplaceed_confidence_sum / len(scores)
    mean_pertubation = pertubation_sum / len(scores)
    dictionary = {
                  'confidences': confidences,
                  'classes': classes,
                  'accuracy': accuracy,
                  'GMQ': GMQ,
                  'mean_pertubation': mean_pertubation

    }

    # this section writes the calculated metrics for the trial to a file
    # so that they can be stored persistently.
    with open(f'{directory_string}/metrics.txt', "w") as file:
        file.write(str(dictionary))






