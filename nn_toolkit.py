'''
A Deep learning tool kit with a Neural Network model implementation, in addition to various helper functions to ease the applications.
'''
# Importing necessary librarise:
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import image
from PIL import Image
from os import listdir, getcwd
import pandas as pd
from datetime import datetime
datetime.now()

# 01 ________________________________________________________________________________________________________________________________________________________________

def prepare_image_data(images_path, resize = 64, label_tag = 1, show_rejected_images = False):
    '''
    A function to prepare one class of images into column arrays. Works only on images of RGB color mode.
    
    Arguments:
        images_path: A path containing the class of images.
        resize: The hight and width in pixils to get all images into the same square dimension of (resize * resize * 3), where 3 is for RGB channels.
        label_tag : A categorical label tag whether 0 or 1, 1 by default.
        show_rejected_images : Whether to show the rejected images or not, they are saved by default in a returned list 'rejected_pics', False by default.
    
    Returns:
        pics_array: A 4D array of shape (number of converted images, resize, resize, 3) containing the arrays of converted images.
        labels_array: A 2D array of shape (1, number of converted images) containing the lagel tage assigned.
        rejected_pics: A list containing the name of each rejected image.
    '''
    pics_list = list()
    rejected_pics = list()
      
    for picture in listdir(images_path):
        pic = Image.open(images_path + picture)
        
        try:
            pic_resized = pic.resize((resize, resize))
            pic_array = np.asarray(pic_resized)
            assert(np.shape(pic_array) == (resize, resize, 3))

        except:
            rejected_pics.append((picture, pic))
            if show_rejected_images:
                print(picture)
                print(pic)
                plt.imshow(pic)
                plt.show()
                print('-' * 50)
            continue
            
        pics_list.append(pic_array)
        
    pics_array = np.array(pics_list).reshape((len(pics_list), resize, resize, 3))
    labels_array = np.zeros((1, len(pics_list))) + label_tag
    
    print('Pics Array shape:', np.shape(pics_array))
    print('Labels Array shape:', np.shape(labels_array))
    
    return pics_array, labels_array, rejected_pics

# 02 ________________________________________________________________________________________________________________________________________________________________

def merge_shuffle_split(images_array_1, labels_array_1, images_array_2, labels_array_2, validation_split = 0.2, seed = 123):
    '''
    Given 4 arrays of images data and their labels, returns shuffled train and test data sets.
    '''
    # Merging the images and labels arrays (merge)
    images_array = np.concatenate((images_array_1, images_array_2), axis = 0)
    labels_array = np.concatenate((labels_array_1, labels_array_2), axis = 1)
    
    # Creating indices to shuffle (shuffle)
    indices = np.arange(images_array.shape[0])
    np.random.shuffle(indices)
    
    # Shuffling the merged arrays
    images_array = images_array[indices]
    labels_array = labels_array[:, indices]
    
    # Creating the train sets (split)
    train_set_x_orig = images_array[:int((1 - validation_split) * len(images_array))]
    train_set_y = labels_array[:, :int((1 - validation_split) * len(images_array))]
    
    # Creating the test sets
    test_set_x_orig = images_array[int((1 - validation_split) * len(images_array)):]
    test_set_y = labels_array[:, int((1 - validation_split) * len(images_array)):]
    
    print('Output Shapes:')
    print('train_set_x_orig:', np.shape(train_set_x_orig))
    print('train_set_y:', np.shape(train_set_y))
    print('test_set_x_orig:', np.shape(test_set_x_orig))
    print('test_set_y:', np.shape(test_set_y))
    
    return train_set_x_orig, train_set_y, test_set_x_orig, test_set_y

# 03 ________________________________________________________________________________________________________________________________________________________________

def prepare_image_arrays(set_x, standardize = 'pixil_max'):
    set_x_flatten = set_x.reshape(set_x.shape[0], -1).T
#     if standardize == 'pixil_max':
    set_x_flatten_stdr = set_x_flatten / 255.
#     else:
#         set_x_flatten_stdr = (set_x_flatten - np.mean(set_x_flatten)) / np.std(set_x_flatten)
    print('Shape of Flatten and Standardized array:', np.shape(set_x_flatten_stdr))
    return set_x_flatten_stdr

# 04 ________________________________________________________________________________________________________________________________________________________________

def sigmoid(set_x):
    return (1 / (1 + np.exp(-set_x)))

# 05 ________________________________________________________________________________________________________________________________________________________________

def initialize_parameters(dim):
    b = 0
    w = np.random.randn(dim, 1) * 0
    return w, b

# 06 ________________________________________________________________________________________________________________________________________________________________

def cost_calc(a, set_y):
    return - np.sum(np.add(np.dot(set_y, np.log(a.T)), np.dot(1 - set_y, np.log(1 - a.T)))) / set_y.shape[1]

