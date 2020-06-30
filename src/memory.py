from sklearn.utils import shuffle

class Memory():
    def __init__(self, max_size = 100):
        self.max_size = max_size

        # they all have the same size
        self.states = []
        self.actions = []
        self.rewards = []
    
    def push(self, state, action, reward):
        if len(self.states) >= self.max_size:
            print("full memory")
            return
        else:
            self.states.append(state)
            self.actions.append(action)
            self.rewards.append(reward)
    
    def get(self, item):
        if len(self.states) > item:
            return self.states[item], self.actions[item], self.rewards[item]

    def clear(self):
        self.states = []
        self.actions = []
        self.rewards = []

    def size(self):
        return len(self.states)

    def __str__(self):
        s =  "\n--------------------------------\n"
        for i in range(len(self.states)):
            s += "item: " + str(i) + "\t"
            s += "state: " + str(self.states[i]) + " "
            s += "action: " + str(self.actions[i]) + " "
            s += "reward: " + str(self.rewards[i]) + " "
            s += "\n"
        s += "--------------------------------\n"

        return s

    def randomize(self):
        self.states, self.actions, self.rewards = shuffle(self.states, self.actions, self.rewards, random_state=0)