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

def perform_arbitary_precision_addtion_of_numpy_arrays(array1,array2):
    operand1 = np.vectorize(Decimal)(array1.astype(str))
    operand2 = np.vectorize(Decimal)(array2.astype(str))
    result = operand1 + operand2
    #print('this is the result to arbitary precision' + str(result))
    #print('this is the result to float64 precision' + str(np.array(result, dtype=np.longdouble)))
    return np.array(result, dtype=np.float64)

class AdversarialAttacks:
    def DeepFool_iteration_step(self,image,classification,model):
        np.set_printoptions(precision=20)
        #print('perhaps i am an idiot' + str(50-1e-13))
        #print('maybe god is a fool' + str(np.array([50-1e-13], dtype=np.float64)))
        thing = tf.constant([0.12345678901234567890], dtype=tf.float64)
  
        image = image.astype(np.float64)
        class_list = [0,217,482,491,497,566,569,571,574,701]
        #print('this is the shape of the original image' + str(np.array(image).shape))
        #print('this is the original image' +str(np.array(image)))
        image1 = np.expand_dims(image, axis=0)
        scores = model(image1)
        loop_counter = 0
        cumulative_pertubation = 0
        overshoot_scalar = 1
        while (np.argmax(scores) == classification) and (loop_counter < 30):
            loop_counter += 1
            print('now entering pertubation cycle ' + str(loop_counter))
            logit_derivative_for_true_class = find_logit_derivative_value(image,classification,model)
            #print('step 1: identifying closest boundary via heuristic')
            #this iterates though all possible classes for each image
            minimum_absolute_boundary_distance = 999999999999999999999999999
            minimum_euclidean_distance = 9999999999999999999999
            minimum_heuristic = 99999999999999999999
            minimum_logit_derivative = 9999999999999999999
            nearest_class = 0
            for entry in class_list:
                #print('reviewing class:' + str(entry))
                if entry != classification:
                    #this calculates the absolute distance between the class to be checked and the true class
                    current_absolute_boundary_distance = np.array(abs(scores[:1,entry] - scores[:1,(classification-1):classification]),dtype=np.float64)[0,0]
                    #this calculates the euclidean distance between the derivatives of the logits for those classes
                    logit_derivative_for_class_being_checked = find_logit_derivative_value(image,entry,model)
                    current_euclidean_distance = np.linalg.norm(logit_derivative_for_class_being_checked - logit_derivative_for_true_class)
                    if current_absolute_boundary_distance/current_euclidean_distance < minimum_heuristic:
                        minimum_absolute_boundary_distance = current_absolute_boundary_distance
                        minimum_euclidean_distance = current_euclidean_distance
                        minimum_logit_derivative = logit_derivative_for_class_being_checked
                        nearest_class = entry
            print('minimum absolute boundary_distance ' + str(minimum_absolute_boundary_distance))
            print('minimum euclidean distance ' + str(minimum_euclidean_distance))
            #print('minimum logit derivative ' + str(minimum_logit_derivative))
            print('nearest class ' + str(nearest_class))
            #print('step 2: calculate pertubation')
            #this component finds the pertubation to be applied to the image
            cumulative_pertubation = (((minimum_absolute_boundary_distance) / (minimum_euclidean_distance ** 2)) * (minimum_logit_derivative-logit_derivative_for_true_class)) + cumulative_pertubation
            print('pertubation:' + str(cumulative_pertubation))
            #print('this is the shape of the pertubation' + str(np.squeeze(np.array(pertubation),axis=0).shape))
            image = perform_arbitary_precision_addtion_of_numpy_arrays(image, (np.squeeze(np.array(cumulative_pertubation, dtype = np.longdouble),axis=0)*overshoot_scalar))
            #print('this is the shape of the pertubed image' + str(np.array(image).shape))
            print('this is the pertubed image' + str(image))
            image1 = np.expand_dims(image, axis=0)
            scores = model(image1)
                

        return image

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

            #display_1 = Image.fromarray(((database['images'][iteration] - database['images'][iteration].min()) / (database['images'][iteration].max() - database['images'][iteration].min()) * 255).astype(np.uint8))
            #display_1.save(f'unpertubed_image_{iteration}.png')


            print('pertubing image:' + str(iteration))
            pertubed_image = np.array(iteration_method(database['images'][iteration],database['classifications'][iteration],model))
            pertubed_database['images'].append(pertubed_image)

        print('this is the shape of the database' + str(np.array(pertubed_database['images']).shape))
        return pertubed_database