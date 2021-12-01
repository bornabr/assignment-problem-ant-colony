# Ant Colony Algorithm for the Assignment Problem
## Introduction
The assignment problem is a fundamental combinatorial optimization problem. In its most general form, the problem is as follows:

The problem instance has n agents and n tasks. Any agent can be assigned to perform any task, incurring some costs that may vary depending on the agent-task assignment. It is required to perform as many tasks as possible by assigning at most one agent to each task and at most one task to each agent so that the total cost of the assignment is minimized.

## The Ant Colony Algorithm
Here we explain the implementation of an Ant Colony Algorithm for solving the Assignment Problem.
### Environment
Our input is an n×n matrix `M`, which gives us information about the cost of assigning each agent to each task.

Regarding our ant colony, the graph that ants move on in this problem is actually not a real graph but many task-agent pairs that are stored in an n×n matrix called `G`. Ants in our implementation choose these pairs one by one, and we could say by choosing them, they make a permutation which is called a `path` in my code. You could also imagine that these ants move on a bipartite-directed graph. The first part is for tasks, and the second is for agents, and by going from one node in the first part to the node, the second one, we assign a task to an agent.

#### Reasons for this implementation:
- Simplicity of implementation
- Reducing processing (time complexity)
- Less need for memory

I should mention that in my first implementation, I chose a multipartite-directed graph in which each part represented a task, and selecting a node in each meant that an assignment was done. The ants went from first to the last and created the permutation, which was the solution to the problem. In that implementation, the matrix `G` was an (n-1)×n×n matrix. The reason for changing my solution was simply because that implementation did not reach good answers and was a little slow.

### Loop
The whole process is done through a loop which is indicated by `n_iterations`. In each iteration, we create ants, and they will go through the matrix `G` and choose their pairs based on a decision algorithm implemented in the `choose_node` method. Note that these ants keep in mind which agent is assigned, and they avoid multiple assignments. After every ant has found a permutation for itself, we calculate the fitness of each ant's path, which is the sum of costs of agent-task pairs. After this, we evaporate pheromone from matrix `G`. We place a new pheromone on `G` based on evaluated costs in this step also, we add additional pheromone for the best possible path in each generation. Finally, we evaluate the best answer by running one ant, which only chooses the best nodes based on pheromone and prints the iteration result.

### Node Choosing
In the function `chooses_node`, we decide that ant should choose which agent for a specific task based on pheromones available in `G`. The algorithm is provided here:

```python
	def choose_node(self):
		weights = []
		for node in self.available_nodes:
			weights.append((self.G[self.current_node][node] ** self.alpha)
			               * (1/self.M[self.current_node][node] ** self.beta))
		return random.choices(self.available_nodes, weights)[0]
```
`alpha` and `beta` are our hyperparameters that control the effect of pheromones and our heuristic function, which is the cost of choosing that specific agent for that task.

### Pheromone Evaporation
For the sake of exploring, we remove some of the previous pheromones to let ants cover new places in the next iterations.
```python
	def evaporate_pheromone(self):
		self.G = self.G * (1-self.evaporation_rate)
```

### Pheromone Placement
For this matter, we add `1/ant.cost` to each place that each ant has been as the new pheromone.
```python
	def place_pheromone(self):
		for ant in self.ants:
			for i in range(self.n):
				self.G[i][ant.path[i]] += ant.pheromone_delta
```
Also, some additional pheromone is added just for the best solution in each iteration.
```python
	def place_additional_pheromone(self, best_ant):
		for i in range(self.n):
			self.G[i][best_ant.path[i]] += self.e*best_ant.pheromone_delta
```
`e` here controls the impact of this additional pheromone.

## Test
My answers for the second test case reached 500 very soon with different hyperparameters. Still, for reaching under 350, I had to run it for a significantly higher number of iterations and test different hyperparameters. I understood for this problem that a very low evaporation rate and a high beta could be beneficial. Here is my answer:

```90, 11, 10, 74, 28, 44, 60, 56, 22, 43, 21, 30, 87, 97, 12, 84, 0, 23, 35, 26, 19, 72, 31, 24, 5, 9, 67, 91, 92, 46, 64, 77, 17, 98, 7, 85, 42, 29, 13, 71, 79, 18, 86, 48, 78, 3, 27, 99, 95, 25, 82, 20, 88, 54, 58, 89, 41, 37, 38, 52, 53, 14, 50, 81, 93, 65, 39, 62, 55, 59, 63, 94, 70, 96, 76, 4, 69, 2, 33, 68, 51, 80, 16, 36, 83, 8, 47, 49, 66, 73, 32, 6, 61, 1, 57, 45, 34, 40, 15, 75```

This answer cost was 348 and was produced in 8000 iterations and with the following parameters:

```n_ants=10, initial_pheromone=1, alpha=1, beta=10, evaporation_rate=1/50, e=0```

For the third test case, reaching below 1000 was really hard, and I had to tweak the parameters many times and run the program for a high number of iterations. Here is my answer:

```8, 27, 93, 78, 14, 104, 122, 15, 56, 40, 110, 128, 172, 195, 115, 66, 83, 11, 169, 120, 121, 45, 140, 106, 41, 69, 125, 162, 150, 87, 147, 16, 175, 23, 179, 72, 30, 142, 146, 170, 159, 32, 183, 196, 34, 58, 18, 160, 92, 68, 194, 157, 112, 103, 33, 39, 13, 187, 166, 197, 109, 95, 116, 52, 62, 165, 152, 55, 114, 44, 188, 73, 64, 48, 20, 82, 86, 81, 88, 4, 138, 46, 108, 26, 50, 190, 85, 28, 65, 107, 97, 198, 154, 181, 173, 53, 101, 178, 80, 189, 22, 25, 61, 35, 37, 148, 182, 63, 141, 176, 31, 113, 84, 24, 38, 0, 171, 133, 156, 21, 47, 94, 57, 192, 126, 51, 135, 5, 132, 174, 71, 143, 149, 2, 117, 151, 123, 99, 144, 145, 17, 7, 186, 180, 191, 184, 98, 10, 60, 136, 36, 89, 19, 111, 168, 77, 119, 163, 118, 199, 1, 129, 134, 158, 43, 177, 124, 79, 54, 49, 155, 67, 42, 105, 96, 70, 6, 131, 91, 102, 139, 193, 76, 167, 185, 161, 137, 100, 164, 127, 74, 75, 59, 90, 9, 3, 12, 153, 130, 29```

This answer cost was 832 and was produced in 10000 iterations and with the following parameters:

```n_ants=10, initial_pheromone=1, alpha=0.4, beta=0.5, evaporation_rate=1/70, e=0.01```