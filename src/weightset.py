import numpy as np

class WeightSet():
    def __init__(self, n_input, n_hidden, n_output, weights = None):

        self.n_W0 = n_hidden * n_input
        self.n_b0 = n_hidden
        self.n_W1 = n_output * n_hidden
        self.n_b1 = n_output

        self.n_input = n_input
        self.n_hidden = n_hidden
        self.n_output = n_output

        self.size = self.n_W0 + self.n_b0 + self.n_W1 + self.n_b1

        # weights are storead as a np.array
        if weights is None:
            self.weights = np.zeros((self.size))
        else:
            assert(self.size == len(weights))
            self.weights = weights

    def getSize(self):
        return self.size

    """def getW0(self):
        return self.n_W0
    
    def getW1(self):
        return self.n_W1

    def getb0(self):
        return self.n_b0

    def getb1(self):
        return self.n_b1"""

    def getWeights(self):
        return self.weights

    def getNInput(self):
        return self.n_input

    def getNHidden(self):
        return self.n_hidden

    def getNOutput(self):
        return self.n_output
    
    def __str__(self):
        return str(self.weights)

    def mutate(self, prob = 0.2):
        # only those nodes whose rand > (1-prob) will be mutated 
        selected = np.random.rand((self.size))
        selected = np.greater((selected),(1-prob))

        # add mutation from [-0.5, +0.5)
        self.weights += (np.random.rand((self.size)) -0.5) * selected

    @classmethod
    def mix(cls, ws1, ws2):

        # make sure we are using the same lengths
        assert(ws1.n_input == ws2.n_input)
        assert(ws1.n_hidden == ws2.n_hidden)
        assert(ws1.n_output == ws2.n_output)

        selected = np.random.rand((ws1.size))
        selected = np.greater((selected),(0.5))

        not_selected = np.logical_not(selected)

        weights = selected * ws1.weights + not_selected * ws2.weights
        return WeightSet(ws1.n_input, ws1.n_hidden, ws1.n_output, weights)

