import random
import math
import matplotlib.pyplot as plt


class Cities:

    def __init__(self, xcord=0, ycord=0):
        if(xcord == 0):
            self.x = random.randint(1, 100)
            self.y = random.randint(1, 100)
        else:
            self.x = xcord
            self.y = ycord

    def __str__(self):
        return 'x=' + str(self.x) + ' y=' + str(self.y)


class Agent:

    def __init__(self, nrCities):
        string = []
        module = nrCities - 1
        for i in range(nrCities):
            string.append(random.randint(0, module))
            module -= 1
        self.string = string
        self.decoded = []
        self.distance = 999999
        self.selection = -1

    def __str__(self):
        return str(self.string) + ' ' + str(self.decoded) + ' ' + str(self.distance)


def TSP(nr_population, generations, m_prob, nrCities=0, data=''):
    bestDistance = 999999
    best_this_generation = 999999
    cities_list = initCities(data, nrCities)
    if data != '':
        nrCities = len(cities_list)
    population = initPopulation(nrCities, nr_population)

    for generation in range(generations):
        population = crossOver(population, nrCities)
        population = mutation(population, m_prob, nrCities)

        decode(population, nrCities)
        calculateDistance(population, cities_list, nrCities)
        best_this_generation, agent = Best_this_generation(population)
        if best_this_generation < bestDistance:
            bestDistance = best_this_generation
            return_agent = agent

        population = selection(population)

        print('Generation: ' + str(generation))
        print('best this gen: ', best_this_generation,
              '\n 		best: ', bestDistance)

    print('best distance:', bestDistance)
    return bestDistance, return_agent, cities_list


def initPopulation(nrCities, nr_population):
    return [Agent(nrCities) for _ in range(nr_population)]


def initCities(data, nrCities):
    if data == '':
        return [Cities() for _ in range(nrCities)]
    else:
        file = open(data)
        ret = []
        for lin in file:
            if lin[0] in '1234567890':
                nr = lin.split(' ')
                ret.append(Cities(float(nr[1]), float(nr[2])))
        return ret


def calculateDistance(population, cities_list, nrCities):
    for agent in population:
        agent.distance = 0
        for i in range(nrCities - 1):
            agent.distance += round(math.sqrt((cities_list[agent.decoded[i + 1]].x - cities_list[agent.decoded[
                                    i]].x)**2 + (cities_list[agent.decoded[i + 1]].y - cities_list[agent.decoded[i]].y)**2))
        agent.distance += round(math.sqrt((cities_list[agent.decoded[nrCities - 1]].x - cities_list[agent.decoded[
                                0]].x)**2 + (cities_list[agent.decoded[nrCities - 1]].y - cities_list[agent.decoded[0]].y)**2))


def Best_this_generation(population):
    best = population[0].distance
    return_agent = population[0]
    for agent in population:
        if best > agent.distance:
            best = agent.distance
            return_agent = agent
    return best, return_agent


def decode(population, nrCities):
    nr_city = [i for i in range(nrCities)]
    for agent in population:
        copy = nr_city[:]
        agent.decoded = []
        for i in agent.string:
            agent.decoded.append(copy.pop(i))


def crossOver(population, nrCities):
    copy_population = []
    for _ in range(len(population) // 2):
        if random.random() < 0.175:
            split = random.randint(1, nrCities - 2)
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            child1 = Agent(nrCities)
            child2 = Agent(nrCities)
            child1.string = parent1.string[:split] + parent2.string[split:]
            child2.string = parent2.string[:split] + parent1.string[split:]
            copy_population.append(child1)
            copy_population.append(child2)
        else:
            copy_population.append(random.choice(population))
            copy_population.append(random.choice(population))
    return copy_population


def mutation(population, m_prob, nrCities):
    for agent in population:
        copy_agent = []
        module = nrCities - 1
        for i in range(nrCities):
            if random.random() < m_prob:
                copy_agent.append(random.randint(0, module))
            else:
                copy_agent.append(agent.string[i])
            module -= 1
        agent.string = copy_agent
    return population


def selection(population):
    max_distance = 0
    for agent in population:
        if max_distance < agent.distance:
            max_distance = agent.distance
    max_distance += 1
    max_distance2 = 0
    for agent in population:
        agent.selection = (max_distance - agent.distance)
        max_distance2 += agent.selection
    prev = 0
    vec = []
    for agent in population:
        vec.append(agent.selection / max_distance2 + prev)
        prev = vec[-1]
    vec[-1] = 1
    copy_population = []
    for i in range(len(population)):
        rand = random.random()
        for j in range(len(vec)):
            if rand <= vec[j]:
                copy_population.append(population[j])
                break

    return copy_population


def draw(agent, cities):
    for i in range(len(agent.decoded) - 1):
        x = [cities[agent.decoded[i]].x, cities[agent.decoded[i + 1]].x]
        y = [cities[agent.decoded[i]].y, cities[agent.decoded[i + 1]].y]
        plt.plot(x, y, marker='o')
    x = [cities[agent.decoded[i + 1]].x, cities[agent.decoded[0]].x]
    y = [cities[agent.decoded[i + 1]].y, cities[agent.decoded[0]].y]
    plt.plot(x, y, marker='o')

    plt.show()

nr_population = 800
generations = 2000
m_prob = 0.003

best, agent, cities = TSP(nr_population, generations, m_prob, 0, 'sahara.tsp')
# orase: sahara djibouti qatar

draw(agent, cities)
