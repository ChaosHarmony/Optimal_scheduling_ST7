class Ant():

    def __init__(self, starting_point, objectif_point):
        self.solution = [starting_point]
        self.objectif = objectif_point

    def is_visited(self, node):
        return node in self.solution

    def choose_node(self, node):
        self.solution.append(node)

    def has_finished(self):
        return self.objectif == self.solution[-1]
