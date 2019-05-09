import random
import math

SIZE_OF_POPULATION = 8
MUTATION_LIKELIHOOD = 0.05
CROSSOVER_LIKELIHOOD = 0.7
VALUES_RANGE = [2,31]

binary_digits_to_represent = int((math.log2(VALUES_RANGE[1])))+1
#while (binary_digits_to_represent % 4 != 0):
#    binary_digits_to_represent += 1

def linear_func(x):
    return (-3)*x + 5
    
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
        self.fitness = linear_func(self.decimal)
    def get_fitness(self):
        return self.fitness
    def __str__(self):
        return str(self.genes) + "- " + str(self.decimal)
        
class Population:
    def set_decimals(self, size):
        return random.sample(range(VALUES_RANGE[0],VALUES_RANGE[1]),size)
    
    def __init__(self,size):
        self.chromosomes = []
        self.chromosomes_decimals = self.set_decimals(size)
        '0 to size-1'
        for i in range(size): 
            self.chromosomes.append(Chromosome(self.chromosomes_decimals[i]))
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
    First, we should select chromosomes that will participate in breeding. They'll be stored in "intermediate list".
    Selection is performed according to the following rule: 
        for each chromosome we estimate BREEDING_LIKELIHOOD = приспособленность особи / ср.приспособленность по популяции
        if whole part from division is n > 0 than we should add chromosome n times to list, and fraction from division
        says what likelihood it has to appear in list 1 more time(if it's greater than RANDOMVAL, then we add it to list) 
        it's called REMAINDER STOCHASTIC SAMPLING
        IT WORKS!
    '''
    @staticmethod
    def selection(pop):
        selection_likelihood = random.random() #to apply adding to interList one more time if succedeed
        interList = Population(0)
        breeding = 0
        breeding_whole = 0
        breeding_fract = 0.0
        sumFitn = 0
        for ch in pop.get_chromosomes() : sumFitn += abs(ch.get_fitness())
        avgFitn = sumFitn / len(pop.get_chromosomes())
        #breeding - данное отношение для каждой особи
        #breeding_whole - целая часть деления
        #breeding_fract - дробная
        for ch in pop.get_chromosomes():
            breeding = abs(ch.get_fitness() / avgFitn) #посчитаем отношение
            breeding_whole = breeding // 1 #посчитаем его целую часть
            breeding_fract = breeding - breeding_whole #вычислим дробную 
            for i in range(int(breeding_whole)):
                interList.get_chromosomes().append(ch)
            if (breeding_fract <= selection_likelihood):
                interList.get_chromosomes().append(ch)
        return interList

    '''
    Then using chromosomes from intermediate list, we randomly pick up pairs for breeding. 
    According to crossover_likelihood this pairs can breed. If they are allowed to breed, their children will be
    added to crossover_pop, else pair itself will be added to crossover_pop
    '''
    @staticmethod
    def crossover_population(pop):
        crossover_pop = Population(0) #where store chosen chromosomes
        while(len(pop.get_chromosomes()) > 1):
            pair = random.sample(pop.get_chromosomes(),2) #randomly select pair of chromosomes
            if (random.random() <= CROSSOVER_LIKELIHOOD):
                crossover_pop.get_chromosomes().extend(GeneticAlgorithm.crossover_chromosomes(pair[0],pair[1]))
            else:
                crossover_pop.get_chromosomes().extend(pair)
            pop.chromosomes = [ch for ch in pop.get_chromosomes() if ch not in pair] # change pop list
        return crossover_pop

    '''
    Here we perform onePoint crossover, get new chromosomes and return them as list
    1)Select the crossover point
    2)Perform 1Point crossover
    3)return list of children
    '''
    @staticmethod
    def crossover_chromosomes(chromosome1, chromosome2):
        leng = len(chromosome1.get_genes())
        idx = random.randint(0,leng) #generate index of crossover point
        var = 0 #for exchange
        while idx < leng:
            var = chromosome1.get_genes()[idx]
            chromosome1.get_genes()[idx] = chromosome2.get_genes()[idx]
            chromosome2.get_genes()[idx] = var
            idx += 1
        return [chromosome1,chromosome2]
   
    @staticmethod
    def mutate_population(pop):
        for i in range(len(pop.get_chromosomes())):
            GeneticAlgorithm.mutate_chromosome(pop.get_chromosomes()[i])
        return pop

    '''
    Here we perform mutation of each chromosome of population according to MUTATION_LIKELIHOOD
    '''
    @staticmethod
    def mutate_chromosome(ch):
        for i in range(len(ch.get_genes())):
            val = random.random() 
            if(val <= MUTATION_LIKELIHOOD):
                #here we should perform mutation
                if(ch.get_genes()[i] == 0): ch.get_genes()[i] = 1
                else: ch.get_genes()[i] = 0
        #should change fitness value of chromosome
        ch.set_decimal()
        ch.set_fitness()

    '''
    Here is main method. It produces new generation using existing one. It calls methods such as:
    1)selection
    2)crossover_population
    3)mutate_population
    '''
    @staticmethod
    def evolve(pop):
        return GeneticAlgorithm.mutate_population(GeneticAlgorithm.crossover_population(GeneticAlgorithm.selection(pop)))

def _print_population(pop,gen_number):
    print("\n-----------------------------------------")
    print("Generation #", gen_number)
    print("-----------------------------------------")
    i = 0
    for ch in pop.get_chromosomes():
        print("Chromosome #", i, " :", ch, "| Fitness: ", ch.get_fitness())
        i += 1

#initialize the population of 8 chromosomes
population = Population(SIZE_OF_POPULATION)
_print_population(population, gen_number=0)
generation_number = 1
while generation_number < 6:
    population = GeneticAlgorithm.evolve(population)
    _print_population(population,generation_number)
    generation_number += 1

#print(population.__str__())
#pop1 = GeneticAlgorithm.selection(population)
#print(pop1.__str__())

#c1 = Chromosome(15)
#print(c1.__str__())
#GeneticAlgorithm.mutate_chromosome(c1)
#print(c1.__str__())
#print(c1.get_decimal())

'''Classical genetic algorithm(Holland)
Случайно генерируем набор параметров функции(ЦФ) - числа,
лежащие на промежутке [xmin, xmax].
Для каждого параметра находим значение ЦФ(его пригодность)
Помним, что для нашей задачи, чем меньше значение, тем лучше
1)Начинается этап селекции параметров в промежуточный массив параметров
годных к размножению. Для каждого параметра высчитываем отношение
его пригодности к средней пригодности по всей популяции, 
целое число отношения покажет сколько раз добавить особь в 
промежуточный массив, в то время как дробная часть покажет
вероятность следующего попадания в промежуточный массив.
Генерируется параметр отбора - число [0,1] и если вероятность
больше этого числа, то особь отбирается в промежуточный массив
снова. Промежуточный массив сформирован.
2)Далее выбираются пары для скрещивания. Если выбранная пара
содержит повторяющиеся хромосомы, то скрещивание не происходит и
выбирается новая пара, иначе происходит скрещивание и выбранные
эл-ты удаляются из промежут массива.
3)  
'''