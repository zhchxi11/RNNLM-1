'''
Created on Aug 21, 2014

@author: sumanravuri
'''
import sys
import numpy as np
import scipy.io as sp
import copy

class LSTM_NNLM_Weight_with_embedding(object):
    def __init__(self, weights=None, bias=None):
        """num_layers
        weights - actual LSTM weights, a dictionary with keys corresponding to layer, ie. weights['visible_hidden'], weights['hidden_hidden'], and weights['hidden_output'] each numpy array
        bias - NN biases, again a dictionary stored as bias['visible'], bias['hidden'], bias['output'], etc.
        weight_type - optional command indexed by same keys weights, possible optionals are 'rbm_gaussian_bernoullli', 'rbm_bernoulli_bernoulli'"""
#        self.valid_layer_types = dict()
#        self.valid_layer_types['visible_hidden'] = ['rbm_gaussian_bernoulli', 'rbm_bernoulli_bernoulli']
#        self.valid_layer_types['hidden_hidden'] = ['rbm_bernoulli_bernoulli']
#        self.valid_layer_types['hidden_output'] = ['logistic']
        self.bias_keys = ['inputgate', 'forgetgate', 'outputgate', 'cell', 'output', 'embedding']
        self.weights_keys = ['visible_inputgate', 'visible_forgetgate', 'visible_outputgate', 'visible_cell',
                             'hidden_inputgate', 'hidden_forgetgate', 'hidden_outputgate', 'hidden_cell',
                             'prevcell_inputgate', 'prevcell_forgetgate', 'curcell_outputgate',
                             'hidden_output', 'embedding']
        
#        if init_hiddens != None:
#            self.init_hiddens = init_hiddens
        if weights == None:
            self.weights = dict()
        else:
            self.weights = copy.deepcopy(weights)
        if bias == None:
            self.bias = dict()
        else:
            self.bias = copy.deepcopy(bias)
#        if weight_type == None:
#            self.weight_type = dict()
#        else:
#            self.weight_type = copy.deepcopy(weight_type)
            
    def clear(self):
        self.num_layers = 0
        self.weights.clear()
        self.bias.clear()
#        self.weight_type.clear()
        #TO DO: do init hiddens need to be removed
        
#    def dot(self, nn_weight2, excluded_keys = {'bias': [], 'weights': []}):
#        if type(nn_weight2) is not LSTM_NNLM_Weight_with_embedding:
#            print "argument must be of type LSTM_NNLM_Weight_with_embedding... instead of type", type(nn_weight2), "Exiting now..."
#            sys.exit()
#        return_val = 0
#        for key in self.bias_keys:
#            if key in excluded_keys['bias']:
#                continue
#            return_val += np.sum(self.bias[key] * nn_weight2.bias[key])
#        for key in self.weights_keys:
#            if key in excluded_keys['weights']:
#                continue
#            return_val += np.sum(self.weights[key] * nn_weight2.weights[key])
#        return return_val
    
    def __str__(self):
        string = ""
        for key in self.bias_keys:
            string = string + "bias key " + key + "\n"
            string = string + str(self.bias[key]) + "\n"
        for key in self.weights_keys:
            string = string + "weight key " + key + "\n"
            string = string + str(self.weights[key]) + "\n"
        return string
    
    def print_statistics(self):
        for key in self.bias_keys:
            print "min of bias[" + key + "] is", np.min(self.bias[key]) 
            print "max of bias[" + key + "] is", np.max(self.bias[key])
            print "mean of bias[" + key + "] is", np.mean(self.bias[key])
            print "var of bias[" + key + "] is", np.var(self.bias[key]), "\n"
        for key in self.weights_keys:
            print "min of weights[" + key + "] is", np.min(self.weights[key]) 
            print "max of weights[" + key + "] is", np.max(self.weights[key])
            print "mean of weights[" + key + "] is", np.mean(self.weights[key])
            print "var of weights[" + key + "] is", np.var(self.weights[key]), "\n"
        
#        print "min of init_hiddens is", np.min(self.init_hiddens) 
#        print "max of init_hiddens is", np.max(self.init_hiddens)
#        print "mean of init_hiddens is", np.mean(self.init_hiddens)
#        print "var of init_hiddens is", np.var(self.init_hiddens), "\n"
        
    def norm(self, excluded_keys = {'bias': [], 'weights': []}):
        squared_sum = 0
        for key in self.bias_keys:
            if key in excluded_keys['bias']:
                continue
            squared_sum += np.sum(self.bias[key] ** 2)
        for key in self.weights_keys:
            if key in excluded_keys['weights']:
                continue  
            squared_sum += np.sum(self.weights[key] ** 2)
