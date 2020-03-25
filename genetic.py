"""
Simple genetic algorithm guessing a string.
"""
 
# ----- Dependencies
 
from random import random
from string import ascii_letters
 
# One-linner for randomly choose a element in an array
# This one-linner is fastest than random.choice(x).
choix = lambda x: x[int(random() * len(x))]
 
# Enter here the string to be searched
RESULTA_ATTENDU = "REiniTialiSation de 2.20"
 
# Enter here the chance for an individual to mutate (range 0-1)
CHANCE_DE_MUTER = 0.1
 
# Enter here the percent of top-grated individuals to be retained for the next generation (range 0-1)
CHANCE_DE_REPECHAGE = 0.2
 
# Enter here the chance for a non top-grated individual to be retained for the next generation (range 0-1)
CHANCE_DE_NON_REPECHAGE = 0.05
 
# Number of individual in the population
POPULATION_COUNT = 100
 
# Maximum number of generation before stopping the script
NB_MAX_GENERATION = 100000
 
# ----- Do not touch anything after this line
 
# Number of top-grated individuals to be retained for the next generation
NB_INDIVIDU_A_EVOLUER = int(POPULATION_COUNT * CHANCE_DE_REPECHAGE)
 
# Precompute the length of the expected string (individual are always fixed size objects)
TAILLE_RESULTAT = len(RESULTA_ATTENDU)
 
# Precompute TAILLE_RESULTAT // 2
MOITIE_RESULTAT = TAILLE_RESULTAT // 2
 
# Charmap of all allowed characters (A-Z a-z, space and !)
CHARACTERE_UTILISER = ascii_letters + ' !\'.'
 
# Maximum fitness value
FITNESS_MAX = TAILLE_RESULTAT
 
# ----- Genetic Algorithm code
# Note: An individual is simply an array of TAILLE_RESULTAT characters.
# And a population is nothing more than an array of individuals.
 
def obtenir_char_aleatoire():
    """ Return a random char from the allowed charmap. """
    return choix(CHARACTERE_UTILISER)
     
 
def obtenir_un_invidu_x():
    """ Create a new random individual. """
    return [obtenir_char_aleatoire() for _ in range(TAILLE_RESULTAT)]
 
 
def creer_une_population():
    """ Create a new random population, made of `POPULATION_COUNT` individual. """
    return [obtenir_un_invidu_x() for _ in range(POPULATION_COUNT)]
 
 
def avoir_le_fitness(individual):
    """ Compute the fitness of the given individual. """
    fitness = 0
    for c, expected_c in zip(individual, RESULTA_ATTENDU):
        if c == expected_c:
            fitness += 1
    return fitness
 
 
def moyenne_population(population):
    """ Return the average fitness of all individual in the population. """
    total = 0
    for individual in population:
        total += avoir_le_fitness(individual)
    return total / POPULATION_COUNT
 
 
def classer_population(population):
    """ Grade the population. Return a list of tuple (individual, fitness) sorted from most graded to less graded. """
    graded_individual = []
    for individual in population:
        graded_individual.append((individual, avoir_le_fitness(individual)))
    return sorted(graded_individual, key=lambda x: x[1], reverse=True)
 
 
def faire_evoluer(population):
    """ Make the given population evolving to his next generation. """
 
    # Get individual sorted by grade (top first), the average grade and the solution (if any)
    raw_graded_population = classer_population(population)
    average_grade = 0
    solution = []
    graded_population = []
    for individual, fitness in raw_graded_population:
        average_grade += fitness
        graded_population.append(individual)
        if fitness == FITNESS_MAX:
            solution.append(individual)
    average_grade /= POPULATION_COUNT
 
    # End the script when solution is found
    if solution:
        return population, average_grade, solution    
 
    # Filter the top graded individuals
    parents = graded_population[:NB_INDIVIDU_A_EVOLUER]
 
    # Randomly add other individuals to promote genetic diversity
    for individual in graded_population[NB_INDIVIDU_A_EVOLUER:]:
        if random() < CHANCE_DE_NON_REPECHAGE:
            parents.append(individual)
 
    # Mutate some individuals
    for individual in parents:
        if random() < CHANCE_DE_MUTER:
            place_to_modify = int(random() * TAILLE_RESULTAT)
            individual[place_to_modify] = obtenir_char_aleatoire()
 
    # Crossover parents to create children
    parents_len = len(parents)
    desired_len = POPULATION_COUNT - parents_len
    children = []
    while len(children) < desired_len:
        father = choix(parents)
        mother = choix(parents)
        if True: #father != mother:
            child = father[:MOITIE_RESULTAT] + mother[MOITIE_RESULTAT:]
            children.append(child)
 
    # The next generation is ready
    parents.extend(children)
    
    return parents, average_grade, solution
 
 
# ----- Runtime code
 
def main():
    """ Main function. """
 
    # Create a population and compute starting grade
    population = creer_une_population()
    
    average_grade = moyenne_population(population)
    print('Starting grade: %.2f' % average_grade, '/ %d' % FITNESS_MAX)
 
    # Make the population evolve
    i = 0
    ancien_i = i
    j=0
    solution = None
    log_avg = []
    solution_gen = []
    solution_ind = []
    while not solution and i < NB_MAX_GENERATION:
        population, average_grade, solution = faire_evoluer(population)
        for individual in population:
            if(ancien_i != i):
                j=0
                ancien_i = i
            if(avoir_le_fitness(individual)==FITNESS_MAX):
                solution_ind.append(j+1)
                solution_gen.append(i)
            print("individu: {0} - generation: {1} => {2}".format(j+1,i,individual))
            j+=1
        pass
        if i & 255 == 255:
            print('Current grade: %.2f' % average_grade, '/ %d' % FITNESS_MAX, '(%d generation)' % i)
        if i & 31 == 31:
            log_avg.append(average_grade)
        i += 1
 
    
    # Print the final stats
    average_grade = moyenne_population(population)
    print('Final grade: %.2f' % average_grade, '/ %d' % FITNESS_MAX)
 
    # Print the solution
    if solution:
        print('Solution obtenue (%d times) apres %d generations.' % (len(solution), i))
        print('generation => individu {0} , {1} resultat : {2}'.format(solution_gen,solution_ind,RESULTA_ATTENDU))
    else:
        print('pas de solutions %d generations.' % i)
        print('- Last population was:')
        for number, individual in enumerate(population):
            print(number, '->',  ''.join(individual))
 
 
if __name__ == '__main__':
    main()