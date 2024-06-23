import random
from settings import *

maze = matrika

maze_width = len(maze[0])
maze_height = len(maze)

def ga_pathfinding(maze, start, end):
    population_size = 100
    mutation_rate = 0.01
    crossover_rate = 0.8
    directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

    def calculate_fitness(individual):
        x, y = start
        for direction in individual:
            dx, dy = direction
            if maze[x + dx][y + dy] == 0:
                return False
            x += dx
            y += dy
        return True

    def crossover(parent1, parent2):
        crossover_point = random.randint(1, len(parent1) - 2)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        return child

    def mutate(individual):
        if random.random() < mutation_rate:
            mutation_point = random.randint(0, len(individual) - 1)
            individual[mutation_point] = random.choice(directions)
        return individual

    population = [random.choices(directions, k=maze_width) for _ in range(population_size)]

    for generation in range(100): 
        population.sort(key=calculate_fitness, reverse=True)  
        top_10_percent = int(population_size * 0.1)
        next_generation = population[:top_10_percent] 

        while len(next_generation) < population_size:
            parent1 = random.choice(next_generation)
            parent2 = random.choice(next_generation)
            child = crossover(parent1, parent2)
            child = mutate(child)
            next_generation.append(child)

        population = next_generation

    best_individual = max(population, key=calculate_fitness)
    return best_individual