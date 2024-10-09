import numpy as np
import tensorflow as tf

def find_logit_value(image,logit,model):
    truth = np.zeros((1,1000))
    truth[0,(logit)] = 1
    image = np.expand_dims(image, axis=0)
    loss_fn = tf.keras.losses.CategoricalCrossentropy()
    with tf.GradientTape() as watcher:
        score = model(image)
        loss = loss_fn(truth,score)
        print(loss)
    grad = watcher.gradient(loss,model.trainable_variables)


def generate_pertubations(database,model,adversary_string) :
    if adversary_string == 'none':
        return database
    elif adversary_string == 'test':
        # this option exists for me to test the find logit value function and will be removed from the final product
        macguffin = find_logit_value(database['images'][0],database['classifications'][0],model)
        return database