# STILL WORKING ON THIS
# Jack Nason, jnason3@unb.ca, Jan 2026

import random
import matplotlib.pyplot as plt

def InitializeLociAlleleNumbersForPopulation(numberOfLoci: int = 100, minNumber: int = 2, maxNumber: int = 10):
    lociAlleleNums = []

    for i in range(numberOfLoci):

        lociAlleleNums.append(random.randint(minNumber, maxNumber))

    return lociAlleleNums


def CreatePanelOfIndividualLoci(alleleNumbers):
    loci = []

    for i in range(len(alleleNumbers)):

        alleleOne = random.randint(1, alleleNumbers[i])
        alleleTwo = random.randint(1, alleleNumbers[i])

        newLocus = Locus(i, alleleOne, alleleTwo)

        loci.append(newLocus)

    return loci


def CreatePopulation(numberOfIndividuals: int = 1000):
    individuals = []

    for i in range(numberOfIndividuals):
        indLoci = CreatePanelOfIndividualLoci(alleleNums)
        s = "F"
        if (random.randint(1,2) == 2): s = "M"

        newIndividual = Individual(indLoci, s)
        individuals.append(newIndividual)

    return individuals


def ProduceNextGenerationRandomMating(pop, percentageThatMate: float = 0.25, numberOfIndividuals: int = 1000,
                                      minOffspring: int = 1, maxOffspring: int = 10, numberOfPairsPer: int = 3):
    males = []
    females = []

    offspring = []

    for i in pop:
        if i.sex == "M":
            males.append(i)
        else:
            females.append(i)

    numOfEachSexToContribute = round(percentageThatMate * 0.5 * len(pop))

    numMalesToRemove = len(males) - numOfEachSexToContribute
    if (numMalesToRemove < 0): numMalesToRemove = 0

    numFemalesToRemove = len(females) - numOfEachSexToContribute
    if (numFemalesToRemove < 0): numFemalesToRemove = 0

    for i in range(numMalesToRemove):
        random_male = random.choice(males)
        males.remove(random_male)

    for i in range(numFemalesToRemove):
        random_female = random.choice(females)
        females.remove(random_female)

    random.shuffle(females)
    random.shuffle(males)

    for f in females:

        currentMinNumberToScanFor = 0

        while f.mates < numberOfPairsPer:

            random.shuffle(males)

            for m in males:

                if m.mates == currentMinNumberToScanFor:

                    m.mates = m.mates + 1
                    f.mates = f.mates + 1

                    numOffspring = random.randint(minOffspring, maxOffspring)

                    for o in range(numOffspring):

                        newOffspring = Mate(f,m)

                        offspring.append(newOffspring)

                    break

            currentMinNumberToScanFor = currentMinNumberToScanFor + 1

            if (currentMinNumberToScanFor > numberOfPairsPer): break

    random.shuffle(offspring)

    if (len(offspring) > numberOfIndividuals):

        del offspring[:(len(offspring) - numberOfIndividuals)]

    """
    for i in females:
        print(f"f: {i.mates}")
    for i in males:
        print(f"m: {i.mates}")
    """

    return offspring


def Mate(female, male):

    loci = []

    for i in range(len(female.loci)):

        f_allele = 0
        m_allele = 0

        if (random.randint(1,2) == 1): f_allele = female.loci[i].alleleID_1
        else: f_allele = female.loci[i].alleleID_2

        if (random.randint(1,2) == 1): m_allele = male.loci[i].alleleID_1
        else: m_allele = male.loci[i].alleleID_2

        newLocus = Locus(i, f_allele, m_allele)
        loci.append(newLocus)

    s = "F"
    if (random.randint(1, 2) == 2): s = "M"

    return Individual(loci, s)

class Locus:
    locusID = 0
    alleleID_1 = 0
    alleleID_2 = 0

    def __init__(self, locID, aID_1, aID_2):
        self.locusID = locID
        self.alleleID_1 = aID_1
        self.alleleID_2 = aID_2


class Individual:
    loci = []
    sex = ""
    mates = 0
    def __init__(self, locs, sex):
        self.loci = locs
        self.sex = sex

populationSize = 1000
maxNumberOfAllelesAtALocus = 4
numberOfLociToSimulate = 1

alleleNums = InitializeLociAlleleNumbersForPopulation(numberOfLociToSimulate, 2,maxNumberOfAllelesAtALocus)

population = CreatePopulation(populationSize)

numLocOneAlleleOne_F0 = 0

for i in population:
    if i.loci[0].alleleID_1 == 1 or i.loci[0].alleleID_2 == 1: numLocOneAlleleOne_F0 = numLocOneAlleleOne_F0 + 1

numberOfGenerations = 100
locOneAlleleOneFreqs = []

locOneAlleleOneFreqs.append(numLocOneAlleleOne_F0 / (len(population) * 2))

for i in range(numberOfGenerations):

    newGen = ProduceNextGenerationRandomMating(population, numberOfIndividuals=populationSize,
                                               minOffspring=1, maxOffspring=10, numberOfPairsPer=3)

    numLocOneAlleleOne_F1 = 0

    for i in newGen:
        if i.loci[0].alleleID_1 == 1: numLocOneAlleleOne_F1 = numLocOneAlleleOne_F1 + 1
        if i.loci[0].alleleID_2 == 1: numLocOneAlleleOne_F1 = numLocOneAlleleOne_F1 + 1

    locOneAlleleOneFreqs.append(numLocOneAlleleOne_F1 / (len(newGen) * 2))

    population = newGen


print(locOneAlleleOneFreqs)
plt.plot(range(numberOfGenerations + 1), locOneAlleleOneFreqs, marker='o', linestyle='-', color='b')
plt.ylim(0, 1)
plt.xlabel('Generation')
plt.ylabel('Loc 1 - allele A freq.')
#plt.scatter(range(numberOfGenerations), locOneAlleleOneFreqs)
plt.show()

#print(f"Loc 1 Allele 1 freq. in F0: {numLocOneAlleleOne_F0 / (len(population) * 2)}")
#print(f"Loc 1 Allele 1 freq. in F1: {numLocOneAlleleOne_F1 / (len(newGen) * 2)}")