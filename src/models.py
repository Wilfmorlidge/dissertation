import tensorflow as tf


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