import tensorflow as tf
import numpy as np

class NeuralNetwork():
    def __init__(self, n_inputs, n_hidden, n_output, weights = None):

        self.n_inputs = n_inputs
        self.n_hidden = n_hidden
        self.n_output = n_output

        if weights is None:
            self.W0 = tf.constant(np.random.randn(n_hidden, n_inputs), name = "W0")
            self.W1 = tf.constant(np.random.randn(self.n_output, n_hidden), name = "W1")

            self.b0 = tf.constant(np.random.randn(n_hidden, 1), name = "b0")
            self.b1 = tf.constant(np.random.randn(self.n_output, 1), name = "b1")
        else:
            self.setWeights(weights)

        x = tf.constant(np.random.randn(n_inputs, 1), name = "x")

    # dense relu
    def denseR(self, x, W, b):
        return tf.nn.relu(tf.matmul(W, x) + b)

    # dense sigmoid
    def denseS(self, x, W, b):
        return tf.nn.sigmoid(tf.matmul(W, x) + b)

    # array of W0, b0, W1, b1 concatenated
    def setWeights(self, weights):
        assert(0)

    @tf.function
    def forward(self, x):
        x = np.matrix(x).T.astype(float)
        x_const = tf.constant(x, name = "x")
        a0 = self.denseR(x_const, self.W0, self.b0)
        output = self.denseS(a0, self.W1, self.b1)

        return output