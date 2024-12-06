import numpy as np
import tensorflow as tf
from decimal import Decimal


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

def perform_arbitary_precision_addition_of_numpy_arrays(array1,array2):
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

def calculate_cumulative_pertubation(optimizer_values,image,cumulative_pertubation,logit_derivative_for_true_class,overshoot_scalar=0.02):
        cumulative_pertubation = (np.squeeze(np.array((((optimizer_values['minimum_absolute_boundary_distance']) / (optimizer_values['minimum_euclidean_distance'] ** 2)) * (optimizer_values['minimum_logit_derivative']-logit_derivative_for_true_class)) + cumulative_pertubation), axis = 0)) * overshoot_scalar
        image = perform_arbitary_precision_addition_of_numpy_arrays(image, cumulative_pertubation)    
        return cumulative_pertubation, image

def DeepFool_iteration_step(self,image,classification,model, class_list, maximal_loop = 50, overshoot_scalar = 0.2, maximum_pertubation_distance = 1000.0):

        #in this section necessary variables are defined
        np.set_printoptions(precision=20)
        image = image.astype(np.float64)
        true_image = image
        scores = model(np.expand_dims(image, axis=0))
        loop_counter = 0
        cumulative_pertubation = np.zeros((image.shape))
        print('this is the overshoot scalar' + str(overshoot_scalar))


        while ((loop_counter < maximal_loop) and (np.argmax(scores) == classification)):
            loop_counter += 1
            print('now entering pertubation cycle ' + str(loop_counter))
            logit_derivative_for_true_class = find_logit_derivative_value(image,classification,model)
            #this iterates though all possible classes for each image
        
            optimizer_values = {'minimum_absolute_boundary_distance': 1e10,'minimum_euclidean_distance':1e10,'minimum_heuristic':1e10,'minimum_logit_derivative':1e10,'nearest_class':-1}
             
            for entry in class_list:
                entry_class_pair = (entry,classification)
                optimizer_values = find_nearest_class_boundary(optimizer_values,entry_class_pair,image,model,scores,logit_derivative_for_true_class)

            #this component finds the pertubation to be applied to the image

            cumulative_pertubation,image = calculate_cumulative_pertubation(optimizer_values,image,cumulative_pertubation,logit_derivative_for_true_class,overshoot_scalar)
            scores = model(np.expand_dims(image, axis=0))

        if (np.linalg.norm(image-true_image) < maximum_pertubation_distance):
            return image, cumulative_pertubation
        else:
            return true_image, np.zeros((image.shape))