# 07 ________________________________________________________________________________________________________________________________________________________________

def forward_pass(set_x, set_y, w, b):
    costs = list()
    z = np.dot(w.T, set_x) + b
    a = sigmoid(z)
    cost = cost_calc(a, set_y)
    costs.append(cost)
    return w, b, z, a, costs

# 08 ________________________________________________________________________________________________________________________________________________________________

def optimize(set_x, set_y, num_iterations, learning_rate, print_cost):
    m = set_x.shape[1]
    w, b = initialize_parameters(set_x.shape[0])
    for i in range(num_iterations):
        w, b, z, a, costs = forward_pass(set_x, set_y, w, b)
        dz = a - set_y
        dw = np.dot(set_x, dz.T) / m
        db = np.sum(dz) / m
        w -= learning_rate * dw
        b -= learning_rate * db
        if i % 1000 == 0 and print_cost:
            print('Cost after iteration {}: {}'.format(i, costs[-1].round(4)))
        
    return w, b, z, a, costs

# 09 ________________________________________________________________________________________________________________________________________________________________

def predict(w, b, set_x, set_y):
    w, b, z, a, costs = forward_pass(set_x, set_y, w, b)
    yhat = a
    for i in range(a.shape[1]):
        if a[0, i] > 0.5:
            yhat[0, i] = 1
        else:
            yhat[0, i] = 0
    return yhat

# 10 ________________________________________________________________________________________________________________________________________________________________

def logistic_nn_model(set_x_train, set_y_train, set_x_test, set_y_test, num_iterations = 1000, learning_rate = 0.001, print_cost = False):
    
    w, b, z, a, costs = optimize(set_x_train, set_y_train, num_iterations, learning_rate, print_cost)
    
    yhat_train = predict(w, b, set_x_train, set_y_train)
    
    yhat_test = predict(w, b, set_x_test, set_y_test)
    
    train_acc = (100 - np.mean(np.abs(yhat_train - set_y_train)) * 100).round(4)
    test_acc = (100 - np.mean(np.abs(yhat_test - set_y_test)) * 100).round(4)
    
    print('Train Accuracy: {}%'.format(train_acc))
    print('Test Accuracy: {}%'.format(test_acc))
    
    model_summary = {'Model No. ': str(datetime.now()), 'Train X Shape': np.shape(set_x_train), 'Train Y Sahpe': np.shape(set_y_train),
                    'Test X Shape': np.shape(set_x_test), 'Test Y Sahpe': np.shape(set_y_test),
                     'Iterations': num_iterations, 'alpha': learning_rate,
                     'w': w, 'b': b, 'Costs': costs,
                    'Train Accuracy': train_acc, 'Test Accuracy': test_acc}
    return model_summary

# 11 ________________________________________________________________________________________________________________________________________________________________

def models_summary(models_list):
    models_df = pd.DataFrame.from_dict(models_list)
    
    best_test_accuracy = models_df['Test Accuracy'].max()
    
    best_test_models = models_df[models_df['Test Accuracy'] == best_test_accuracy]
    
    local_best_train = best_test_models['Train Accuracy'].max()
    
    top_model_number = models_df.index[(models_df['Test Accuracy'] == best_test_accuracy) & (models_df['Train Accuracy'] == local_best_train)].tolist()
    print('Top models, based on Test then Train accuracies:', top_model_number)
    return models_df, top_model_number[0]

# 12 ________________________________________________________________________________________________________________________________________________________________

def predict_sample(sample_path, w, b):
    pics_array, labels_array, rejected_pics = prepare_image_data(sample_path, label_tag = 1, show_rejected_images = False)
    set_x_flatten_stdr = prepare_image_arrays(pics_array, standardize = 'pixil_max')
    yhat = predict(w, b, set_x_flatten_stdr, labels_array)
    return yhat

# 13 ________________________________________________________________________________________________________________________________________________________________

