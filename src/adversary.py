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
        retrieved_logit = scores[:1,logit]
    return np.array(watcher.gradient(retrieved_logit,image))

class AdversarialAttacks:
    def DeepFool_iteration_step(self,image,classification,model):
        print('this is the shape of the original image' + str(np.array(image).shape))
        image1 = np.expand_dims(image, axis=0)
        print('this is the shape of the image altered ' + str(np.array(image1).shape))
        scores = model(image1)
        logit_derivative_for_true_class = find_logit_derivative_value(image,classification,model)
        print('step 1: identifying closest boundary via heuristic')
        #this iterates though all possible classes for each image
        minimum_absolute_boundary_distance = 999999999999999999999999999
        minimum_euclidean_distance = 9999999999999999999999
        minimum_heuristic = 99999999999999999999
        minimum_logit_derivative = 9999999999999999999
        nearest_class = 0
        for counter in range(0,999):
            if counter % 50 == 0:
                print('reviewing class:' + str(counter))
            if counter != classification:
                #this calculates the absolute distance between the class to be checked and the true class
                current_absolute_boundary_distance = np.array(abs(scores[:1,counter] - scores[:1,(classification-1):classification]))[0,0]
                #this calculates the euclidean distance between the derivatives of the logits for those classes
                logit_derivative_for_class_being_checked = find_logit_derivative_value(image,counter,model)
                current_euclidean_distance = np.linalg.norm(logit_derivative_for_class_being_checked - logit_derivative_for_true_class)
                if current_absolute_boundary_distance/current_euclidean_distance < minimum_heuristic:
                    minimum_absolute_boundary_distance = current_absolute_boundary_distance
                    minimum_euclidean_distance = current_euclidean_distance
                    minimum_logit_derivative = logit_derivative_for_class_being_checked
                    nearest_class = counter
        print('minimum absolute boundary_distance' + str(minimum_absolute_boundary_distance))
        print('minimum euclidean distance' + str(minimum_euclidean_distance))
        print('minimum logit derivative' + str(minimum_logit_derivative))
        print('nearest class')
        print('step 2: calculate pertubation')
        #this component finds the pertubation to be applied to the image
        pertubation = ((minimum_absolute_boundary_distance) / (minimum_euclidean_distance ** 2)) * (minimum_logit_derivative-logit_derivative_for_true_class)
        print('pertubation:' + str(pertubation))
        print('this is the shape of the pertubation' + str(np.squeeze(np.array(pertubation),axis=0).shape))
        image = image + np.squeeze(np.array(pertubation),axis=0)
        print('this is the shape of the pertubed image' + str(np.array(image).shape))

                

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
            print('pertubing image:' + str(iteration))
            pertubed_database['images'].append(np.array(iteration_method(database['images'][iteration],database['classifications'][iteration],model)))

        print('this is the shape of the database' + str(np.array(pertubed_database['images']).shape))
        return pertubed_database