#        if calc_init_hiddens:
#            squared_sum += np.sum(self.init_hiddens ** 2)
        return np.sqrt(squared_sum)
    
    def max(self, excluded_keys = {'bias': [], 'weights': []}):
        max_val = -float('Inf')
        for key in self.bias_keys:
            if key in excluded_keys['bias']:
                continue
            max_val = max(np.max(self.bias[key]), max_val)
        for key in self.weights_keys:
            if key in excluded_keys['weights']:
                continue  
            max_val = max(np.max(self.weights[key]), max_val)
#        if calc_init_hiddens:
#            max_val = max(np.max(self.init_hiddens), max_val)
        return max_val
    
    def min(self, excluded_keys = {'bias': [], 'weights': []}):
        min_val = float('Inf')
        for key in self.bias_keys:
            if key in excluded_keys['bias']:
                continue
            min_val = min(np.min(self.bias[key]), min_val)
        for key in self.weights_keys:
            if key in excluded_keys['weights']:
                continue  
            min_val = min(np.min(self.weights[key]), min_val)
#        if calc_init_hiddens:
#            min_val = min(np.min(self.init_hiddens), min_val)
        return min_val
    
    def clip(self, clip_min, clip_max, excluded_keys = {'bias': [], 'weights': []}):
        nn_output = copy.deepcopy(self)
        for key in self.bias_keys:
            if key in excluded_keys['bias']:
                continue
            np.clip(self.bias[key], clip_min, clip_max, out=nn_output.bias[key])
        for key in self.weights_keys:
            if key in excluded_keys['weights']:
                continue  
            np.clip(self.weights[key], clip_min, clip_max, out=nn_output.weights[key])
#        if calc_init_hiddens:
#            np.clip(self.init_hiddens, clip_min, clip_max, out=nn_output.init_hiddens)
        return nn_output
    
    def get_architecture(self):
        return [self.weights['embedding'].shape[0], self.bias['embedding'].size, self.bias['cell'].size, self.bias['output'].size]
    
    def size(self, excluded_keys = {'bias': [], 'weights': []}):
        numel = 0
        for key in self.bias_keys:
            if key in excluded_keys['bias']:
                continue
            numel += self.bias[key].size
        for key in self.weights_keys:
            if key in excluded_keys['weights']:
                continue  
            numel += self.weights[key].size
#        if include_init_hiddens:
#            numel += self.init_hiddens.size
        return numel
    
    def open_weights(self, weight_matrix_name): #completed
        """the weight file format is very specific, it contains the following variables:
        weights_visible_hidden, weights_hidden_hidden, weights_hidden_output,
        bias_visible, bias_hidden, bias_output,
        init_hiddens, 
        weights_visible_hidden_type, weights_hidden_hidden_type, weights_hidden_output_type, etc...
        everything else will be ignored"""
        try:
            weight_dict = sp.loadmat(weight_matrix_name)
        except IOError:
            print "Unable to open", weight_matrix_name, "exiting now"
            sys.exit()
        
        for bias_name in self.bias_keys:
            try:
                self.bias[bias_name] = weight_dict['bias_' + bias_name]
            except KeyError:
                print "ERROR: %s not found. %s must exist for %s to be a valid weight file..." % (bias_name, bias_name, weight_matrix_name)
                raise KeyError
        for weight_name in self.weights_keys:
            try:
                self.weights[weight_name] = weight_dict['weights_' + weight_name]
            except KeyError:
                print "ERROR: %s not found. %s must exist for %s to be a valid weight file..." % (weight_name, weight_name, weight_matrix_name)
                raise KeyError
        
        del weight_dict
        self.check_weights()
        
    def init_random_weights(self, architecture, seed=0): #completed, expensive, should be compiled
        np.random.seed(seed)
