import random
from settings import *

maze = matrika

maze_width = len(maze[0])
maze_height = len(maze)

def find_best_path(maze, start, end):
    population_size = 100
    mutation_rate = 0.01
    crossover_rate = 0.8

    def calculate_fitness(individual):
        path_cost = 0
        x, y = start
        for direction in individual:
            dx, dy = direction
            if maze[x + dx][y + dy] == 0:
                path_cost += 1
                x += dx
                y += dy
            else:
                return 0
        return path_cost

    def crossover(parent1, parent2):
        crossover_point = random.randint(1, len(parent1) - 2)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2

    def mutate(individual):
        if random.random() < mutation_rate:
            mutation_point = random.randint(0, len(individual) - 1)
            individual[mutation_point] = random.choice([(0, 1), (1, 0), (-1, 0), (0, -1)])
        return individual

    population = [[random.choice([(0, 1), (1, 0), (-1, 0), (0, -1)]) for _ in range(len(maze[0]))] for _ in range(population_size)]

    for generation in range(100): 
        population.sort(key=calculate_fitness, reverse=True)  
        top_10_percent = int(population_size * 0.1)
        next_generation = population[:top_10_percent] 

        for _ in range(population_size - top_10_percent):
            parent1 = random.choice(next_generation)
            parent2 = random.choice(next_generation)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)
            next_generation.append(child1)
            next_generation.append(child2)

        population = next_generation

    best_individual = max(population, key=calculate_fitness)
    return best_individual