import tensorflow as tf
import numpy as np

class NeuralNetwork():
    def __init__(self, num_inputs, num_layer1):

        self.num_outputs = 4

        self.W0 = tf.constant(np.random.randn(num_layer1, num_inputs), name = "W0")
        self.W1 = tf.constant(np.random.randn(self.num_outputs, num_layer1), name = "W1")

        self.b0 = tf.constant(np.random.randn(num_layer1, 1), name = "b0")
        self.b1 = tf.constant(np.random.randn(self.num_outputs, 1), name = "b1")

        #x = tf.constant(np.random.randn(num_inputs, 1), name = "x")

        #output = self.multilayer_perceptron(x, self.W0, self.b0, self.W1, self.b1)

        #print(float(output[0]))


    def denseR(self, x, W, b):
        #return tf.nn.sigmoid(tf.matmul(W, x) + b)
        return tf.nn.relu(tf.matmul(W, x) + b)

    def denseS(self, x, W, b):
        return tf.nn.sigmoid(tf.matmul(W, x) + b)

    @tf.function
    def multilayer_perceptron(self, x, w0, b0, w1, b1):
        a0 = self.denseR(x, w0, b0)
        output = self.denseS(a0, w1, b1)

        return output

    @tf.function
    def forward(self, x):
        print(x)
        x_const = tf.constant(x, name = "x")
        a0 = self.denseR(x_const, self.W0, self.b0)
        output = self.denseS(a0, self.W1, self.b1)

        return output