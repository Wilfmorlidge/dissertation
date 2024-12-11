import tensorflow as tf
import tensorflow_datasets as tfds
import sys

sys.path.insert(0, 'c:\\Users\\wilfm\\dissertation\\dissertation\\src\\attacks')

from DeepFool import DeepFool_iteration_step

from Carlini_Wagner import Carlini_Wagner_iteration_step

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
    elif (model_string == 'mobilenet'):
        return tf.keras.applications.MobileNetV2(
            input_shape=None,
            alpha=1.0,
            include_top=True,
            weights='imagenet',
            input_tensor=None,
            pooling=None,
            classes=1000,
            classifier_activation='softmax'
        )
    elif (model_string == 'vgg19'):
        return tf.keras.applications.VGG19(
            include_top=True,
            weights='imagenet',
            input_tensor=None,
            input_shape=None,
            pooling=None,
            classes=1000,
            classifier_activation='softmax'
        )
    
attack_dictionary = {
    'DeepFool' : {
        'algorithm': DeepFool_iteration_step,
        'hyperparameters': {
            'overshoot_scalar': [],
            'pertubation_cap': [],
            'maximum_loop': []
            }
        },
    'Carlini_Wagner' : {
        'algorithm':Carlini_Wagner_iteration_step,
        'hyperparameters': {
            'learning_rate': [],
            'starting_points': [],
            'temperature': []
            }
        } 
    }
    
model_dictionary = { 
    'resnet': (tf.keras.applications.ResNet50(
        include_top=True,
        weights="imagenet",
        classifier_activation="softmax"
    )),
    'efficientnet': (tf.keras.applications.EfficientNetB0(
            include_top=True,
            weights='imagenet',
            input_tensor=None,
            classifier_activation='softmax',
    )),
    'mobilenet': (tf.keras.applications.MobileNetV2(
            input_shape=None,
            alpha=1.0,
            include_top=True,
            weights='imagenet',
            input_tensor=None,
            pooling=None,
            classes=1000,
            classifier_activation='softmax'
    )),
    'vgg19': (tf.keras.applications.VGG19(
            include_top=True,
            weights='imagenet',
            input_tensor=None,
            input_shape=None,
            pooling=None,
            classes=1000,
            classifier_activation='softmax'
        ))
    }

image_trio_dictionary = {}
graph_dictionary = {}
    

def load_dataset(dataset_string):
    if (dataset_string == 'imagenette'):
        database, info = tfds.load('imagenette/320px-v2', split='validation', shuffle_files=True, with_info=True)
        class_list = [0,217,482,491,497,566,569,571,574,701]
        return database, info, class_list
    if (dataset_string == 'imagewoof'):
        database, info = tfds.load('imagewang/320px', split='validation', shuffle_files=True, with_info=True)
        class_list = [566,569,155,229,159,207,273,574,9,571,701,497,491,0,182,16,193,18,482]
        return database, info, class_list
    if (dataset_string == 'imagewang'):
        database, info = tfds.load('imagewang/320px', split='train', shuffle_files=True, with_info=True)
        class_list = [566,569,155,229,159,207,273,574,9,571,701,497,491,0,182,16,193,18,482]
        return database, info, class_list
    if (dataset_string == 'imagenet'):
        database, info = tfds.load('imagenet_r', split='test', shuffle_files=True, with_info=True)
        class_list = [range(0,999)]
        return database, info, class_list

