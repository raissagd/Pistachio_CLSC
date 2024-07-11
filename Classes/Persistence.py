import pickle

class SaveSolution:
    def __init__(self) -> None:
        self.format = '.pkl'
    def save(self, solution=None, filename='', filepath=''):
        with open(filepath + filename + self.format, 'wb') as file:
            pickle.dump(solution, file)
    def load(self, filename='', filepath=''):
        with open(filepath + filename + self.format, 'rb') as file:
            solution = pickle.load(file)
        return solution