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
            #self.weights = np.array([-0.4007046481483505, -0.4852496144463698, 0.13428035434878527, 1.3579594797045602, -0.7469166549988614, 1.1624532856425738, 0.2873566513064756, -0.6246350868630266, -0.46084097587489725, -0.00019920393280015158, -2.0586065921469854, 2.03599355533315, -2.562469796435539, 1.3019765413824325, -0.6851691977635034, -0.5445041243358397, -0.4070242847517127, -0.5874005609443698, -1.1400709717311177, 0.9200414236052564, 0.6399099586573925, 2.555566879661534, -2.040300527732088, 0.8092598960768151, 0.701039146921445, -0.5668781582673297, -1.593596057869624, 0.195966640641277, 1.1954533802865883, -0.44601113437740525, 0.08345375362395979, 1.4077664682934223, -1.4020055593585021, -0.11768329760399032, 2.396553054936149, 1.3264630437094882, -0.5441650196257561, -0.96111452047462, 1.4202573261911287, -1.5774260614679605, -0.6436626587443335, -0.9744031361375237, 1.2191717209978643, -0.36629396004729975, 0.8348631291382315, 0.8535730280543306, -3.3791839539145925, -1.0569547281915275, 0.3052528079057356, 1.0923252189446662, -2.2941989064824444, 3.0564688925975996, 0.6589162100177538, -0.00991355548670958, -1.6664067483781104, 3.4188920083301033, -2.2525546025114083, -1.3055092281134555, 0.24762760074571633, -0.8460394933666222, 0.6730384297165772, 1.6432868345046079, 0.948560820311448, -0.3754881493039971, 0.7478386077790204, 0.5898030845764448, 0.24485691975615897, 1.477776471634057, 0.6501458313139632, -1.9435543048730284, 1.3988255254678847, 0.913171724486696, 1.6039431090678393, -0.583123049636066, -3.62354872072339, -1.8188514117526884, -0.8487217297250584, 1.014557610256329, -0.7904073807739738, -3.144896259885882, -2.341159184689845, 1.0659233825540066, 1.322567020974651, -1.8414042282711875, -2.5366327546029668, 0.9127427156679921, 0.7574328553564739, 1.1962414391051754, -0.4330571335920428, 2.3009217432167697, -1.3198334995591736, -1.1608848502153344, 1.6851434886638983, -2.5677285729182837])
        else:
            assert(self.size == len(weights))
            self.weights = np.array(weights)

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
        print("mutate")
        # only those nodes whose rand > (1-prob) will be mutated 
        selected = np.random.rand((self.size))
        selected = np.greater((selected),(1-prob))

        self.weights *= np.logical_not(selected)

        # add mutation from [-0.5, +0.5)
        self.weights += np.random.randn(self.size) * selected

        #print((np.random.rand((self.size)) -0.5) * selected)

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