#        initial_bias_range = initial_bias_max - initial_bias_min
#        initial_weight_range = initial_weight_max - initial_weight_min
#        self.bias['visible'] = initial_bias_min + initial_bias_range * np.random.random_sample((1,architecture[0]))
#        self.bias['hidden'] = initial_bias_min + initial_bias_range * np.random.random_sample((1,architecture[1]))
#        self.bias['output'] = initial_bias_min + initial_bias_range * np.random.random_sample((1,architecture[2]))
        self.bias['output'] = 0.2 * np.random.randn(1,architecture[3])
        self.bias['cell'] = 0.2 * np.random.randn(1,architecture[2])
        self.bias['embedding'] = 0.2 * np.random.randn(1,architecture[1])
        self.bias['forgetgate'] = 0.2 * np.random.randn(1,architecture[2]) - 0.5
        self.bias['inputgate'] = 0.2 * np.random.randn(1,architecture[2]) + 0.5
        self.bias['outputgate'] = 0.2 * np.random.randn(1,architecture[2]) + 0.5
        
        for weight_name in self.weights_keys:
            if weight_name.startswith('visible'):
                self.weights[weight_name] = 0.2 * np.random.randn(architecture[1],architecture[2])
            elif weight_name == 'hidden_output':
                self.weights[weight_name] = 0.2 * np.random.randn(architecture[2],architecture[3])
            elif weight_name == 'embedding':
                self.weights[weight_name] = 0.2 * np.random.randn(architecture[0],architecture[1])
            else:
                self.weights[weight_name] = 0.2 * np.random.randn(architecture[2],architecture[2])
        
#        print "architecture is", self.get_architecture()
#        self.init_hiddens = np.random.random_sample((1,architecture[1])) #because of sigmoid non-linearity
#        self.init_hiddens =  0.2 * np.random.randn(1,architecture[1])
#        self.weights['visible_hidden']=(initial_weight_min + initial_weight_range * 
#                                        np.random.random_sample( (architecture[0],architecture[1]) ))
#        self.weights['hidden_hidden']=(initial_weight_min + initial_weight_range * 
#                                       np.random.random_sample( (architecture[1],architecture[1]) ))
#        self.weights['hidden_output']=(initial_weight_min + initial_weight_range * 
#                                       np.random.random_sample( (architecture[1],architecture[2]) ))
        
#        self.weights['visible_hidden'] = 0.2 * np.random.randn( architecture[0],architecture[1]) 
#        self.weights['hidden_hidden'] = 0.2 * np.random.randn( architecture[1],architecture[1]) 
#        self.weights['hidden_output'] = 0.2 * np.random.randn( architecture[1],architecture[2])
#        if maxent:
#            self.weights['visible_output'] = 0.2 * np.random.randn( architecture[0],architecture[2])
#            if 'visible_output' not in self.weights_keys:
#                self.weights_keys += ['visible_output']
        
#        self.weight_type['visible_hidden'] = 'rbm_gaussian_bernoulli'
#        self.weight_type['hidden_hidden'] = 'rbm_bernoulli_bernoulli'
#        self.weight_type['hidden_output'] = 'logistic'
        
        print "Finished Initializing Weights"
        self.check_weights()
        
    def init_zero_weights(self, architecture, verbose=False, maxent=False):
        self.bias['output'] = np.zeros((1,architecture[3]))
        self.bias['cell'] = np.zeros((1,architecture[2]))
        self.bias['embedding'] = np.zeros((1,architecture[1]))
        self.bias['forgetgate'] = np.zeros((1,architecture[2]))
        self.bias['inputgate'] = np.zeros((1,architecture[2]))
        self.bias['outputgate'] = np.zeros((1,architecture[2]))
        
        for weight_name in self.weights_keys:
            if weight_name.startswith('visible'):
                self.weights[weight_name] = np.zeros((architecture[1],architecture[2]))
            elif weight_name == 'hidden_output':
                self.weights[weight_name] = np.zeros((architecture[2],architecture[3]))
            elif weight_name == 'embedding':
                self.weights[weight_name] = np.zeros((architecture[0],architecture[1]))
            else:
                self.weights[weight_name] = np.zeros((architecture[2],architecture[2]))
        
#        print self.get_architecture()
#        self.weight_type['visible_hidden'] = 'rbm_gaussian_bernoulli'
#        self.weight_type['hidden_hidden'] = 'rbm_bernoulli_bernoulli'
#        self.weight_type['hidden_output'] = 'logistic'
        if verbose:
            print "Finished Initializing Weights"
        self.check_weights(False)
        
    def check_weights(self, verbose=True): #need to check consistency of features with weights
        """checks weights to see if following conditions are true
        *feature dimension equal to number of rows of first layer (if weights are stored in n_rows x n_cols)
        *n_cols of (n-1)th layer == n_rows of nth layer
        if only one layer, that weight layer type is logistic, gaussian_bernoulli or bernoulli_bernoulli
        check is biases match weight values
        if multiple layers, 0 to (n-1)th layer is gaussian bernoulli RBM or bernoulli bernoulli RBM and last layer is logistic regression
        """
        if verbose:
            print "Checking weights...",
            
        if verbose:
            print "weight check not yet implemented... assuming it is correct"
        return
        
        #check weight types
