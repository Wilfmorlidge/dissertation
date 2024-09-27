import tensorflow as tf
import numpy as np
import tensorflow_datasets as tfds

# Load the ImageNet V2 dataset
database, info = tfds.load('imagenet_v2', split='test', with_info=True)


def normalize_database(unnormalised_database,length,info='info not provided'):
    print(info)

    def resize_image(image):
        image = tf.image.resize(image, (224,224))
        return image

    database = tfds.as_numpy(unnormalised_database.take(length))
    normalized_database = []
    for entry in database:
        normalized_database.append(resize_image(entry['image']))
    return np.array(normalized_database)


normalized_database = normalize_database(database,250)

# implement an adversarial flag, so that where true the normalized images are passed to adversary.py and pertubed before being used

#update to allow selection of model

model = tf.keras.applications.ResNet50(
    include_top=True,
    weights="imagenet",
    classifier_activation="softmax"
)

# Compile the model
model.compile(optimizer='sgd', loss='mean_squared_error')

# update to provide human readbale information, e.i what each image was and what it was classified as +
# percentage of correct classifications, as well as the actual loss function value.
print(model.predict(normalized_database))