import numpy as np
import tensorflow as tf

def find_logit_value(image,logit,model):
    # this function calculates the gradient of network logic (the value for a possible class prior to the final softmax layer) with respect to a single input image)
    image = np.expand_dims(image, axis=0)
    with tf.GradientTape() as watcher:
        #all calculations occuring in here are recorded by gradient tape, which allows the gradient of a valeu calculated in this indent to be automatically calculated
        #with respect to a value passed into this indent.
        score = model(image)
    grad = watcher.gradient(model.trainable_variables,image)


def generate_pertubations(database,model,adversary_string) :
    if adversary_string == 'none':
        return database
    elif adversary_string == 'test':
        # this option exists for me to test the find logit value function and will be removed from the final product
        macguffin = find_logit_value(database['images'][0],database['classifications'][0],model)
        return database