import tensorflow as tf
from tensorflow.contrib import layers
from tensorflow.contrib import losses
from tensorflow.contrib import learn
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
from sklearn import metrics

tf.logging.set_verbosity(tf.logging.INFO)

# read digit images of 28 x 28 = 784 pixels size
# target is image value in [0,9] range; one-hot encoded to 10 columns
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
X_train = mnist.train.images
y_train = mnist.train.labels

X_validation = mnist.validation.images
y_validation = mnist.validation.labels

X_test = mnist.test.images
y_test = mnist.test.labels

# Hidden layers generally use sigmoid perceptrons
# Output layer uses softmax for overall interpretability of all the 10 outputs
def model_function(features, targets, mode):
    # 1st hidden layer
    hlayer = layers.fully_connected(inputs = features,
                                    num_outputs= 50,
                                    activation_fn=tf.sigmoid) # Sigmoid perceptrons
    
    # Shallow neural network because there is only 1 hidden layer
    outputs = layers.fully_connected(inputs= hlayer,
                                     num_outputs=10,        # 10 perceptrons in output layer for 10 numbers (0 to 9)
                                     activation_fn=None)     # Use "None" as activation function specified in "softmax_cross_entropy" loss
    
    # Calculate loss using cross-entropy error; also use the 'softmax' activation function
    loss = losses.softmax_cross_entropy(outputs, targets)
    
    optimizer = layers.optimize_loss(loss= loss,
                                         global_step=tf.contrib.framework.get_global_step(),
                                         learning_rate=0.001,
                                         optimizer="SGD")
    
    # Class of output (i.e., predicted number) corresponds to the perceptron returning the highest fractional value
    # Returning both fractional values and corresponding labels    
    probs=tf.nn.softmax(outputs)
    return {'Probs':probs, 'labels':tf.argmax(probs, 1)},loss, optimizer
    # Applying softmax on top of plain outputs from layer (linear activation function since activation_fn=None) to give results

classifier = learn.Estimator(model_fn=model_function, model_dir="//home//tensorflow//Models//Shallow-NN-Model//Model1")    
classifier.fit(x=X_train, y=y_train, steps=1000,batch_size=1)

for var in classifier.get_variable_names():
    print var, ": ", classifier.get_variable_value(var).shape, " - ", classifier.get_variable_value(var)

#evaluate the model using validation set
results = classifier.evaluate(x=X_validation, y=y_validation, steps=1)
type(results)
for key in sorted(results):
    print "%s:%s" %(key, results[key])
    
# Predict the outcome of test data using model
predictions = classifier.predict(X_test)
metrics.accuracy_score(np.argmax(y_test,1), predictions['labels'])

# Predictions in tabular form
a = np.bincount(predictions['labels'])
b = np.nonzero(a)[0]
zip(b,a[b])
np.vstack((b,a[b])).T    
    
    
 