def deep_nn_model(X, Y, X_test, Y_test, layer_structure = [4, 3, 1], iterations = 10, alpha = 0.01,
                  lambd = 0, dropout_layers = [], keep_prob = 1,
                  print_cost = True, print_every = 500, show_plots = True):
    start = datetime.now() # to measure training time (start).
    model_structure = layer_structure.copy() # to include the inpout layer of shape (X.shape[0], number of images / examples).
    model_structure.insert(0, X.shape[0]) # including the input layer and its dimensions.
    num_layers = len(model_structure) # total number of layers in the model including the input layer (layer 0).
    L = num_layers - 1 # number of hidden layers in the model.
    
    ## Initialize the parameters:
    P = dict() # parameters dictionary
    
    for l in range(1, num_layers): # for every heddin layer in the model, create the set of parameters below.
        P['W' + str(l)] = np.random.randn(model_structure[l], model_structure[l - 1]) * np.sqrt(2 / model_structure[l - 1]) # random initialization with 'He' scaling.
        P['b' + str(l)] = np.zeros((model_structure[l], 1)) # zero inialization.
        
    # Dictionaries to run and save the forward and backward propagation results:
    Z = dict() # linear forward pass.
    A = dict() # forward activation.
    D = dict() # dropout mask.
    dZ = dict() # linear backward pass.
    dA = dict() # backward activation.
    dP = dict() # parameters gradiants.
    
    A['A0'] = X # to intialize the forward pass.
    m = Y.shape[1] # number of traning examples.
    costs = list() # to save cost values per iteration.
    
    ## Forward Propagation:
    for i in range(iterations): # over each iteration.
        for l in range(1, num_layers): # for every layer in the model>
            Z['Z' + str(l)] = np.dot(P['W' + str(l)], A['A' + str(l - 1)]) + P['b' + str(l)] # linear forward pass.
            if l < L: # if this is not the last hidden layer in the model then:
                A['A' + str(l)] = np.maximum(0, Z['Z' + str(l)]) # calculate the activation as a RelU function.
                if (len(dropout_layers) != 0) and (keep_prob < 1.0) and (l in dropout_layers):
                    D['D' + str(l)] = np.random.rand(A['A' + str(l)].shape[0], A['A' + str(l)].shape[1])
                    D['D' + str(l)] = (D['D' + str(l)] < keep_prob).astype('int')
                    A['A' + str(l)] *= D['D' + str(l)] / keep_prob
            else:
                A['A' + str(l)] = 1 / (1 + np.exp(-(Z['Z' + str(l)]))) # else if it's the last hidden layer, then calculate the activation as a 
                                                                       # sigmoid fucntion since the task is binary classification.
                    
        cross_entropy_cost = - np.sum(np.add(np.dot(Y, np.log(A['A' + str(L)].T)), np.dot(1 - Y, np.log(1 - A['A' + str(L)].T)))) / m # calculates the cross entropy (first part of the cost).
        L2_regularization_cost = 0
        for l in range(1, num_layers):
            L2_regularization_cost += np.sum(np.square(P['W' + str(l)]))
        L2_regularization_cost = L2_regularization_cost * lambd / (2 * m)
        cost = cross_entropy_cost + L2_regularization_cost
        cost = np.squeeze(cost) # insure it's not a rank one array.
        assert(cost.shape == ()) # raise error if it is not a scalar.
        costs.append(cost) # append it to the costs list.
        
        Yhat_train = A['A' + str(L)] # final output (Yhat).
        Yhat_train = np.array((Yhat_train > 0.5) * 1).reshape(1, m) # converting to 0s and 1s based on 0.5 threshold.
        train_acc = (100 - np.mean(np.abs(Yhat_train - Y)) * 100).round(4) # calculate accuracy using the final output.
        
        if print_cost and i % print_every == 0: # to print the cost and training accuracy if set to Ture, every number of iterations based on 'print_every' argument.
            print('Iteration {} : Cost: {}, Train Acc.: {}%'.format(i, cost.round(4), train_acc.round(4))) # round the cost and accuracy and print them.
    
    ## Backward Propagation:   
        dA['dA' + str(L)] = - (np.divide(Y, A['A' + str(L)]) - np.divide(1 - Y, 1 - A['A' + str(L)])) # initializing backward propagation.
        dZ['dZ' + str(L)] = dA['dA' + str(L)] * A['A' + str(L)] * (1 - A['A' + str(L)]) # sigmoid activation backwared
        
        for l in reversed(range(1, num_layers)): # for every layer in the model, going last to first, calculate:
            dP['dW' + str(l)] = np.dot(dZ['dZ' + str(l)], A['A' + str(l - 1)].T) / m + (P['W' + str(l)] * lambd / m)# Ws gradiants with regularization.
            dP['db' + str(l)] = np.sum(dZ['dZ' + str(l)], axis = 1, keepdims = True) / m # bs gradiants.
            if l > 1: # As long as this is not the first layer, then calcualte:
                dA['dA' + str(l - 1)] = np.dot(P['W' + str(l)].T, dZ['dZ' + str(l)]) # Relu activations gradiants.
                if (len(dropout_layers) != 0) and (keep_prob < 1.0) and (l - 1 in dropout_layers):
                    dA['dA' + str(l - 1)] *= D['D' + str(l - 1)] / keep_prob
                dZ['dZ' + str(l - 1)] = np.array(dA['dA' + str(l - 1)], copy=True) # to calculate dZ_l-1.
                dZ['dZ' + str(l - 1)][Z['Z' + str(l - 1)] <= 0] = 0 # the gradiant of the linear activation at dZ_l-1.
    
    ## Updating the parameters:    
        for l in range(1, num_layers): # for every heddin layer in the model:
            P['W' + str(l)] -= alpha * dP['dW' + str(l)] # update Ws.
            P['b' + str(l)] -= alpha * dP['db' + str(l)] # update bs.
    
    end = datetime.now() # to measure training time (end).
    
    ## Predictions on test set:
    m_test = Y_test.shape[1] # number of test examples.
    A_test = dict() # activations dictionary.
    A_test['A0'] = X_test # initializing to calculate the linear forward pass.
    
    for l in range(1, num_layers): # for every hidden layer in the model, calculate:
            Z['Z' + str(l)] = np.dot(P['W' + str(l)], A_test['A' + str(l - 1)]) + P['b' + str(l)] # linear forward pass.
            if l < L: # if this is not the last layer:
                A_test['A' + str(l)] = np.maximum(0, Z['Z' + str(l)]) # calculate the activations as ReLU functions.
            else: # otherwise:
                A_test['A' + str(l)] = 1 / (1 + np.exp(-(Z['Z' + str(l)]))) # calculate as sigmoid functions.
                
    Yhat_test = A_test['A' + str(L)] # final output (Yhat_test)
    Yhat_test = np.array((Yhat_test > 0.5) * 1).reshape(1, m_test) # converting to 0s and 1s based on 0.5 threshold.
    
    train_acc = (100 - np.mean(np.abs(Yhat_train - Y)) * 100).round(4) # calculating the training accuracy.
    test_acc = (100 - np.mean(np.abs(Yhat_test - Y_test)) * 100).round(4) # calculating the testing accuracy.
    
    print('Train Accuracy: {}%'.format(train_acc)) # printing train accuracy.
    print('Test Accuracy: {}%'.format(test_acc)) # printing test accuracy.
    
    if show_plots: # if 'show_plots' argument is set to True, show the costs plots:
        plt.plot(np.squeeze(costs)) # ploting the costs over iterations.
        plt.ylabel('cost') # labeling the y axis.
        plt.xlabel('iterations') # labeling the x axis.
        plt.title('model struc.: ' + str(model_structure) + '.' + ' alpha = ' + str(alpha)) # title of the plot showing the learning rate and model structure.
        plt.show() # to show the plot.
    
    ## Model Summary
    model_summary = {'Model No.': str(datetime.now()), 'Model Structure': tuple(model_structure),
                     'Training Minutes': str(end - start),
                     'Number of Parameters': len(P), 'Train X Shape': np.shape(X), 'Train Y Sahpe': np.shape(Y),
                     'Test X Shape': np.shape(X_test), 'Test Y Sahpe': np.shape(Y_test),
                     'Iterations': iterations, 'alpha': alpha,
                     'P': P, 'Costs': costs, 'Train Accuracy': train_acc, 'Test Accuracy': test_acc, 'Dropout Masks': D,
                     'Regularization Lambd': lambd, 'Keep Prob.': keep_prob, 'Dropout Layers': tuple(sorted(dropout_layers))}
    return model_summary

