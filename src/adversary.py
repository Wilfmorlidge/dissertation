import numpy as np
import tensorflow as tf
from decimal import Decimal
import random


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

def calculate_class_term_derivative_for_carlini_wagner_loss_function(image,model,learning_rate,target_class,k):
        image = tf.Variable(image)
        learning_rate = tf.constant(learning_rate)
        target_class = tf.constant(target_class)
        k = tf.constant([k])
        with tf.GradientTape() as watcher:
            watcher.watch(image)
            scores = model(image)
            retrieved_logit = scores[:1,target_class]
            if target_class == 0:
                filtered_scores = scores[:,1:]
            else:
                filtered_scores = tf.concat([scores[:target_class], scores[target_class+1:]], axis=0)
            maximal_logit = tf.reduce_max(filtered_scores)
            comparable_value = maximal_logit - retrieved_logit
            final = tf.reduce_max([comparable_value,k])
            weighted_result = learning_rate * final
        return np.array(watcher.gradient(weighted_result,image))
    

def calculate_euclidean_term_derivative_for_carlini_wagner_loss_function(image,pertubed_image):
    image = tf.Variable(tf.cast(image, tf.float64))
    pertubed_image = tf.constant(tf.cast(pertubed_image, tf.float64))
    with tf.GradientTape() as watcher:
        watcher.watch(image)
        l2_norm = tf.norm(image - pertubed_image, ord='euclidean')
    return np.array(watcher.gradient(l2_norm,image))

def optimal_image_calculator(outputs):
        # where starting points for Carlini Wagner is not 0, this calculates the optimal outcome from the trials
        minimal_loss = 999999999999999
        best_image = np.zeros((1,224,224,3))
        best_pertubation = np.zeros((1,224,224,3))
        for entry in outputs:
            if entry[1] < minimal_loss:
                minimal_loss = entry[1]
                best_image = entry[0]
                best_pertubation = entry[2]
        return np.squeeze(best_image,axis=0), np.squeeze(best_pertubation,axis=0)

def update_loss_function_for_carlini_wagner(image, pertubed_image, model, learning_rate, target_class, k):
    #this performs a gradient descent step by calculating the derivative of the loss for the current pertubation, and then subtracting it from the image.
    class_term_derivative = calculate_class_term_derivative_for_carlini_wagner_loss_function(pertubed_image,model,learning_rate,target_class,k)
    euclidean_term_derivative = calculate_euclidean_term_derivative_for_carlini_wagner_loss_function(image,pertubed_image)
    pertubation_delta = perform_arbitary_precision_addtion_of_numpy_arrays(euclidean_term_derivative, class_term_derivative)
    image = pertubed_image
    pertubed_image = perform_arbitary_precision_addtion_of_numpy_arrays(pertubed_image, -pertubation_delta)
    scores = model(pertubed_image)
    loss = np.linalg.norm(image - pertubed_image) + (learning_rate *max((max(np.delete(scores,target_class)) -scores[:1,target_class]),k))
    print('this is the loss' + str(loss))
    return image, pertubed_image, pertubation_delta, loss, scores

class AdversarialAttacks:
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

            cumulative_pertubation,image = calculate_cumulative_pertubation_for_deepfool(optimizer_values,image,cumulative_pertubation,logit_derivative_for_true_class,overshoot_scalar)
            scores = model(np.expand_dims(image, axis=0))

        if (np.linalg.norm(image-true_image) < maximum_pertubation_distance):
            return image, cumulative_pertubation
        else:
            return true_image, np.zeros((image.shape))

    def Carlini_Wagner_iteration_step(self,image,classification,model, class_list, maximal_loop = 50,temperature = 1, k = -0.2, learning_rate = 10000.0,maximum_pertubation_distance = 1000.0):
        np.set_printoptions(precision=20)
        current_class_list = np.copy(class_list).tolist()
        current_class_list.remove(classification)
        target_class = random.choice(current_class_list)
        starting_points = 1
        positions = np.random.uniform(-temperature,temperature,(starting_points, *image.shape))
        true_image = np.expand_dims(image,axis=0)
        outer_counter = 0
        outputs= []
        print(target_class)
        print(classification)

        #this section causes the gradient descent to be started from multiple points
        for entry in positions:
            print('now entering gradient descent trial ' + str(outer_counter))
            outer_counter += 1
            pertubation_delta = np.expand_dims(entry, axis=0)
            image = true_image
            pertubed_image = perform_arbitary_precision_addtion_of_numpy_arrays(image, pertubation_delta)
            scores = model(pertubed_image)
            print(np.argmax(scores))
            loss = np.linalg.norm(image - pertubed_image) + (learning_rate *max((max(np.delete(scores,target_class)) -scores[:1,target_class]),k))
            inner_counter = 0

            # this section calculates the derivative of the loss for the current image, and adds this as a pertubation, before checking
            # if the result correctly missclassifies the image.
            while ((np.argmax(scores) == classification)) and (inner_counter < maximal_loop):
                print('now entering pertubation cycle ' + str(inner_counter))
                inner_counter += 1
                image, pertubed_image, pertubation_delta,loss,scores = update_loss_function_for_carlini_wagner(image, pertubed_image, model, learning_rate, target_class, k)
            outputs.append((pertubed_image,loss,pertubation_delta))


        #this section identifies which of the calculated pertubed images produces the lowest loss.
        image, pertubation_delta = optimal_image_calculator(outputs)
        if (np.linalg.norm(image-true_image) < maximum_pertubation_distance):
            return image, pertubation_delta
        else:
            return true_image, np.zeros((image.shape))




def generate_pertubations(database,selected_model,selected_attack,class_list,trial_hyperparameters) :
        # this represents an extensible way of retrieving the iteration step function for the addition of pertubation.
        final_database = {'unpertubed_images': [],'pertubed_images': [],'pertubations': [], 'classifications': database['classifications']}
        #this causes the iteration function corresponding to the selected attack to be run for all images passed in
        for iteration in range (0,len(np.array(database['images']))):

            image = np.array(database['images'][iteration])
            final_database['unpertubed_images'].append(image)
          


            #this causes the pertubation to be calculated

            print('pertubing image:' + str(iteration))
            pertubed_image, pertubation = selected_attack(image,database['classifications'][iteration],selected_model,class_list)



            final_database['pertubed_images'].append(np.array(pertubed_image))
            final_database['pertubations'].append(np.array(pertubation))

        return final_database