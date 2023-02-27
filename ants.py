import numpy as np


class Ant():

    def __init__(self, starting_point, objectif_point, alpha, beta):
        self.solution = [starting_point]
        self.objectif = objectif_point
        self.alpha = alpha
        self.beta = beta

    def is_visited(self, node):
        return node in self.solution

    def add_node(self, node):
        self.solution.append(node)

    def has_finished(self):
        return self.objectif == self.solution[-1]


class Ant_TGE(Ant):
    def __init__(self, starting_point, objectif_point, alpha, beta, nb_machines):
        super().__init__(starting_point, objectif_point, alpha, beta)
        self.nb_machines = nb_machines
        self.machines_time_track = np.zeros((1, nb_machines), dtype=float)
        self.affected_machine = []

    def machine_available(self):
        return self.machines_time_track == 0.

    def update_all_time_track(self, duration: float):
        self.machines_time_track = self.machines_time_track - duration
        self.machines_time_track = np.where(self.machines_time_track <= 0, np.zeros_like(
            self.machines_time_track), self.machines_time_track)

    def update_machine_time_track(self, machine, duration):
        self.machines_time_track[machine] = duration

    def choose_machine(self):
        possible_machines = []
        for i in range(self.nb_machines):
            if self.machine_available():
                possible_machines.append(i)
        return np.random.choice(possible_machines)

    def add_machine(self, machine):
        self.affected_machine.append(machine)
