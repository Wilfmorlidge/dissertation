import numpy as np

def generate_pertubations(database,selected_model,selected_attack,class_list,trial_hyperparameters) :
        # this represents an extensible way of retrieving the iteration step function for the addition of pertubation.
        final_database = {'unpertubed_images': [],'pertubed_images': [],'pertubations': [], 'classifications': database['classifications']}
        #this causes the iteration function corresponding to the selected attack to be run for all images passed in
        for iteration in range (0,len(np.array(database['images']))):

            image = np.array(database['images'][iteration])
            final_database['unpertubed_images'].append(image)
          


            #this causes the pertubation to be calculated

            print('pertubing image:' + str(iteration))
            pertubed_image, pertubation = selected_attack(image,database['classifications'][iteration],selected_model,class_list,*trial_hyperparameters)



            final_database['pertubed_images'].append(np.array(pertubed_image))
            final_database['pertubations'].append(np.array(pertubation))

        return final_database