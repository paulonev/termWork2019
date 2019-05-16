import random
import math

SIZE_OF_POPULATION = 8
MUTATION_LIKELIHOOD = 0.5
VALUES_RANGE = [0,31]

binary_digits_to_represent = int((math.log2(VALUES_RANGE[1]))) + 1

#-(x**2) + 25*x + 15 both are possible
def quadr_func(x):
    return x**5 - 35*(x**3) -2*(x**2) + 3
    
def convert_to_binary(value_to_convert):
    genes = []
    counter = 0
    while(counter < binary_digits_to_represent):
        if(value_to_convert // 2 >= 1):
            genes.insert(0,value_to_convert % 2)
            value_to_convert = value_to_convert // 2
        elif (value_to_convert // 2 == 0 and value_to_convert != 0):
            genes.insert(0,value_to_convert)
            value_to_convert = 0 
        else:
            genes.insert(0,0)
        counter += 1
    return genes

def deconvert(binary_arr):
    binary_arr = list(reversed(binary_arr))
    value = 0
    i=0
    while(i < len(binary_arr)):
        value += binary_arr[i] * (2**i)
        i += 1
    return value

class Chromosome:
    def __init__(self,val):
        self.genes = convert_to_binary(val)
        self.decimal = val
        self.fitness = 0
    def get_genes(self):
        return self.genes
    def set_decimal(self):
        self.decimal = deconvert(self.genes)
    def get_decimal(self):
        return self.decimal
    def set_fitness(self):
        self.fitness = quadr_func(self.decimal)
    def get_fitness(self):
        return self.fitness
    def __str__(self):
        return str(self.genes)
    def __eq__(self, other): #for operations of comparisons
        return self.genes == other.genes
    def __hash__(self):
        return hash(tuple(self.genes))


class Population:
    def set_decimals(self, size):
        return random.sample(range(VALUES_RANGE[0],VALUES_RANGE[1]),size) #N
    
    def __init__(self,size):
        self.chromosomes = []
        self.chromosomes_decimals = self.set_decimals(size)
        '0 to size-1'
        for i in range(size): 
            self.chromosomes.append(Chromosome(self.chromosomes_decimals[i])) #N
            self.chromosomes[i].set_fitness()
    
    def get_chromosomes(self) : return self.chromosomes
    
    def __str__(self):
        string = ""
        for x in self.chromosomes:
            string += x.__str__() + "\n"
        return string
    
    def __len__(self):
        return len(self.chromosomes)
    
    def get_chromosomes_decimals(self) : return self.chromosomes_decimals   

class GeneticAlgorithm:    

    '''
    defines index of line segment where random value lies, this index would be an index of chosen chromosome
    ranks is a list of available ranks (list of ranks from 1 to SIZE_OF_POPULATION)
    '''
    @staticmethod
    def selectSegment(ranks):
        val = random.uniform(0, sum(ranks))
        i = 0
        for i, rank in enumerate(ranks):
            val -= rank
            if val <= 0:
                break
        return i

    '''
    Method that selects a couple for breeding using rank & roulette wheel selections
    Rank - chromosomes are sorted and given ranks from worst(1) to best(8) and roulette wheel because
    we give each chromosome line segment on the line and select that chromosome where rand value is located
    '''
    #here to check chromosomes with equal genes, and eliminate those using set object
        #and before we start to select chromosomes we should update decimals and fitnesses
        #to store selected couple of chromosomes
        #because we select two chromosomes


    @staticmethod
    def pair_selection(pop):
        pair = [] 
        for i in range(2): 
            pair.append(pop.get_chromosomes()
            [GeneticAlgorithm.selectSegment(range(1,pop.get_chromosomes().__len__()))]
            )
        return [pair[0], pair[1]]

    '''
    This is the method of uniform crossover. Here we use a mask (a list of zeros and ones, which we obtain
    using convert_to_binary method of this app). Rule: if i-th element of mask is 0 than i-th element of child
    would be i-th elem of parent1, mask i-th elem is 1 - child i-th elem will be parent2 i-th elem
    Method returns new chromosome
    '''
        #create a mask for uniform crossover
        #define a child chromosome

    @staticmethod
    def crossover_chromosomes(_chromosomes):
        mask = convert_to_binary(random.randint(VALUES_RANGE[0],VALUES_RANGE[1]))
        childChromosome = Chromosome(0)
        for i in range(len(mask)):
            if mask[i] == 0 : childChromosome.get_genes()[i] = _chromosomes[0].get_genes()[i]
            else : childChromosome.get_genes()[i] = _chromosomes[1].get_genes()[i]
        return childChromosome
        
    @staticmethod
    def mutate_chromosome(ch):
        for i in range(len(ch.get_genes())):
            val = random.random() 
            if(val <= MUTATION_LIKELIHOOD):
                #here we should perform mutation
                if(ch.get_genes()[i] == 0): ch.get_genes()[i] = 1
                else: ch.get_genes()[i] = 0
        ch.set_decimal()
        ch.set_fitness()
        return ch

    '''
    This method is used to compare new chromosome with the worst chromosome of population
    If fitness of worst chromosome is worse then we change it to new chromosome. 
    0 - because pop is a sorted population from worse to best chromosome
    Also after 
    '''
    @staticmethod
    def comparison(pop, ch):
        if(pop.get_chromosomes()[0].get_fitness() > ch.get_fitness()):
            pop.get_chromosomes()[0] = ch
        pop.chromosomes = list(set(pop.get_chromosomes())) #eliminate repeated chromosomes
        return pop

    '''
    This method upgrades the population by removing duplicates 
    and changing 1 chromosome for one iteration
    '''
    @staticmethod
    def evolve(pop):
        return GeneticAlgorithm.comparison(pop,
            GeneticAlgorithm.mutate_chromosome(
                GeneticAlgorithm.crossover_chromosomes(
                    GeneticAlgorithm.pair_selection(pop)
                )
            )
        )       

def _print_population(pop,gen_number):
    print("\n-----------------------------------------")
    print("Generation #", gen_number)
    print("-----------------------------------------")
    i = 0
    for ch in pop.get_chromosomes():
        print("Chromosome #", i, " :", ch, "| Fitness: ", ch.get_fitness())
        i += 1

'''
define variable of greatest fitness, so that if chromosome's fitness reaches this value
algorithm stops and shows how many generations passed to reach fittest chromosome(s)
'''

population = Population(SIZE_OF_POPULATION)
population.get_chromosomes().sort(key=lambda x: x.get_fitness(), reverse=True)
_print_population(population, gen_number=0)

generation_number = 1
while population.get_chromosomes().__len__() != 1:
    population = GeneticAlgorithm.evolve(population)
    population.get_chromosomes().sort(key=lambda x: x.get_fitness(), reverse=True)
    _print_population(population,generation_number)
    generation_number += 1
