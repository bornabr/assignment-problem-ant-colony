import numpy as np
import random

class Ant:
	def __init__(self, M, G, alpha, beta):
		self.M = M
		self.n = len(self.M)
		self.G = G
		self.alpha = alpha
		self.beta = beta
		
		self.path = []
		self.current_node = -1
		self.available_nodes = list(range(self.n))
		self.cost = None
		self.pheromone_delta = None
	
	def add_assignment(self, agent):
		if agent in self.path:
			raise "Already used agent"
		
		if self.current_node == self.n:
			raise "Path completed"
		
		self.path.append(agent)
		self.current_node += 1
		self.available_nodes.remove(agent)
	
	def choose_node(self):
		# Here we ignore dividing by the sum of all weights because we are using `random.choices`
		weights = []
		for node in self.available_nodes:
			weights.append((self.G[self.current_node][self.path[-1]]
			               [node] ** self.alpha) * (1/self.M[self.path[-1]][node] ** self.beta))
		return random.choices(self.available_nodes, weights)[0]
	
	def choose_best(self):
		best_node = None
		for node in self.available_nodes:
			if best_node == None or self.G[self.current_node][self.path[-1]][node] > self.G[self.current_node][self.path[-1]][best_node]:
				best_node = node
		return best_node 
	
	def calculate_cost(self):
		if self.cost is None:
			self.cost = 0
			for i, j in enumerate(self.path):
				self.cost += self.M[i][j]
			self.pheromone_delta = 1/self.cost

class AntColony:
	def __init__(self, n_ants, initial_pheromone, alpha, beta, evaporation_rate, e):
		self.initial_pheromone = initial_pheromone
		self.n_ants = n_ants
		self.alpha = alpha
		self.beta = beta
		self.evaporation_rate = evaporation_rate
		self.e = e

	def fit(self, M, n_iterations):
		self.M = M
		self.n = len(self.M)
		self.G = np.full((self.n - 1, self.n, self.n), self.initial_pheromone)
		best_ant = None
		for epoch in range(n_iterations):
			self.ants = []
			for ant_i in range(self.n_ants):
				ant = Ant(self.M, self.G, self.alpha, self.beta)
				self.ants.append(ant)
				ant.add_assignment(random.choice(ant.available_nodes))
				while len(ant.available_nodes) != 0:
					ant.add_assignment(ant.choose_node())

			self.evaluate_fitness()
			self.evaporate_pheromone()
			self.place_pheromone()
			best_ant = self.evaluate(epoch)
			self.place_additional_pheromone(best_ant)

		print(best_ant.cost, best_ant.path)

	def evaluate_fitness(self):
		self.pheromone_delta = 0
		for ant in self.ants:
			ant.calculate_cost()

	def evaporate_pheromone(self):
		self.G = self.G * (1-self.evaporation_rate)

	def place_pheromone(self):
		for ant in self.ants:
			for i in range(self.n - 1):
				self.G[i][ant.path[i]][ant.path[i+1]] += ant.pheromone_delta

	def evaluate(self, epoch):
		best_ant = None
		for i in range(self.n):
			ant = Ant(self.M, self.G, self.alpha, self.beta)
			ant.add_assignment(i)
			while len(ant.available_nodes) != 0:
				ant.add_assignment(ant.choose_best())
			ant.calculate_cost()
			if best_ant is None or best_ant.cost > ant.cost:
				best_ant = ant
		print(f'Epoch {epoch}:\t Best Ant Cost: {best_ant.cost}')
		return best_ant
		
	def place_additional_pheromone(self, best_ant):
		for i in range(self.n - 1):
			self.G[i][best_ant.path[i]][best_ant.path[i+1]] += self.e*best_ant.pheromone_delta

def load_test(filename):
	M = []
	f  = open(filename, "r")
	
	for line in f:
		M.append([int(x) for x in line.split()])
	
	return M

M = load_test("./Assignment Problem Test Cases/job1.assign")

colony = AntColony(n_ants=2, initial_pheromone=1, alpha=0.5, beta=1, evaporation_rate=0.02, e=1)

colony.fit(M, 10)
