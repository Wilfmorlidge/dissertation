import numpy as np
import tensorflow as tf

def find_logit_value(image,logit,model):
    # this function calculates the gradient of network logic (the value for a possible class prior to the final softmax layer) with respect to a single input image)
    image = tf.Variable(np.expand_dims(image, axis=0))
    with tf.GradientTape() as watcher:
        watcher.watch(image)
        #all calculations occuring in here are recorded by gradient tape, which allows the gradient of a valeu calculated in this indent to be automatically calculated
        #with respect to a value passed into this indent.
        score = model(image)
        retrieved_logit = score[:1,(logit-1):logit]
    return watcher.gradient(retrieved_logit,image)

class AdversarialAttacks:
    def DeepFool_iteration_step(self,image):
        return np.zeros(image.shape)

    def Carlini_Wagner_iteration_step(self,image):
        return np.zeros(image.shape)

def generate_pertubations(database,model,adversary_string) :
    if adversary_string == 'none':
        return database
    else:
        # this represents an extensible way of retrieving the iteration step function for the addition of pertubation.
        iteration_method_name = f"{adversary_string}_iteration_step"
        iteration_method = getattr(AdversarialAttacks(),iteration_method_name)
        pertubed_database = {'images': [], 'classifications': database['classifications']}
        #this causes the iteration function corresponding to the selected attack to be run for all images passed in
        for iteration in range (0,len(np.array(database['images']))):
            pertubed_database['images'].append(np.array(iteration_method(database['images'][iteration])))

        return pertubed_database