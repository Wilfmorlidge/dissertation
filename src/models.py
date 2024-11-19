import tensorflow as tf
import tensorflow_datasets as tfds

def initialize_model(model_string):
    if (model_string == 'resnet'):
        return tf.keras.applications.ResNet50(
        include_top=True,
        weights="imagenet",
        classifier_activation="softmax"
    )
    elif (model_string == 'efficientnet'):
        return tf.keras.applications.EfficientNetB0(
            include_top=True,
            weights='imagenet',
            input_tensor=None,
            classifier_activation='softmax',
        )
    

def load_dataset(dataset_string):
    if (dataset_string == 'imagenette'):
        database, info = tfds.load('imagenette/320px-v2', split='validation', shuffle_files=True, with_info=True)
        class_list = [0,217,482,491,497,566,569,571,574,701]
        return database, info, class_list
    if (dataset_string == 'imagewoof'):
        database, info = tfds.load('imagewang/320px', split='validation', shuffle_files=True, with_info=True)
        class_list = [0,1,182,229,155,162,258,273,8,9,10,11,12,13,14,193,207,167,159,19]
        return database, info, class_list
