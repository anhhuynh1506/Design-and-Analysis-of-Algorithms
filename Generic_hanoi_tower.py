import sys
import inspect
import heapq


def raiseNotDefined():
    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    print("*** Method not implemented: %s at line %s of %s" % (method, line, fileName))
    sys.exit(1)


class Stack:
    "A container with a last-in-first-out (LIFO) queuing policy."

    def __init__(self):
        self.list = []

    def push(self, item):
        "Push 'item' onto the stack"
        self.list.append(item)

    def pop(self):
        "Pop the most recently pushed item from the stack"
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the stack is empty"
        return len(self.list) == 0


class Queue:
    "A container with a first-in-first-out (FIFO) queuing policy."

    def __init__(self):
        self.list = []

    def push(self, item):
        "Enqueue the 'item' into the queue"
        self.list.insert(0, item)

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the queue is empty"
        return len(self.list) == 0


class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)


class Counter(dict):
    def __getitem__(self, idx):
        self.setdefault(idx, 0)
        return dict.__getitem__(self, idx)

    def incrementAll(self, keys, count):
        for key in keys:
            self[key] += count

    def argMax(self):
        if len(self.keys()) == 0: return None
        all = self.items()
        values = [x[1] for x in all]
        maxIndex = values.index(max(values))
        return all[maxIndex][0]

    def sortedKeys(self):
        sortedItems = self.items()
        compare = lambda x, y: sign(y[1] - x[1])
        sortedItems.sort(cmp=compare)
        return [x[0] for x in sortedItems]

    def totalCount(self):
        return sum(self.values())

    def normalize(self):
        total = float(self.totalCount())
        if total == 0: return
        for key in self.keys():
            self[key] = self[key] / total

    def divideAll(self, divisor):
        divisor = float(divisor)
        for key in self:
            self[key] /= divisor

    def copy(self):
        return Counter(dict.copy(self))

    def __mul__(self, y):
        sum = 0
        x = self
        if len(x) > len(y):
            x, y = y, x
        for key in x:
            if key not in y:
                continue
            sum += x[key] * y[key]
        return sum

    def __radd__(self, y):
        for key, value in y.items():
            self[key] += value

    def __add__(self, y):
        addend = Counter()
        for key in self:
            if key in y:
                addend[key] = self[key] + y[key]
            else:
                addend[key] = self[key]
        for key in y:
            if key in self:
                continue
            addend[key] = y[key]
        return addend

    def __sub__(self, y):

        addend = Counter()
        for key in self:
            if key in y:
                addend[key] = self[key] - y[key]
            else:
                addend[key] = self[key]
        for key in y:
            if key in self:
                continue
            addend[key] = -1 * y[key]
        return addend


class SearchProblem:

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        raiseNotDefined()


def depthFirstSearch(problem):
    return GraphSearch(problem, "DFS").search()


def breadthFirstSearch(problem):
    return GraphSearch(problem, "BFS").search()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    return GraphSearch(problem, "UCS").search()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    return GraphSearch(problem, "ASTAR", heuristic).search()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch


class Node:
    state = None
    action = None
    father = None
    step_cost = 0
    path_cost = 0

    def __init__(self, state, action, father, step_cost, path_cost):
        self.state = state
        self.action = action
        self.father = father
        self.step_cost = step_cost
        self.path_cost = path_cost


class GraphSearch:
    def __init__(self, problem, type_search, heuristic=None):
        self.problem = problem
        self.type_search = type_search
        self.heuristic = heuristic

    def search(self):
        frontier = Counter()
        visited = Counter()
        fringe = None
        start_state = self.problem.getStartState()
        start_node = Node(start_state, None, None, 0, 0)
        if self.type_search == "DFS":
            fringe = Stack()
            fringe.push(start_node)
        elif self.type_search == "BFS":
            fringe = Queue()
            fringe.push(start_node)
        elif self.type_search == "UCS":
            fringe = PriorityQueue()
            fringe.push(start_node, start_node.path_cost)
        else:
            fringe = PriorityQueue()
            fringe.push(start_node, start_node.path_cost + self.heuristic(start_node.state, self.problem))
        frontier[hash(start_state)] = start_node
        while not fringe.isEmpty():
            node = fringe.pop()
            hash_code = hash(node.state)
            visited[hash_code] = node
            frontier.pop(hash_code, None)
            if self.problem.isGoalState(node.state):
                path = []
                while node is not None:
                    if node.action is not None:
                        path.append(node.action)
                    node = node.father
                result = path[::-1]
                return result
            successors = self.problem.getSuccessors(node.state)
            for x in successors:
                successor, action, step_cost = x
                hash_code_child = hash(successor)
                if visited[hash_code_child] == 0:
                    child = Node(successor, action, node, step_cost, node.path_cost + step_cost)
                    if self.type_search == "DFS":
                        fringe.push(child)
                        if frontier[hash_code_child] == 0:
                            frontier[hash_code_child] = child
                    elif self.type_search == "BFS":
                        if frontier[hash_code_child] == 0:
                            fringe.push(child)
                            frontier[hash_code_child] = child
                    elif self.type_search == "UCS":
                        if frontier[hash_code_child] == 0:
                            fringe.push(child, child.path_cost)
                            frontier[hash_code_child] = child
                        elif frontier[hash_code_child].path_cost > child.path_cost:
                            fringe.update(child, child.path_cost)
                            frontier[hash_code_child] = child
                    else:
                        if frontier[hash_code_child] == 0:
                            fringe.push(child, child.path_cost + self.heuristic(child.state, self.problem))
                            frontier[hash_code_child] = child
                        elif frontier[hash_code_child].path_cost > child.path_cost:
                            fringe.update(child, child.path_cost)
                            frontier[hash_code_child] = child

        return []


