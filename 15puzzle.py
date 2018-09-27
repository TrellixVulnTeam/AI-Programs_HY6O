import sys
import random
#import xlsxwriter
from collections import deque
import time
import pickle
from heapq import heappush, heappop
# heappush(list, item)
# heappop(list)


def main():
    global size
    global goal

    filename = "16puzzle.txt"
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    goal = "0ABCDEFGHIJKLMNO"
    sum_time = 0
    count = 0

    for line in lines:
        sep = line.split(" ")
        size = 4
        state = sep[0].replace("\n", "")

        print("%s: (depth: %s)" % (state, count))

        try:
            start = time.process_time()
            solve_bfs_zoom(state)
            end = time.process_time()
            sum_time = sum_time + (end - start)
            print("\tBFS %s" % (end - start))
        except MemoryError:
            print("\tBFS Memory Error")

        # start = time.process_time()
        # id_dfs(state, count)
        # end = time.process_time()
        # sum_time = sum_time + (end - start)
        # print("\tID_DFS %s" % (end - start))

        count += 1


def solve_kdfs(start, k):
    fringe = deque()
    fringe.append((start, 0, {start, }, ""))
    while len(fringe) is not 0:
        v = fringe.pop()
        if goal_test(v[0]):
            return v
        if v[1] < k:
            children = get_children(v[0])
            for child in children:
                if child not in v[2]:
                    a = set(v[2])
                    a.add(child)
                    fringe.append((child, v[1] + 1, a, v[3]+children.get(child)))
    return None


def id_dfs(start, max):
    for k in range(1, max):
        sol = solve_kdfs(start, k)
        if sol is not None:
            return sol
    return None


def solve_bfs_original(state):
    # finds the path to the goal state from a given state using a breadth first search algorithm
    startState = state
    start = (state, "")
    fringe = deque()
    fringe.append(start)
    visited = {state, }

    if parity_check(state) == 1:   #
        return -1                 # if parity determines its not solveable

    while len(fringe) is not 0:
        v = fringe.popleft()
        if goal_test(v[0]):
            return v[1]
        children = get_children(v[0])
        for child in children.keys():
            if child not in visited:
                fringe.append((child, v[1]+children.get(child, 0)))
                visited.add(child)
    if len(fringe) is 0:
        return -1


def solve_bfs_zoom(state):
    # finds the path to the goal state from a given state using a breadth first search algorithm
    start_state = state
    fringe_top = deque()
    fringe_top.append((state, 0), )
    fringe_bottom = deque()
    fringe_bottom.append((goal, 0), )
    visited_top = {state, }
    visited_bottom = {goal, }
    fringe_t = {state, }

    if parity_check(state) == 1:   #
        return -1                 # if parity determines its not solveable

    while len(fringe_top) is not 0 and len(fringe_bottom) is not 0:
        vt = fringe_top.pop()                                     # your standard BFS algorithm
        vb = fringe_bottom.pop()
        if vb[0] in visited_top:
            for state in fringe_top:
                if state[0] == vb[0]:
                    return state[1] + vb[1]
        if goal_test(vt[0]):
            return vt[1]
        children = get_children(vt[0])
        for child in children.keys():
            if child not in visited_top:
                fringe_top.appendleft((child, vb[1]+1))
                visited_top.add(child)
        children = get_children(vb[0])
        for child in children.keys():
            if child not in visited_bottom:
                fringe_bottom.appendleft((child, vb[1]+1))
                visited_bottom.add(child)
    if len(fringe_top) is 0 and len(fringe_bottom) is 0:
        return -2



def parity_check(state):

    i = state.index("0")
    # state = state.replace("0", "")  # removes the 0 from the state string

    # print(parityCount(state))
    if goal == "012345678":
        count = parity_count(state)
    else:
        count = abs(parity_count(goal) - parity_count(state))

    if size % 2 == 1:  # if size is odd
        if count % 2 == 1:  # if count is even
            return 1  # its solvable
        else:
            return 0
    else:  # if size if even
        if (i // size) % 2 == 1:  # if the 0 was in an odd row
            if count % 2 == 0:  # if the count is even
                return 1  # not solvable
            else:
                return 0
        else:  # if the 0 was in an even row
            if count % 2 == 1:  # if the count is odd
                return 1  # not solvable
            else:
                return 0


def parity_count(state):
    count = 0  # variable to count the number of out of order pairs
    i = state.index("0")
    state = state.replace("0", "")  # removes the 0 from the state string
    for char in state:
        for check in state[state.index(char):]:
            if char > check:
                count = count + 1  # iterates through all characters in the state,
                #  adding to the count varible if the character is out of order
    return count


def taxicab_dist(state):
    summ = 0
    for char in state:
        y_goal = goal.index(char) / size
        x_goal = goal.index(char) % size
        y_cur = state.index(char) / size
        x_cur = state.index(char) % size
        summ += abs(y_goal-y_cur) + abs(x_goal-x_cur)
    return summ


def random_state():
    # generates a random state by shuffling the string "012345678"
    return(''.join(random.sample("012345678", 9)))


def random_solvable():
    # generates a random but solvable state
    state = random_state()   # random state
    while (parity_check(state)) is 1:   # while it's not solvable
        state = random_state()          # shuffle again
    return state


def get_children(state):
    # returns a dictionary of the children from a state, each child's value being the move direction used to get there
    children = {up(state): "1", right(state): "2", down(state): "3", left(state): "4"}
    # children.pop(state, None)  # removes states that are the same as the original (i.e. if "moved up" from top row)
    return children

# up: 1, right: 2, down: 3, left: 4


def left(state):
    # moves space left
    i = state.index("0")
    if i % size is not 0:
        newState = state[:i-1] + state[i] + state[i-1] + state[i+1:]
        #print_puzzle(newState)
        return(newState)
    else:
        return(state)


def right(state):
    # moves space right
    i = state.index("0")
    if i % size is not size-1:
        newState = state[:i] + state[i+1] + state[i] + state[i+2:]
        # print_puzzle(newState)
        return(newState)
    else:
        return(state)


def up(state):
    # moves space up
    i = state.index("0")
    if int(i/size) is not 0:
        if(i-size > 0):
            newState = state[:max(0, i-size)] + state[i] + state[max(0, i-size)+1:i] + state[max(0, i-size)] + state[i+1:]
        else:
            newState =  state[i] + state[max(0, i - size) + 1:i] + state[max(0, i - size)] + state[i + 1:]
        # print_puzzle(newState)
        return(newState)
    else:
        return(state)


def down(state):
    # moves space down
    i = state.index("0")
    if int(i/size) is not size-1:
        if(i+size+1<=size*size-1):
            newState = state[:i] + state[i+size] + state[i+1:i+size] + state[i] + state[i+size+1:]
        else:
            newState = state[:i] + state[i + size] + state[i + 1:i + size] + state[i]
        # print_puzzle(newState)
        return(newState)
    else:
        return(state)


def goal_test(state):
    # if a state is at the goal state
    if state == goal:
        return True


def print_puzzle(state):
    # prints the puzzle in a more user friendly way
    for x in range(0, size):
        print(" ".join(state[x*size:(x+1)*size]))
    print("")

if __name__ == "__main__":
    # main func!
    main()