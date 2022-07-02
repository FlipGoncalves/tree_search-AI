
# Module: tree_search
# 
# This module provides a set o classes for automated
# problem solving through tree search:
#    SearchDomain  - problem domains
#    SearchProblem - concrete problems to be solved
#    SearchNode    - search tree nodes
#    SearchTree    - search tree with the necessary methods for searhing
#
#  (c) Luis Seabra Lopes
#  Introducao a Inteligencia Artificial, 2012-2019,
#  Inteligência Artificial, 2014-2019

from abc import ABC, abstractmethod
import time

# Dominios de pesquisa
# Permitem calcular
# as accoes possiveis em cada estado, etc
class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state, goal):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal
    def goal_test(self, state):
        return self.domain.satisfies(state,self.goal)

# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self,state,parent, depth, cost, heuristic=0): 
        self.state = state
        self.parent = parent
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic
    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + ")"
    def __repr__(self):
        return str(self)

    def in_parent(self, node):
        if self.parent == None:
            return False
        if self.state == node:
            return True
        return self.parent.in_parent(node)

# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self,problem, strategy='breadth'): 
        self.problem = problem
        root = SearchNode(problem.initial, None, 0, 0, 0)
        self.open_nodes = [root]
        self.strategy = strategy
        self.terminals = 0
        self.non_terminals = 0
        self.solution = None
        self.cost = 0

    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return(path)

    # procurar a solucao
    def search(self, limit = 100):
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            self.terminals = len(self.open_nodes)
            if node.depth <= limit:
                if self.problem.goal_test(node.state):
                    self.solution = node
                    self.solution.heuristic = 0
                    self.cost = self.solution.cost
                    self.avg_branching = round((self.terminals+self.non_terminals-1)/self.non_terminals, 2)
                    print(self.terminals)
                    print(self.non_terminals)
                    return self.get_path(node)
                lnewnodes = []
                for a in self.problem.domain.actions(node.state):
                    newstate = self.problem.domain.result(node.state,a)
                    node.heuristic = self.problem.domain.heuristic(node.state, newstate)
                    s = self.problem.domain.heuristic(newstate, self.problem.goal)
                    newnode = SearchNode(newstate,node, node.depth +1, node.cost + self.problem.domain.cost(node.state, a), s)
                    if not node.in_parent(newstate):
                        lnewnodes.append(newnode)
                self.non_terminals += 1
                self.add_to_open(lnewnodes)
        return None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'uniform':
            self.open_nodes[:0] = lnewnodes
            self.open_nodes = sorted(self.open_nodes, key=lambda x: x.cost, reverse=False)
        elif self.strategy == 'greedy':
            self.open_nodes[:0] = lnewnodes
            self.open_nodes = sorted(self.open_nodes, key=lambda x: x.heuristic, reverse=False)
        elif self.strategy == 'a*':
            self.open_nodes[:0] = lnewnodes
            self.open_nodes = sorted(self.open_nodes, key=lambda x: x.heuristic + x.cost, reverse=False)

    @property
    def length(self):
        return self.solution.depth