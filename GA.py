from ast import Sub
from turtle import done
import gym
import numpy as np
import pandas as pd
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import cv2
from RNG import RandomNumberGenerator as rng
from Subject import Subject
from Mapper import Mapper


class GeneticAlg:
    def __init__(self, seed:int=71) -> None:
        _ENV_NAME = 'CarRacing-v1'
        self.env = gym.make(_ENV_NAME)
        self.env.reset(seed=seed)
        self.rng = rng(seedVaule=seed)
        self._genotype_lenght = 6
        self.seed = seed

    def generate_random_parents(self, population_size):
        parents = [] 
        for _ in range(population_size):
            gen = [
                self.rng.nextFloat(0, 2.5), # 0.4
                self.rng.nextFloat(0, 2.5), # 0.7
                self.rng.nextFloat(10, 150), # 50
                self.rng.nextFloat(.25, 10),  # 1
                self.rng.nextFloat(.25, 10),  # 1
                self.rng.nextInt(5, 20)  # 10

                ]

            parents.append(Subject(gen))
        return parents

    def evaluate_subject(self, sbj: Subject, sbj_steps:int) -> int:
        self.env.reset(seed=self.seed)
        mp = Mapper()
        
        
        # pierwszy krok:
        first_steep_velocity = 0.1
        for _ in range(10):
            state, reward, _, _ = self.env.step([0,first_steep_velocity,0])
            sbj.shift_speed(first_steep_velocity)
            self.env.render()
        
        '''for _ in range(75):
            state, _, _, _ = self.env.step([0,first_steep_velocity,0])
            self.env.render()
            sbj.shift_speed(first_steep_velocity)
            print(sbj.speed)

        print('hamowanie')
        
        for _ in range(100):
            state, _, _, _ = self.env.step([0,0,first_steep_velocity])
            self.env.render()
            sbj.shift_speed(-2*first_steep_velocity)
            print(sbj.speed)'''
        

        # powtarzaj eksperyment przez zadaną ilość kroków:
        for i in range(sbj_steps):

            # Ocena fitness:
            if mp.distance_fitness(state[:,:,1]):
                sbj.fitness += 1
            
            self.env.render()

            # Mapowanie obserwacji (96x96) - > (1x5) - otrzymujemy tablicę dystansów
            state = mp.calculate_distances(state=state[:,:,1])
            # Na podstawie dystansów oblicza się następny krok:
            next_step = sbj.calculate_decision(state)
            # Wykonanie kroku
            state, _, _, _ = self.env.step(next_step)

            if mp.is_car_on_grass(state[:,:,1]):
                return 0

        return sbj.fitness

        
    def crossover(self, sbj1 : Subject, sbj2: Subject):

        a, b, c = self.rng.nextInt(0, self._genotype_lenght-1), self.rng.nextInt(0, self._genotype_lenght-1), self.rng.nextInt(0, self._genotype_lenght-1)

        while a == b or a == c or b == c:
            a, b, c = self.rng.nextInt(0, self._genotype_lenght-1), self.rng.nextInt(0, self._genotype_lenght-1), self.rng.nextInt(0, self._genotype_lenght-1)
        
        sbj1._genotype[a], sbj1._genotype[b], sbj1._genotype[c] = sbj2._genotype[a], sbj2._genotype[b], sbj2._genotype[c]

        return sbj1, sbj2

    def mutation(self, sbj: Subject):
        gen_index = self.rng.nextInt(0, self._genotype_lenght-1)

        sbj._genotype[gen_index] = sbj._genotype[gen_index]*self.rng.nextFloat(0.85, 1.15)

        return sbj


    def run(
        self,
        population_size:int = 10,
        generations:int = 5,
        crossover_prob:int = 85,
        mutation_prob:int = 5,
        subject_steps:int = 300
    ):
        # create begin (random) population, with given size
        population = self.generate_random_parents(population_size)
        

        # główna pętla alg.
        for generation in range(generations):

            # Czyszczenie fitness (po poprzedniej iteracji)
            for p in range(len(population)):
                population[p].fitness = 0

            mean_fitness = []
            
            # Ocena populacji:
            for sbj in range(len(population)):

                population[sbj].fitness = self.evaluate_subject(population[sbj], subject_steps)
                print(f'Subject: {sbj+1}/{len(population)}, generation: {generation+1}/{generations}, fitness: {population[sbj].fitness}')
                mean_fitness.append(population[sbj].fitness)

            mean_fitness_np = np.array(mean_fitness)
            print(f'Mean fitness: {np.mean(mean_fitness_np)}, after generation: {generation+1}/{generations}')

            # Selekcja:

            roulette = []

            for i in range(len(population)):
                for _ in range(population[i].fitness):
                    roulette.append(i)

            
            # Kręcenie ruletką:

            best_parents = []

            for _ in range(population_size):
                best_parents.append(population[roulette[self.rng.nextInt(low=0,high=len(roulette)-1)]])


            # Krzyżowanie:

            children = []

            for i in range(0,len(best_parents)-1,2):
                if self.rng.nextInt(0, 99) <= crossover_prob:
                    child_1, child_2 = self.crossover(best_parents[i], best_parents[i+1])
                    children.append(child_1)
                    children.append(child_2)
                else:
                    children.append(best_parents[i])
                    children.append(best_parents[i+1])


            # Mutacja:

            for i in range(len(children)):
                if self.rng.nextInt(0, 99) <= mutation_prob:
                    children[i] = self.mutation(children[i])


            population = children

        
        best_fitness = 0
        best_subject = None 
        
        for sbj in range(len(population)):
            if population[sbj].fitness > best_fitness:
                best_fitness = population[sbj].fitness
                best_subject = population[sbj]

        print(f'Best subject has: {best_fitness} fitness') 
        print('Its genotype is:')  
        best_subject.show_yourself()

        self.env.close()