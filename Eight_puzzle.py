from array import array
from collections import deque

m, n = input().split()
m = int(m)
n = int(n)

class State:
	global m
	global n
	def __init__(self, listState, parent, pos):
		self.listState = listState
		self.parent = parent
		self.pos = pos

	def GetCurrentPos(self):
		return self.pos

	def Print(self):
		index = 0
		for i in range(m):
			for j in range(n):
				print(self.listState[index+j], end=' ')
			print('\n')
			index += n



test = (m - 1, n - 1)
inital_state = array('H')

goal = array('H', range(1, m*n+1))
goal[m*n-1] = 0
startPos = ()

for i in range(m):
	listNumber = [int(i) for i in input().split()]
	for number in listNumber:
		inital_state.append(number)

for index, val in enumerate(inital_state):
	if val == 0:
		startPos = (index//n, index%n)
		break

startState = State(inital_state, None, startPos)

length1 = len(inital_state)

def GetNeighbourState(state, pos, explored):
	global m
	global n

	listNewState = []
	currentList = state.listState
	indexStart = pos[1] + n * pos[0]

	# Left
	if 0 <= pos[1] - 1 < n:
		indexTarget = pos[1] - 1 + n * pos[0]

		currentList[indexStart], currentList[indexTarget] = currentList[indexTarget], currentList[indexStart]

		value = tuple(currentList)
		if value not in explored.keys():
			newState = currentList[:]
			listNewState.append(State(newState, state, (pos[0], pos[1]-1)))

		currentList[indexStart], currentList[indexTarget] = currentList[indexTarget], currentList[indexStart]

	# Up
	if 0 <= pos[0] - 1 < m:
		indexTarget = pos[1] + n * (pos[0] - 1)

		currentList[indexStart], currentList[indexTarget] = currentList[indexTarget], currentList[indexStart]

		value = tuple(currentList)
		if value not in explored.keys():
			newState = currentList[:]
			listNewState.append(State(newState, state, (pos[0]-1, pos[1])))

		currentList[indexStart], currentList[indexTarget] = currentList[indexTarget], currentList[indexStart]

	# Right
	if 0 <= pos[1] + 1 < n:
		indexTarget = pos[1] + 1 + n * pos[0]

		currentList[indexStart], currentList[indexTarget] = currentList[indexTarget], currentList[indexStart]

		value = tuple(currentList)
		if value not in explored.keys():
			newState = currentList[:]
			listNewState.append(State(newState, state, (pos[0], pos[1]+1)))

		currentList[indexStart], currentList[indexTarget] = currentList[indexTarget], currentList[indexStart]

	# Down
	if 0 <= pos[0] + 1 < m:
		indexTarget = pos[1] + n * (pos[0] + 1)

		currentList[indexStart], currentList[indexTarget] = currentList[indexTarget], currentList[indexStart]

		value = tuple(currentList)
		if value not in explored.keys():
			newState = currentList[:]
			listNewState.append(State(newState, state, (pos[0]+1, pos[1])))

		currentList[indexStart], currentList[indexTarget] = currentList[indexTarget], currentList[indexStart]

	return listNewState


def BFS(startState):
	global goal, allowTable, test

	frontier = deque()
	frontier.append(startState)
	explored = {}
	value = tuple(startState.listState)
	explored[value] = True

	while frontier:
		state = frontier.popleft()
		pos = state.GetCurrentPos()

		if state.listState == goal:
			return state

		for stateNeighbour in GetNeighbourState(state, pos, explored):
			frontier.append(stateNeighbour)
			value = tuple(stateNeighbour.listState)
			explored[value] = True


stateResult = BFS(startState)
temp = stateResult
result = []

while temp:
	result.append(temp)
	temp = temp.parent

for i in reversed(result):
	i.Print()
	print('-')