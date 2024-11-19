import tensorflow as tf
import numpy as np
import tensorflow_datasets as tfds
from models import initialize_model
from window import denormalize_and_save_image
from PIL import Image

#resize the image to the size expected by the network
def resize_image(image):
    image = tf.image.resize(image, (224,224))
    return image

def re_label_image(label,class_list):
    print('this is one of the dumber problesm we have had'+ str(label))
    mapping = {i: class_list[i] for i in range(10)}
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
    print(normalized_database['classifications'])
    return normalized_database



def calculate_output_data(database,model):

    scores = model.predict(np.array(database['pertubed_images']))
    # provide human readable results
    confidences = []
    classes = []
    accuracy = 0
    for counter in range(0,len(scores)):
        denormalize_and_save_image(database['unpertubed_images'][counter],counter,'unpertubed')
        denormalize_and_save_image(database['pertubations'][counter],counter,'pertubation')
        denormalize_and_save_image(database['pertubed_images'][counter],counter,'pertubed')
        confidences.append(np.max(scores[counter]))
        this_class = np.argmax(scores[counter])
        if this_class == database['classifications'][counter]:
            accuracy += 1
        classes.append(this_class)
    accuracy = accuracy / len(scores)
    dictionary = {'confidences': np.array(confidences),
                  'classes': np.array(classes),
                  'accuracy': accuracy
    }
    return dictionary





# implement an adversarial flag, so that where true the normalized images are passed to adversary.py and pertubed before being used