# Module Classes

class HNProb:

    def __init__(self, a1, a2, a3):
        # a1:List
        # a2:List
        # a3:List
        self.axis1 = a1
        self.axis2 = a2
        self.axis3 = a3

    def isGoal(self):
        if (self.axis2 == [] and self.axis1 == []):
            for i in range(len(self.axis3) - 1):
                if self.axis3[i] < self.axis3[i + 1]: return False
            return True
        return False

    def legalMoves(self):
        moves = []
        l1, l2, l3 = self.axis1, self.axis2, self.axis3
        if (l1 == []):
            if (l2 != []):
                moves.append('m21')
            if (l3 != []):
                moves.append('m31')
        else:
            if (l2 != []):
                if (l2[-1] < l1[-1]):
                    moves.append('m21')
            if (l3 != []):
                if (l3[-1] < l1[-1]):
                    moves.append('m31')
        if (l2 == []):
            if (l1 != []):
                moves.append('m12')
            if (l3 != []):
                moves.append('m32')
        else:
            if (l1 != []):
                if (l1[-1] < l2[-1]):
                    moves.append('m12')
            if (l3 != []):
                if (l3[-1] < l2[-1]):
                    moves.append('m32')
        if (l3 == []):
            if (l2 != []):
                moves.append('m23')
            if (l1 != []):
                moves.append('m13')
        else:
            if (l2 != []):
                if (l2[-1] < l3[-1]):
                    moves.append('m23')
            if (l1 != []):
                if (l1[-1] < l3[-1]):
                    moves.append('m13')

        return moves

    def result(self, move):

        newPuzzle = HNProb([], [], [])
        newPuzzle.axis1 = self.axis1.copy()
        newPuzzle.axis2 = self.axis2.copy()
        newPuzzle.axis3 = self.axis3.copy()

        if (move == 'm21'):
            temp = newPuzzle.axis2.pop()
            newPuzzle.axis1.append(temp)
        elif (move == 'm31'):
            temp = newPuzzle.axis3.pop()
            newPuzzle.axis1.append(temp)
        elif (move == 'm12'):
            temp = newPuzzle.axis1.pop()
            newPuzzle.axis2.append(temp)
        elif (move == 'm32'):
            temp = newPuzzle.axis3.pop()
            newPuzzle.axis2.append(temp)
        elif (move == 'm13'):
            temp = newPuzzle.axis1.pop()
            newPuzzle.axis3.append(temp)
        elif (move == 'm23'):
            temp = newPuzzle.axis2.pop()
            newPuzzle.axis3.append(temp)
        else:
            raise "Illegal Move"

        return newPuzzle

    # Utilities for comparison and display

    def __hash__(self):
        return hash(str(self.axis1) + str(self.axis2) + str(self.axis3))

    def __getAsciiString(self):
        """
          Returns a display string for the maze
        """
        line = ""
        count = 0
        for x in self.axis1:
            count += 1
            line += x.__str__()
            if(count < len(self.axis1)):
                line += " "
        line += "\n"
        count = 0
        for x in self.axis2:
            count += 1
            line += x.__str__()
            if (count < len(self.axis2)):
                line += " "
        line += "\n"
        count = 0
        for x in self.axis3:
            count += 1
            line += x.__str__()
            if (count < len(self.axis3)):
                line += " "
        line += "\n#"
        return line

    def __str__(self):
        return self.__getAsciiString()


# TODO: Implement The methods in this class

class HanoiProblem(SearchProblem):

    def __init__(self, puzzle):
        self.puzzle = puzzle

    def getStartState(self):
        return puzzle

    def isGoalState(self, state):
        return state.isGoal()

    def getSuccessors(self, state):
        """
          Returns list of (successor, action, stepCost) pairs where
          each succesor is either left, right, up, or down
          from the original state and the cost is 1.0 for each
        """
        succ = []
        for a in state.legalMoves():
            succ.append((state.result(a), a, 1))
        return succ

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)


x = [int(x) for x in input().split()]
y = [int(x) for x in input().split()]
z = [int(x) for x in input().split()]
puzzle = HNProb(x, y, z)
print(puzzle)
problem = HanoiProblem(puzzle)
path = breadthFirstSearch(problem)
curr = puzzle
i = 1
for a in path:
    curr = curr.result(a)
    print(curr)

    i += 1