#        if self.weight_type['visible_hidden'] not in self.valid_layer_types['visible_hidden']:
#            print self.weight_type['visible_hidden'], "is not valid layer type. Must be one of the following:", self.valid_layer_types['visible_hidden'], "...Exiting now"
#            sys.exit()
#        if self.weight_type['hidden_hidden'] not in self.valid_layer_types['hidden_hidden']:
#            print self.weight_type['hidden_hidden'], "is not valid layer type. Must be one of the following:", self.valid_layer_types['hidden_hidden'], "...Exiting now"
#            sys.exit()
#        if self.weight_type['hidden_output'] not in self.valid_layer_types['hidden_output']:
#            print self.weight_type['hidden_output'], "is not valid layer type. Must be one of the following:", self.valid_layer_types['hidden_output'], "...Exiting now"
#            sys.exit()
        
        #check biases
#        if self.bias['visible'].shape[1] != self.weights['visible_hidden'].shape[0]:
#            print "Number of visible bias dimensions: ", self.bias['visible'].shape[1],
#            print " of layer visible does not equal visible weight dimensions ", self.weights['visible_hidden'].shape[0], "... Exiting now"
#            sys.exit()
#            
#        if self.bias['output'].shape[1] != self.weights['hidden_output'].shape[1]:
#            print "Number of visible bias dimensions: ", self.bias['visible'].shape[1],
#            print " of layer visible does not equal output weight dimensions ", self.weights['hidden_output'].shape[1], "... Exiting now"
#            sys.exit()
#        
#        if self.bias['hidden'].shape[1] != self.weights['visible_hidden'].shape[1]:
#            print "Number of hidden bias dimensions: ", self.bias['hidden'].shape[1],
#            print " of layer 0 does not equal hidden weight dimensions ", self.weights['visible_hidden'].shape[1], " of visible_hidden layer ... Exiting now"
#            sys.exit()
#        if self.bias['hidden'].shape[1] != self.weights['hidden_output'].shape[0]:
#            print "Number of hidden bias dimensions: ", self.bias['hidden'].shape[1],
#            print " of layer 0 does not equal hidden weight dimensions ", self.weights['hidden_output'].shape[0], "of hidden_output layer... Exiting now"
#            sys.exit()
#        if self.bias['hidden'].shape[1] != self.weights['hidden_hidden'].shape[0]:
#            print "Number of hidden bias dimensions: ", self.bias['hidden'].shape[1],
#            print " of layer 0 does not equal input weight dimensions ", self.weights['hidden_hidden'].shape[0], " of hidden_hidden layer... Exiting now"
#            sys.exit()
#        if self.bias['hidden'].shape[1] != self.weights['hidden_hidden'].shape[1]:
#            print "Number of hidden bias dimensions: ", self.bias['hidden'].shape[1],
#            print " of layer 0 does not equal output weight dimensions ", self.weights['hidden_hidden'].shape[1], " hidden_hidden layer... Exiting now"
#            sys.exit()
#        if self.bias['hidden'].shape[1] != self.init_hiddens.shape[1]:
#            print "dimensionality of hidden bias", self.bias['hidden'].shape[1], "and the initial hiddens", self.init_hiddens.shape[1], "do not match. Exiting now."
#            sys.exit()
#            
#        #check weights
#        if self.weights['visible_hidden'].shape[1] != self.weights['hidden_hidden'].shape[0]:
#            print "Dimensionality of visible_hidden", self.weights['visible_hidden'].shape, "does not match dimensionality of hidden_hidden", "\b:",self.weights['hidden_hidden'].shape
#            print "The second dimension of visible_hidden must equal the first dimension of hidden_hidden layer"
#            sys.exit()
#        
#        if self.weights['hidden_hidden'].shape[1] != self.weights['hidden_hidden'].shape[0]:
#            print "Dimensionality of hidden_hidden", self.weights['hidden_hidden'].shape, "is not square, which it must be. Exiting now..."
#            sys.exit()
#        
#        if self.weights['hidden_hidden'].shape[1] != self.weights['hidden_output'].shape[0]:
#            print "Dimensionality of hidden_hidden", self.weights['hidden_hidden'].shape, "does not match dimensionality of hidden_output", "\b:",self.weights['hidden_output'].shape
#            print "The second dimension of hidden_hidden must equal the first dimension of hidden_output layer"
#            sys.exit()
#        if self.weights['hidden_hidden'].shape[1] != self.init_hiddens.shape[1]:
#            print "dimensionality of hidden_hidden weights", self.weights['hidden_hidden'].shape[1], "and the initial hiddens", self.init_hiddens.shape[1], "do not match. Exiting now."
#            sys.exit() 
#        
#        if verbose:
#            print "seems copacetic"
            
    def write_weights(self, output_name): #completed
        weight_dict = dict()
        for bias_name in self.bias_keys:
            weight_dict['bias_' + bias_name] = self.bias[bias_name]
        for weight_name in self.weights_keys:
            weight_dict['weights_' + weight_name] = self.weights[weight_name] 
        try:
            sp.savemat(output_name, weight_dict, oned_as='column')
        except IOError:
            print "Unable to save ", self.output_name, "... Exiting now"
            sys.exit()
        else:
            print output_name, "successfully saved"
            del weight_dict

    def assign_weights(self,other):
        if self.get_architecture() != other.get_architecture():
            raise ValueError("Neural net models do not match... Exiting now")
        
        for key in self.bias_keys:
            self.bias[key][:] = other.bias[key][:]
        for key in self.weights_keys:
            self.weights[key][:] = other.weights[key][:]
