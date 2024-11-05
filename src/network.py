import tensorflow as tf
import numpy as np
import tensorflow_datasets as tfds
from models import initialize_model
from window import denormalize_and_save_image

#resize the image to the size expected by the network
def resize_image(image):
    image = tf.image.resize(image, (224,224))
    return image

def re_label_image(label):
    mapping = {0:0,1:217,2:482,3:491,4:497,5:566,6:569,7:571,8:574,9:701}
    return mapping.get(label,label)

def normalize_database(unnormalised_database,length,model_string,info='info not provided'):
    print(info)
    # convert the database to the appropriate file type.
    database = tfds.as_numpy(unnormalised_database.take(length))
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
        fixed_label = re_label_image(entry['label'])
        normalized_database['classifications'].append(fixed_label)
    return normalized_database



def calculate_output_data(database,model):

    scores = model.predict(np.array(database['images']))
    # provide human readable results
    confidences = []
    classes = []
    accuracy = 0
    for counter in range(0,len(scores)):
        denormalize_and_save_image(database['images'][counter],counter)
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