# 14 ________________________________________________________________________________________________________________________________________________________________

def deep_nn_model_predict(sample_path, model):
    pics_array = prepare_image_data(sample_path)[0]
    set_x_flatten_stdr = prepare_image_arrays(pics_array)
    num_layers = len(model['Model Structure'])
    L = num_layers - 1
    P = model['P']
    Z = dict()
    A = dict()
    A['A0'] = set_x_flatten_stdr    
    for l in range(1, num_layers):
            Z['Z' + str(l)] = np.dot(P['W' + str(l)], A['A' + str(l - 1)]) + P['b' + str(l)]
            if l < L:
                A['A' + str(l)] = np.maximum(0, Z['Z' + str(l)])
            else:
                A['A' + str(l)] = 1 / (1 + np.exp(-(Z['Z' + str(l)])))
                
    Yhat = A['A' + str(L)]
    Yhat = np.array((Yhat > 0.5) * 1).reshape(1, len(pics_array))
    return Yhat

# 15 ________________________________________________________________________________________________________________________________________________________________


# 16 ________________________________________________________________________________________________________________________________________________________________


# 17 ________________________________________________________________________________________________________________________________________________________________


# 18 ________________________________________________________________________________________________________________________________________________________________


# 19 ________________________________________________________________________________________________________________________________________________________________


# 20 ________________________________________________________________________________________________________________________________________________________________


# 21 ________________________________________________________________________________________________________________________________________________________________


# 22 ________________________________________________________________________________________________________________________________________________________________


# 23 ________________________________________________________________________________________________________________________________________________________________


# 24 ________________________________________________________________________________________________________________________________________________________________


# 25 ________________________________________________________________________________________________________________________________________________________________


# 26 ________________________________________________________________________________________________________________________________________________________________


# 27 ________________________________________________________________________________________________________________________________________________________________