#        self.init_hiddens[:] = other.init_hiddens[:]

    def __neg__(self):
        nn_output = copy.deepcopy(self)
        for key in self.bias_keys:
            nn_output.bias[key] = -self.bias[key]
        for key in self.weights_keys:
            nn_output.weights[key] = -self.weights[key]
#        nn_output.init_hiddens = -self.init_hiddens
        return nn_output
    
    def __add__(self,addend):
        nn_output = copy.deepcopy(self)
        if type(addend) is LSTM_NNLM_Weight_with_embedding:
            if self.get_architecture() != addend.get_architecture():
                print "Neural net models do not match... Exiting now"
                sys.exit()
            
            for key in self.bias_keys:
                nn_output.bias[key] = self.bias[key] + addend.bias[key]
            for key in self.weights_keys:
                nn_output.weights[key] = self.weights[key] + addend.weights[key]
#            nn_output.init_hiddens = self.init_hiddens + addend.init_hiddens
            return nn_output
        #otherwise type is scalar
        addend = float(addend)
        for key in self.bias_keys:
            nn_output.bias[key] = self.bias[key] + addend
        for key in self.weights_keys:
            nn_output.weights[key] = self.weights[key] + addend
#        nn_output.init_hiddens = self.init_hiddens + addend
        return nn_output
        
    def __sub__(self,subtrahend):
        nn_output = copy.deepcopy(self)
        if type(subtrahend) is LSTM_NNLM_Weight_with_embedding:
            if self.get_architecture() != subtrahend.get_architecture():
                print "Neural net models do not match... Exiting now"
                sys.exit()
            
            for key in self.bias_keys:
                nn_output.bias[key] = self.bias[key] - subtrahend.bias[key]
            for key in self.weights_keys:
                nn_output.weights[key] = self.weights[key] - subtrahend.weights[key]
#            nn_output.init_hiddens = self.init_hiddens - subtrahend.init_hiddens
            return nn_output
        #otherwise type is scalar
        subtrahend = float(subtrahend)
        for key in self.bias_keys:
            nn_output.bias[key] = self.bias[key] - subtrahend
        for key in self.weights_keys:
            nn_output.weights[key] = self.weights[key] - subtrahend
        nn_output.init_hiddens = self.init_hiddens - subtrahend
        return nn_output
    
    def __mul__(self, multiplier):
        #if type(scalar) is not float and type(scalar) is not int:
        #    print "__mul__ must be by a float or int. Instead it is type", type(scalar), "Exiting now"
        #    sys.exit()
        nn_output = copy.deepcopy(self)
        if type(multiplier) is LSTM_NNLM_Weight_with_embedding:
            for key in self.bias_keys:
                nn_output.bias[key] = self.bias[key] * multiplier.bias[key]
            for key in self.weights_keys:
                nn_output.weights[key] = self.weights[key] * multiplier.weights[key]
#            nn_output.init_hiddens = self.init_hiddens * multiplier.init_hiddens
            return nn_output
        #otherwise scalar type
        multiplier = float(multiplier)
        
        for key in self.bias_keys:
            nn_output.bias[key] = self.bias[key] * multiplier
        for key in self.weights_keys:
            nn_output.weights[key] = self.weights[key] * multiplier
