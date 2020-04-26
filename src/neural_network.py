import tensorflow as tf
import numpy as np

class NeuralNetwork():
    def __init__(self, car):
        self.car = car

        W0 = tf.constant(np.random.randn(3, 3), name = "W0")
        W1 = tf.constant(np.random.randn(3, 3), name = "W1")
        W2 = tf.constant(np.random.randn(4, 3), name = "W2")

        b0 = tf.constant(np.random.randn(3, 1), name = "b0")
        b1 = tf.constant(np.random.randn(3, 1), name = "b1")
        b2 = tf.constant(np.random.randn(4, 1), name = "b2")

        x = tf.constant(np.random.randn(3, 1), name = "x")

        output = self.multilayer_perceptron(x, W0, b0, W1, b1, W2, b2)

        print(output)


    def denseR(self, x, W, b):
        #return tf.nn.sigmoid(tf.matmul(W, x) + b)
        return tf.nn.relu(tf.matmul(W, x) + b)

    def denseS(self, x, W, b):
        return tf.nn.sigmoid(tf.matmul(W, x) + b)

    @tf.function
    def multilayer_perceptron(self, x, w0, b0, w1, b1, w2, b2):
        a0 = self.denseR(x, w0, b0)
        a1 = self.denseR(a0, w1, b1)
        output = self.denseS(a1, w2, b2)

        return output