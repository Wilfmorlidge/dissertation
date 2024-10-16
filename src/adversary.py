import numpy as np
import tensorflow as tf

def find_logit_derivative_value(image,logit,model):
    # this function calculates the gradient of network logic (the value for a possible class prior to the final softmax layer) with respect to a single input image)
    image = tf.Variable(np.expand_dims(image, axis=0))
    with tf.GradientTape() as watcher:
        watcher.watch(image)
        #all calculations occuring in here are recorded by gradient tape, which allows the gradient of a valeu calculated in this indent to be automatically calculated
        #with respect to a value passed into this indent.
        scores = model(image)
        retrieved_logit = scores[:1,(logit-1):logit]
    return watcher.gradient(retrieved_logit,image)

class AdversarialAttacks:
    def DeepFool_iteration_step(self,image,classification,model):
        image = np.expand_dims(image, axis=0)
        scores = model(image)
        print('step 1: identifying closest boundary')
        print('step 1a: calculating absolute distance in logits')
        for counter in range(0,999):
            #print('checking class boundary:' + str(counter))
            if counter != classification:
                current_absolute_boundary_distance = abs(scores[:1,(counter-1):counter] - scores[:1,(classification-1):classification])
                print('current absolute boundary distance:' + str(current_absolute_boundary_distance))
                

        return np.zeros(image.shape)

    def Carlini_Wagner_iteration_step(self,image,classification,model):
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
            print('pertubing image:' + str(iteration))
            pertubed_database['images'].append(np.array(iteration_method(database['images'][iteration],database['classifications'][iteration],model)))

        return pertubed_database