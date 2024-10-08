import tensorflow as tf
import numpy as np
import tensorflow_datasets as tfds
from models import initialize_model


def resize_image(image):
    image = tf.image.resize(image, (224,224))
    return image

def normalize_database(unnormalised_database,length,info='info not provided'):
    print(info)

    database = tfds.as_numpy(unnormalised_database.take(length))
    normalized_database = {'images': [], 'classifications': []}
    for entry in database:
        normalized_database['images'].append(resize_image(entry['image']))
        normalized_database['classifications'].append(entry['label'])
    return normalized_database


def run_prediction(database,model_string = 'resnet'):
    model = initialize_model(model_string)

    # Compile the model
    model.compile(optimizer='sgd', loss='mean_squared_error')

    # update to provide human readbale information, e.i what each image was and what it was classified as +
    # percentage of correct classifications, as well as the actual loss function value.
    scores = model.predict(np.array(database['images']))
    confidences = []
    classes = []
    accuracy = 0
    for counter in range(0,len(scores)):
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


