import numpy as np
import tensorflow as tf
from decimal import Decimal
import random


def perform_arbitary_precision_addtion_of_numpy_arrays(array1,array2):
    operand1 = np.vectorize(Decimal)(array1.astype(str))
    operand2 = np.vectorize(Decimal)(array2.astype(str))
    result = operand1 + operand2
    return np.array(result, dtype=np.float64)


def calculate_class_term_derivative(image,model,learning_rate,target_class,k):
        image = tf.Variable(image)
        learning_rate = tf.constant(learning_rate)
        target_class = tf.constant(target_class)
        k = tf.constant([k])
        with tf.GradientTape() as watcher:
            watcher.watch(image)
            scores = model(tf.convert_to_tensor(image, dtype=tf.float64))
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
    

def calculate_euclidean_term_derivative(image,pertubed_image):
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

def update_loss_function(image, pertubed_image, model, learning_rate, target_class, k):
    #this performs a gradient descent step by calculating the derivative of the loss for the current pertubation, and then subtracting it from the image.
    class_term_derivative = calculate_class_term_derivative(pertubed_image,model,learning_rate,target_class,k)
    euclidean_term_derivative = calculate_euclidean_term_derivative(image,pertubed_image)
    pertubation_delta = perform_arbitary_precision_addtion_of_numpy_arrays(euclidean_term_derivative, class_term_derivative)
    image = pertubed_image
    pertubed_image = perform_arbitary_precision_addtion_of_numpy_arrays(pertubed_image, -pertubation_delta)
    scores = model(pertubed_image)
    loss = np.linalg.norm(image - pertubed_image) + (learning_rate *max((max(np.delete(scores,target_class)) -scores[:1,target_class]),k))
    print('this is the loss' + str(loss))
    return image, pertubed_image, pertubation_delta, loss, scores


def Carlini_Wagner_iteration_step(image,classification,model, class_list, learning_rate, starting_points,temperature, k,perubation_cap, maximal_loop):
       
        # this section checks if hyperparameters are undefined and sets them to default
        if learning_rate == None:
             learning_rate = 100.0
        if starting_points == None:
            starting_points = 1.0
        if temperature == None:
            temperature = 1
        if k == None:
            k = 0.2
        if perubation_cap == None:
            perubation_cap = 1000.0
        if maximal_loop == None:
            maximal_loop = 50
       
        np.set_printoptions(precision=20)
        current_class_list = np.copy(class_list).tolist()
        current_class_list.remove(classification)
        target_class = random.choice(current_class_list)
        positions = np.random.uniform(-temperature,temperature,(int(starting_points), *image.shape))
        true_image = np.expand_dims(image,axis=0)
        outer_counter = 0
        outputs= []
        print(target_class)
        print(classification)#

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
                image, pertubed_image, pertubation_delta,loss,scores = update_loss_function(image, pertubed_image, model, learning_rate, target_class, k)
            outputs.append((pertubed_image,loss,pertubation_delta))


        #this section identifies which of the calculated pertubed images produces the lowest loss.
        image, pertubation_delta = optimal_image_calculator(outputs)
        if (np.linalg.norm(image-true_image) < perubation_cap):
            return image, pertubation_delta
        else:
            return true_image, np.zeros((image.shape))


