import tensorflow as tf
import numpy as np
import tensorflow_datasets as tfds
from PIL import Image
import os

#resize the image to the size expected by the network

def append_images(database,inner_counter, outer_counter):
    directory_string = f'./images/trial_{outer_counter}'
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
    print(info)
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
    for inner_counter in range(0,len(scores)):
        append_images(database,inner_counter,outer_counter)
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
                  'confidences': np.array(confidences),
                  'classes': np.array(classes),
                  'accuracy': accuracy,
                  'GMQ': GMQ,
                  'mean_pertubation': mean_pertubation

    }
    return dictionary





