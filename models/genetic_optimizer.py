import random
import numpy as np
from datetime import datetime, timedelta

class GeneticOptimizer:
    def __init__(self, population_size=50, generations=30, mutation_rate=0.1):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        
    def optimize(self, trains, track_sections, conflicts):
        """Main optimization function using genetic algorithm"""
        
        # Initialize population
        population = self._initialize_population(trains, track_sections)
        
        best_solution = None
        best_fitness = float('-inf')
        
        for generation in range(self.generations):
            # Evaluate fitness for each solution
            fitness_scores = []
            for solution in population:
                fitness = self._evaluate_fitness(solution, trains, conflicts)
                fitness_scores.append(fitness)
                
                if fitness > best_fitness:
                    best_fitness = fitness
                    best_solution = solution.copy()
            
            # Selection and reproduction
            population = self._evolve_population(population, fitness_scores)
            
        return self._format_solution(best_solution, trains)
    
    def _initialize_population(self, trains, track_sections):
        """Initialize random population of scheduling solutions"""
        population = []
        
        for _ in range(self.population_size):
            solution = {}
            for train in trains:
                # Random scheduling decisions
                solution[train.id] = {
                    'departure_time': self._random_time_adjustment(),
                    'route_priority': random.randint(1, 10),
                    'platform_assignment': random.randint(1, 4),
                    'speed_adjustment': random.uniform(0.8, 1.2)
                }
            population.append(solution)
            
        return population
    
    def _evaluate_fitness(self, solution, trains, conflicts):
        """Evaluate fitness of a scheduling solution"""
        fitness = 0
        
        # Factors for fitness calculation
        delay_penalty = 0
        throughput_bonus = 0
        conflict_penalty = 0
        
        for train in trains:
            train_solution = solution.get(train.id, {})
            
            # Delay penalty
            delay_penalty += train.delay_minutes * train.priority
            
            # Throughput calculation
            speed_factor = train_solution.get('speed_adjustment', 1.0)
            throughput_bonus += speed_factor * train.priority
            
        # Conflict resolution bonus
        resolved_conflicts = len(conflicts) * 0.8  # Assume 80% resolution
        conflict_penalty = len(conflicts) - resolved_conflicts
        
        # Fitness function: maximize throughput, minimize delays and conflicts
        fitness = (throughput_bonus * 2) - (delay_penalty * 1.5) - (conflict_penalty * 3)
        
        return fitness
    
    def _evolve_population(self, population, fitness_scores):
        """Evolve population using selection, crossover, and mutation"""
        new_population = []
        
        # Keep best solutions (elitism)
        elite_count = int(self.population_size * 0.1)
        elite_indices = np.argsort(fitness_scores)[-elite_count:]
        
        for idx in elite_indices:
            new_population.append(population[idx].copy())
        
        # Generate rest through crossover and mutation
        while len(new_population) < self.population_size:
            # Tournament selection
            parent1 = self._tournament_selection(population, fitness_scores)
            parent2 = self._tournament_selection(population, fitness_scores)
            
            # Crossover
            child = self._crossover(parent1, parent2)
            
            # Mutation
            if random.random() < self.mutation_rate:
                child = self._mutate(child)
                
            new_population.append(child)
            
        return new_population
    
    def _tournament_selection(self, population, fitness_scores, tournament_size=3):
        """Tournament selection for parent selection"""
        tournament_indices = random.sample(range(len(population)), tournament_size)
        best_idx = max(tournament_indices, key=lambda i: fitness_scores[i])
        return population[best_idx]
    
    def _crossover(self, parent1, parent2):
        """Crossover between two parent solutions"""
        child = {}
        
        for train_id in parent1.keys():
            if random.random() < 0.5:
                child[train_id] = parent1[train_id].copy()
            else:
                child[train_id] = parent2[train_id].copy()
                
        return child
    
    def _mutate(self, solution):
        """Mutate a solution"""
        mutated = solution.copy()
        
        for train_id in mutated.keys():
            if random.random() < 0.3:  # 30% chance to mutate each train
                mutated[train_id]['departure_time'] = self._random_time_adjustment()
                mutated[train_id]['route_priority'] = random.randint(1, 10)
                mutated[train_id]['speed_adjustment'] = random.uniform(0.8, 1.2)
                
        return mutated
    
    def _random_time_adjustment(self):
        """Generate random time adjustment in minutes"""
        return random.randint(-15, 15)
    
    def _format_solution(self, solution, trains):
        """Format solution for API response"""
        formatted_solution = []
        
        for train in trains:
            if train.id in solution:
                train_solution = solution[train.id]
                formatted_solution.append({
                    'train_id': train.id,
                    'train_name': train.name,
                    'original_delay': train.delay_minutes,
                    'optimized_delay': max(0, train.delay_minutes + train_solution['departure_time']),
                    'priority': train_solution['route_priority'],
                    'platform': train_solution['platform_assignment'],
                    'speed_factor': train_solution['speed_adjustment'],
                    'recommendation': self._generate_recommendation(train_solution)
                })
                
        return formatted_solution
    
    def _generate_recommendation(self, solution):
        """Generate human-readable recommendation"""
        recommendations = []
        
        if solution['departure_time'] < 0:
            recommendations.append(f"Depart {abs(solution['departure_time'])} min early")
        elif solution['departure_time'] > 0:
            recommendations.append(f"Delay departure by {solution['departure_time']} min")
            
        if solution['speed_adjustment'] > 1.0:
            recommendations.append("Increase speed by {:.1%}".format(solution['speed_adjustment'] - 1))
        elif solution['speed_adjustment'] < 1.0:
            recommendations.append("Reduce speed by {:.1%}".format(1 - solution['speed_adjustment']))
            
        recommendations.append(f"Use platform {solution['platform_assignment']}")
        
        return "; ".join(recommendations)