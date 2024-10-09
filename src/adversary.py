import random
import numpy as np

def generate_pertubations(database,model,adversary) :
    if adversary == 'none':
        return database
    elif adversary == 'test':
        for counter in range(0,len(database['images'])):
            image = database['images'][counter]
            image = np.zeros((224,224,3))
            database['images'][counter] = image
        return database