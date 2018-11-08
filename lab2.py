import time
import random
import numpy as np
import math

class Board(object):
    """An N-queens candidate solution ."""

    def __init__(self, N):
        """A random N-queens instance"""
        self.queens = dict()
        for col in range(N):
            row = random.choice(range(N))
            self.queens[col] = row

    def display(self):
        """Print the board."""
        for r in range(len(self.queens)):
            for c in range(len(self.queens)):
                if self.queens[c] == r:
                    print 'Q',
                else:
                    print '-',
            print
        print "cost: ", self.cost()
        print

    def copy(self, board):
        """Copy a board (prevent aliasing)"""
        copyBoard = Board(8)
        for col in range(len(copyBoard.queens)):
            copyBoard.queens[col] = board.queens[col]
        return copyBoard

    def moves(self):
        """Return a list of possible moves given the current placements."""
        moves = dict()
        for r in range(len(self.queens)):
            # r is key in dict
            for c in range(len(self.queens)):
                # c is element in dict
                if self.queens[c]+1 <= r:  # Should look at row up one
                    moves[r] = (self.queens[c]+1)
                elif self.queens[c]-1 >= r:    # Should look at row down one
                    moves[r] = (self.queens[c]-1)
        return moves

    def neighbor(self, move):
        """Return a Board instance like this one but with one move made."""
        moveBoard = Board(8)
        if len(self.moves()) > 0:
            c = self.moves().get(move)
            r = self.moves().get(move)
            self.queens[c] = r
        return moveBoard

    def crossover(self, board):
        """Return a Board instance that is a recombination with its argument."""
        crossBoard = Board(8)
        split = random.randint(0, len(crossBoard.queens))
        copyBoard = self.copy(self)
        for c in range(split):
            crossBoard.queens[c] = copyBoard.queens[c]
        for c in range(split, len(board.queens)):
            crossBoard.queens[c] = board.queens[c]
        return crossBoard

    def cost(self):
        """Compute the cost of this solution."""
        cost = 0
        for r in range(0, len(self.queens)):
            for c in range(r + 1, len(self.queens)):
                diag = r - c
                if self.queens[r] == self.queens[c] or abs(r - c) == abs(self.queens[r] - self.queens[c]):
                    cost = cost + 1
                # diagonals
                if self.queens[r] == self.queens[c] - diag or self.queens[r] == self.queens[c] + diag:
                    cost += 1
        return cost



class EvolutionaryAlgorithm(object):
    def evolve(self, popsize, pc):
        population = []
        for i in range(popsize):
            population.append(Board(8));
        steps = 0
        while (population[0].cost() > 0):
            x = population[random.choice(range(popsize))]
            if random.random() < pc:
                y = population[random.choice(range(popsize))]
                x = x.crossover(y)
            for i in range(np.random.poisson() + 1):
                mlist = x.moves()
                x = x.neighbor(random.choice(mlist))
            population.append(x)
            population = [x for _, x in sorted(zip(map(Board.cost, population), population))]
            population.pop()
            if (steps % 1000 == 0):
                population[0].display()
                #time.sleep(.1)
            steps = steps + 1

        population[0].display()
        return steps


class SimulatedAnnealing(object):
    def anneal(self, startTemp, decayRate):
        ## Initial random board
        x = Board(8)
        steps = 0
        while x.cost() != 0:
            # let neighbor be a random neighbor of solution
            neighbor = x.neighbor(random.choice(range(len(x.queens))))
            if neighbor.cost() < x.cost():
                x = neighbor
            else:
                netCost = abs(neighbor.cost() - x.cost())
                p = math.pow(math.e, -netCost/startTemp)
                if p > random.random():
                    x = neighbor
            startTemp = startTemp * decayRate
            ## Display best every 1000 steps
            if (steps % 1000 == 0):
                x.display()
                #time.sleep(0.1)
            steps = steps + 1
        x.display()
        return steps



def main():
    """Create a problem, solve it with simulated anealing, and console-animate."""
    ea = EvolutionaryAlgorithm();
    ea_steps = ea.evolve(50, .35);
    sa = SimulatedAnnealing()
    sa_steps = sa.anneal(100, .9)
    print "The evolutionary algorithm solved the problem in ", ea_steps, " steps "
    print "Simulated annealing solved the problem in ", sa_steps, " steps"

if __name__ == '__main__':
    main()