#        nn_output.init_hiddens = self.init_hiddens * multiplier
        return nn_output
    
    def __div__(self, divisor):
        #if type(scalar) is not float and type(scalar) is not int:
        #    print "Divide must be by a float or int. Instead it is type", type(scalar), "Exiting now"
        #    sys.exit()
        nn_output = copy.deepcopy(self)
        if type(divisor) is LSTM_NNLM_Weight_with_embedding:
            for key in self.bias_keys:
                nn_output.bias[key] = self.bias[key] / divisor.bias[key]
            for key in self.weights_keys:
                nn_output.weights[key] = self.weights[key] / divisor.weights[key]
#            nn_output.init_hiddens = self.init_hiddens / divisor.init_hiddens
            return nn_output
        #otherwise scalar type
        divisor = float(divisor)
        
        for key in self.bias_keys:
            nn_output.bias[key] = self.bias[key] / divisor
        for key in self.weights_keys:
            nn_output.weights[key] = self.weights[key] / divisor
#        nn_output.init_hiddens = self.init_hiddens / divisor
        return nn_output
    
    def __pow__(self, scalar):
        if scalar == 2:
            return self * self
        scalar = float(scalar)
        nn_output = copy.deepcopy(self)
        for key in self.bias_keys:
            nn_output.bias[key] = self.bias[key] ** scalar
        for key in self.weights_keys:
            nn_output.weights[key] = self.weights[key] ** scalar
#        nn_output.init_hiddens = nn_output.init_hiddens ** scalar
        return nn_output

    def __iadd__(self, nn_weight2):
        if type(nn_weight2) is not LSTM_NNLM_Weight_with_embedding:
            print "argument must be of type LSTM_NNLM_Weight_with_embedding... instead of type", type(nn_weight2), "Exiting now..."
            sys.exit()
        if self.get_architecture() != nn_weight2.get_architecture():
            print "Neural net models do not match... Exiting now"
            raise ValueError

        for key in self.bias_keys:
            self.bias[key] += nn_weight2.bias[key]
        for key in self.weights_keys:
            self.weights[key] += nn_weight2.weights[key]
#        self.init_hiddens += nn_weight2.init_hiddens
        return self
    
    def __isub__(self, nn_weight2):
        if type(nn_weight2) is not LSTM_NNLM_Weight_with_embedding:
            print "argument must be of type LSTM_NNLM_Weight_with_embedding... instead of type", type(nn_weight2), "Exiting now..."
            sys.exit()
        if self.get_architecture() != nn_weight2.get_architecture():
            print "Neural net models do not match... Exiting now"
            sys.exit()

        for key in self.bias_keys:
            self.bias[key] -= nn_weight2.bias[key]
        for key in self.weights_keys:
            self.weights[key] -= nn_weight2.weights[key]
#        self.init_hiddens -= nn_weight2.init_hiddens
        return self
    
    def __imul__(self, scalar):
        #if type(scalar) is not float and type(scalar) is not int:
        #    print "__imul__ must be by a float or int. Instead it is type", type(scalar), "Exiting now"
        #    sys.exit()
        scalar = float(scalar)
        for key in self.bias_keys:
            self.bias[key] *= scalar
        for key in self.weights_keys:
            self.weights[key] *= scalar
#        self.init_hiddens *= scalar
        return self
    
    def __idiv__(self, other):
        if type(other) is LSTM_NNLM_Weight_with_embedding:
            for key in self.bias_keys:
                self.bias[key] /= other.bias[key]
            for key in self.weights_keys:
                self.weights[key] /= other.weights[key]
#            self.init_hiddens /= other.init_hiddens
            
        else:
            scalar = float(other)
            for key in self.bias_keys:
                self.bias[key] /= scalar
            for key in self.weights_keys:
                self.weights[key] /= scalar
#            self.init_hiddens /= scalar
        return self
    
    def __ipow__(self, scalar):
        scalar = float(scalar)
        for key in self.bias_keys:
            self.bias[key] **= scalar
        for key in self.weights_keys:
            self.weights[key] **= scalar
#        self.init_hiddens **= scalar
        return self
    
    def __copy__(self):
        return LSTM_NNLM_Weight_with_embedding(self.weights, self.bias)
    
    def __deepcopy__(self, memo):
        return LSTM_NNLM_Weight_with_embedding(copy.deepcopy(self.weights,memo), copy.deepcopy(self.bias,memo))