import tensorflow as tf
import numpy as np

#from weightset import WeightSet

class NeuralNetwork():
    # weight is of type WeightSet
    def __init__(self, n_inputs, n_hidden, n_output, weights = None):

        self.n_inputs = n_inputs
        self.n_hidden = n_hidden
        self.n_output = n_output

        if weights is None:
            self.W0 = tf.constant(np.random.randn(n_hidden, n_inputs), name = "W0")
            self.b0 = tf.constant(np.random.randn(n_hidden, 1), name = "b0")
                        
            self.W1 = tf.constant(np.random.randn(self.n_output, n_hidden), name = "W1")
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
        line = weights.getWeights()
        
        assert(self.n_inputs == weights.getNInput())
        assert(self.n_hidden == weights.getNHidden())
        assert(self.n_output == weights.getNOutput())

        W0_start = 0
        W0_end = self.n_hidden * self.n_inputs
        W0_tmp = line[W0_start : W0_end ].reshape(self.n_hidden, self.n_inputs)
        self.W0 = tf.constant(W0_tmp.reshape(self.n_hidden, self.n_inputs), name="W0")

        b0_start = W0_end
        b0_end = W0_end + self.n_hidden
        b0_tmp = line[b0_start : b0_end].reshape(self.n_hidden, 1)
        self.b0 = tf.constant(b0_tmp.reshape(self.n_hidden,1), name = "b0")

        W1_start = b0_end
        W1_end = b0_end + self.n_output*self.n_hidden
        W1_tmp = line[W1_start : W1_end].reshape(self.n_output, self.n_hidden)
        self.W1 = tf.constant(W1_tmp.reshape(self.n_output, self.n_hidden), name="W1")

        b1_start = W1_end
        b1_end = W1_end + self.n_output
        b1_tmp = line[b1_start : b1_end].reshape(self.n_output, 1)
        self.b1 = tf.constant(b1_tmp.reshape(self.n_output,1), name = "b1")

        """self.W0 = weights.getW0()
        self.b0 = weights.getb0()
        self.W1 = weigths.getW1()
        self.b1 = weights.getb1()"""


    """def __str__(self):
        return str(self.W0.flatten().tolist()) + str(self.b0.flatten().tolist()) + str(self.W1.flatten().tolist()) + str(self.b1.flatten().tolist())"""

    def print(self):
        print(self.W0.numpy().flatten().tolist())
        print(self.b0)

        print(self.W1)
        print(self.b1)

    def getArr(self):
        return np.concatenate((self.W0.numpy().flatten(), self.b0.numpy().flatten(), self.W1.numpy().flatten(), self.b1.numpy().flatten())).tolist()

    def getStructure(self):
        return (self.n_inputs, self.n_hidden, self.n_output)

    """def getWeightSet(self):
        return WeightSet(self.n_inputs, self.n_hidden, self.n_output)"""

    @tf.function
    def forward(self, x):
        x = np.matrix(x).T.astype(float)
        x_const = tf.constant(x, name = "x")
        a0 = self.denseR(x_const, self.W0, self.b0)
        output = self.denseS(a0, self.W1, self.b1)

        return output