import numpy as np
import tensorflow as tf
from decimal import Decimal
from PIL import Image

from window import denormalize_and_save_image


def find_logit_derivative_value(image,logit,model):
    # this function calculates the gradient of network logic (the value for a possible class prior to the final softmax layer) with respect to a single input image)
    image = tf.Variable(np.expand_dims(image, axis=0))
    with tf.GradientTape() as watcher:
        watcher.watch(image)
        #all calculations occuring in here are recorded by gradient tape, which allows the gradient of a valeu calculated in this indent to be automatically calculated
        #with respect to a value passed into this indent.
        scores = model(image)
        retrieved_logit = scores[:1,logit]
    return np.array(watcher.gradient(retrieved_logit,image))

def perform_arbitary_precision_addtion_of_numpy_arrays(array1,array2):
    operand1 = np.vectorize(Decimal)(array1.astype(str))
    operand2 = np.vectorize(Decimal)(array2.astype(str))
    result = operand1 + operand2
    return np.array(result, dtype=np.float64)

def find_nearest_class_boundary(optimizer_values,entry_class_pair,image,model,scores,logit_derivative_for_true_class):
    if entry_class_pair[0] != entry_class_pair[1]:
        #this calculates the absolute distance between the class to be checked and the true class
        current_absolute_boundary_distance = abs(scores[0][entry_class_pair[0]] - scores[0][entry_class_pair[1]])
        #this calculates the euclidean distance between the derivatives of the logits for those classes
        logit_derivative_for_class_being_checked = find_logit_derivative_value(image,entry_class_pair[0],model)
        current_euclidean_distance = np.linalg.norm(logit_derivative_for_class_being_checked - logit_derivative_for_true_class)
        current_heuristic = current_absolute_boundary_distance/current_euclidean_distance
        if current_heuristic < optimizer_values['minimum_heuristic']:
            optimizer_values = {'minimum_absolute_boundary_distance': current_absolute_boundary_distance,'minimum_euclidean_distance':current_euclidean_distance,'minimum_heuristic':current_heuristic,'minimum_logit_derivative':logit_derivative_for_class_being_checked,'nearest_class':entry_class_pair[0]}       
    return optimizer_values

def calculate_cumulative_pertubation_for_deepfool(optimizer_values,image,cumulative_pertubation,logit_derivative_for_true_class,overshoot_scalar=0.02):
        cumulative_pertubation = (np.squeeze(np.array((((optimizer_values['minimum_absolute_boundary_distance']) / (optimizer_values['minimum_euclidean_distance'] ** 2)) * (optimizer_values['minimum_logit_derivative']-logit_derivative_for_true_class)) + cumulative_pertubation), axis = 0)) * overshoot_scalar
        image = perform_arbitary_precision_addtion_of_numpy_arrays(image, cumulative_pertubation)    
        return cumulative_pertubation, image

class AdversarialAttacks:
    def DeepFool_iteration_step(self,image,classification,model):

        #in this section necessary variables are defined
        np.set_printoptions(precision=20)
        image = image.astype(np.float64)
        class_list = [0,217,482,491,497,566,569,571,574,701]
        scores = model(np.expand_dims(image, axis=0))
        loop_counter = 0
        cumulative_pertubation = np.zeros((224,224,3))
        overshoot_scalar = 0.2
        print('this is the overshoot scalar' + str(overshoot_scalar))


        while (np.argmax(scores) == classification) and (loop_counter < 50):
            loop_counter += 1
            print('now entering pertubation cycle ' + str(loop_counter))
            logit_derivative_for_true_class = find_logit_derivative_value(image,classification,model)
            #this iterates though all possible classes for each image
        
            optimizer_values = {'minimum_absolute_boundary_distance': 1e10,'minimum_euclidean_distance':1e10,'minimum_heuristic':1e10,'minimum_logit_derivative':1e10,'nearest_class':-1}
             
            for entry in class_list:
                entry_class_pair = (entry,classification)
                optimizer_values = find_nearest_class_boundary(optimizer_values,entry_class_pair,image,model,scores,logit_derivative_for_true_class)

            #this component finds the pertubation to be applied to the image

            cumulative_pertubation,image = calculate_cumulative_pertubation_for_deepfool(optimizer_values,image,cumulative_pertubation,logit_derivative_for_true_class,overshoot_scalar)
            scores = model(np.expand_dims(image, axis=0))

        return image, cumulative_pertubation

    def Carlini_Wagner_iteration_step(self,image,classification,model):
        return np.zeros(image.shape)




def generate_pertubations(database,model,adversary_string) :
    if adversary_string == 'none':
        final_database = {'unpertubed_images': [],'pertubed_images': [],'pertubations': [], 'classifications': database['classifications']}
        for iteration in range (0,len(np.array(database['images']))):
            image = np.array(database['images'][iteration])
            final_database['unpertubed_images'].append(image)
            final_database['pertubations'].append(np.zeros((image.shape)))
            final_database['pertubed_images'].append(image)
        return final_database
    else:
        # this represents an extensible way of retrieving the iteration step function for the addition of pertubation.
        iteration_method_name = f"{adversary_string}_iteration_step"
        iteration_method = getattr(AdversarialAttacks(),iteration_method_name)
        final_database = {'unpertubed_images': [],'pertubed_images': [],'pertubations': [], 'classifications': database['classifications']}
        #this causes the iteration function corresponding to the selected attack to be run for all images passed in
        for iteration in range (0,len(np.array(database['images']))):

            image = np.array(database['images'][iteration])
            final_database['unpertubed_images'].append(image)
          


            #this causes the pertubation to be calculated

            print('pertubing image:' + str(iteration))
            pertubed_image, pertubation = iteration_method(image,database['classifications'][iteration],model)



            final_database['pertubed_images'].append(np.array(pertubed_image))
            final_database['pertubations'].append(np.array(pertubation))

        return final_database