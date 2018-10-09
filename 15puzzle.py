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
    global memory
    global memorylist

    memory = set()
    memorylist = []

    filename = "16puzzle.txt"
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    goal = "0ABCDEFGHIJKLMNO"
    sum_time = 0
    count = 0
    size = 4

    # state = "A0BCDEFGHIJKLMNO" #lines[20].split(" ")[0].replace("\n", "")
    # print("%s" % taxicab_dist(state, goal))
    # print("left   %s" % taxicab_dist(left(state), goal))
    # print("right  %s" % taxicab_dist(right(state), goal))
    # print("up     %s" % taxicab_dist(up(state), goal))
    # print("down   %s" % taxicab_dist(down(state), goal))
    #
    # print("")
    #
    # state = "DABC0EFGHIJKLMNO" #lines[21].split(" ")[0].replace("\n", "")
    # print("%s" % taxicab_dist(state, goal))
    # print("left   %s" % taxicab_dist(left(state), goal))
    # print("right  %s" % taxicab_dist(right(state), goal))
    # print("up     %s" % taxicab_dist(up(state), goal))
    # print("down   %s" % taxicab_dist(down(state), goal))
    #
    # print("")
    #
    # state = lines[22].split(" ")[0].replace("\n", "")
    # print("%s" % taxicab_dist(state, goal))
    # print("left   %s" % taxicab_dist(left(state), goal))
    # print("right  %s" % taxicab_dist(right(state), goal))
    # print("up     %s" % taxicab_dist(up(state), goal))
    # print("down   %s" % taxicab_dist(down(state), goal))

    for line in lines:
        sep = line.split(" ")
        size = 4
        state = sep[0].replace("\n", "")

        print("%s: (%s)" % (state, count))



        # try:
        #     start = time.process_time()
        #     path = solve_bfs_original(state)
        #     end = time.process_time()
        #     sum_time = sum_time + (end - start)
        #     print("\tBFS \t%s \t%s" % (len(path), end - start))
        # except MemoryError:
        #     print("\tBFS Memory Error")

        try:
            start = time.process_time()
            path = a_star_taxi(state)
            end = time.process_time()
            sum_time = sum_time + (end - start)
            print("\tA-STAR \t\t%s \t%s" % (path, round(end - start, 5)))
        except MemoryError:
            print("\tA Star")


        # try:
        #     start = time.process_time()
        #     path = solve_bfs_original(state)
        #     end = time.process_time()
        #     sum_time = sum_time + (end - start)
        #     print("\tBFS \t%s \t%s" % (len(path), round(end - start, 5)))
        # except MemoryError:
        #     print("\tBFS Memory Error")


        # start = time.process_time()
        # path = solve_bfs_zoom_heap(state)
        # end = time.process_time()
        # sum_time = sum_time + (end - start)
        # print("\tBZH \t%s \t%s" % (path, end - start))


        # start = time.process_time()
        # path = id_dfs(state, count+3)
        # end = time.process_time()
        # sum_time = sum_time + (end - start)
        # print("\tID_DFS \t%s \t%s" % (len(path), round(end - start, 5)))

        count += 1


    # size = 4
    # start = lines[16].split(" ")[0].replace("\n", "")
    # print(id_bfs(start, 19))

    print("Total Time: %s" % round(sum_time, 5))


def a_star(state):
    fringe_top = [(taxicab_dist(state, goal)+0, state, 0)]
    visited_top = set()

    # if parity_check(state) == 1:
    #     return -1

    while len(fringe_top) is not 0:
        vt = heappop(fringe_top)  # your standard BFS algorithm

        if vt[1] not in visited_top:
            visited_top.add(vt[1])
        else:
            continue

        if goal_test(vt[1]):
            return vt[2]

        children = get_children(vt[1])
        for child in children.keys():
            if child not in visited_top:
                heappush(fringe_top, ((vt[2]+1+taxicab_dist(child, goal)), child, vt[2]+1))
        # visited_top.add(vt[1])

    if len(fringe_top) is 0:
        return -2


def a_star_taxi(state):
    fringe_top = [(taxicab_dist(state, goal)+0, state, 0)]
    visited_top = set()

    # if parity_check(state) == 1:
    #     return -1

    while len(fringe_top) is not 0:
        vt = heappop(fringe_top)  # your standard BFS algorithm

        if vt[1] not in visited_top:
            visited_top.add(vt[1])
        else:
            continue

        if goal_test(vt[1]):
            return vt[2]

        children = get_children_taxi(vt[1])
        for child in children.keys():
            if child not in visited_top:
                a = (vt[2]+1+taxicab_dist(child, goal))
                b = (vt[2]+1+vt[0]+children.get(child))
                heappush(fringe_top, ((vt[2]+1+vt[0]+children.get(child)), child, vt[2]+1))
        # visited_top.add(vt[1])

    if len(fringe_top) is 0:
        return -2


def a_star_random(state):
    fringe_top = [(taxicab_dist(state, goal) + 0, random.randint(1, 1000), state, 0), ]
    visited_top = set()

    # if parity_check(state) == 1:
    #     return -1

    while len(fringe_top) is not 0:
        vt = heappop(fringe_top)  # your standard BFS algorithm

        if vt[2] not in visited_top:
            visited_top.add(vt[2])
        else:
            continue

        if goal_test(vt[2]):
            return vt[3]
        children = get_children(vt[2])
        for child in children.keys():
            if child not in visited_top:
                heappush(fringe_top, ((vt[3] + 1 + taxicab_dist(child, goal)), random.randint(1, 1000), child, vt[3] + 1))
        visited_top.add(vt[2])

    if len(fringe_top) is 0:
        return -2


def solve_kdfs_heap(start, k):
    fringe = [(taxicab_dist(start, goal), start, 0, {start, }, ""), ]
    while len(fringe) is not 0:
        v = heappop(fringe)
        if goal_test(v[1]):
            return v
        if v[2] < k:
            children = get_children(v[1])
            for child in children:
                if child not in v[3]:
                    a = set(v[3])
                    a.add(child)
                    heappush(fringe, (taxicab_dist(child, goal), child, v[2] + 1, a, v[4]+children.get(child)))
    return None


def solve_kdfs(start, k):
    fringe = deque()
    fringe.append((start, 0, {start, }, ""))
    while len(fringe) is not 0:
        v = fringe.pop()
        if goal_test(v[0]):
            return v[3]
        if v[1] <= k:
            children = get_children(v[0])
            for child in children:
                if child not in v[2]:
                    a = set(v[2])
                    a.add(child)
                    fringe.append((child, v[1] + 1, a, v[3] + children.get(child)))
    return None


def id_dfs(start, max):
    for k in range(taxicab_dist(start, goal), max+3):
        sol = solve_kdfs(start, k)
        if sol is not None:
            return sol
    return None


def id_dfs_heap(start, max):
    for k in range(1, max):
        sol = solve_kdfs_heap(start, k)
        if sol is not None:
            return sol
    return None


def solve_kbfs_cab(state, k):
    start_state = state
    fringe_top = [(taxicab_dist(state, goal), state, 0), ]
    visited_top = {state, }
    fringe_top_next = []
    fringe_t = {state, }
    done = False
    count = 0

    if parity_check(state) == 1:  #
        return -1  # if parity determines its not solveable

    while not done:
        while len(fringe_top) is not 0:
            vt = heappop(fringe_top)  # your standard BFS algorithm
            if goal_test(vt[1]):
                return vt[2]
            children = get_children(vt[1])
            for child in children.keys():
                if child not in visited_top:
                    # fringe_top.append((taxicab_dist(child, goal), child, vb[2]+1))
                    heappush(fringe_top_next, (taxicab_dist(child, goal), child, vt[2] + 1))
                    visited_top.add(child)
        if count >= k:
            done = True
        else:
            count += 1
            fringe_top = list(fringe_top_next)

    if len(fringe_top) is 0:
        return None


def id_bfs(start, max):
    for k in range(taxicab_dist(start, goal), max):
        sol = solve_kbfs_zoom_cab(start, k)
        if sol is not None:
            return sol
    if max == 0:
        return ""
    return None


def solve_kbfs_zoom_cab(state, k):
    start_state = state
    fringe_top = [(taxicab_dist(state, goal), state, 0), ]
    fringe_bottom = [(taxicab_dist(goal, state), goal, 0), ]
    visited_top = {state, }
    visited_bottom = {goal, }
    fringe_top_next = []
    fringe_bottom_next = []
    fringe_t = {state, }
    done = False
    count = -1

    if parity_check(state) == 1:  #
        return -1  # if parity determines its not solveable

    while not done:
        while len(fringe_top) is not 0 and len(fringe_bottom) is not 0:
            vt = heappop(fringe_top)  # your standard BFS algorithm
            vb = heappop(fringe_bottom)
            if vb[1] in visited_top:
                for s in fringe_top:
                    if s[1] == vb[1]:
                        #if s[2] + vb[2] < k:
                        return s[2] + vb[2]
            if goal_test(vt[1]):
                return vt[2]
            children = get_children(vt[1])
            for child in children.keys():
                if child not in visited_top:
                    # fringe_top.append((taxicab_dist(child, goal), child, vb[2]+1))
                    heappush(fringe_top_next, (taxicab_dist(child, goal), child, vt[2] + 1))
                    visited_top.add(child)
            children = get_children(vb[1])
            for child in children.keys():
                if child not in visited_bottom:
                    # fringe_bottom.append((taxicab_dist(child, state), child, vb[2] + 1))
                    heappush(fringe_bottom_next, (taxicab_dist(child, state), child, vb[2] + 1))
                    visited_bottom.add(child)
        if count >= k:
            done = True
        else:
            count += 1
            fringe_bottom = list(fringe_bottom_next)
            fringe_top = list(fringe_top_next)

    if len(fringe_top) is 0 and len(fringe_bottom) is 0:
        return None


def solve_bfs_original(state):
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
            return str(v[1])
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
        vt = fringe_top.pop()  # your standard BFS algorithm
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


def solve_bfs_zoom_heap(state):
    # finds the path to the goal state from a given state using a breadth first search algorithm
    start_state = state
    fringe_top = [(taxicab_dist(state, goal), state, 0), ]
    fringe_bottom = [(taxicab_dist(goal, state), goal, 0), ]
    visited_top = {state, }
    visited_bottom = {goal, }
    fringe_t = {state, }

    if parity_check(state) == 1:   #
        return -1                 # if parity determines its not solveable

    while len(fringe_top) is not 0 and len(fringe_bottom) is not 0:
        vt = heappop(fringe_top)  # your standard BFS algorithm
        vb = heappop(fringe_bottom)
        if vb[1] in visited_top:
            for s in fringe_top:
                if s[1] == vb[1]:
                    return s[2] + vb[2]
        if goal_test(vt[1]):
            return vt[2]
        children = get_children(vt[1])
        for child in children.keys():
            if child not in visited_top:
                heappush(fringe_top, (taxicab_dist(child, goal), child, vt[2]+1))
                visited_top.add(child)
        children = get_children(vb[1])
        for child in children.keys():
            if child not in visited_bottom:
                heappush(fringe_bottom, (taxicab_dist(child, state), child, vb[2] + 1))
                # fringe_bottom.appendleft((child, vb[1]+1))
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


def taxicab_dist(state, aim):
    summ = 0
    for char in state:
        if char is not "0":
            ai = aim.index(char)
            ci = state.index(char)
            y_goal = int(ai / size)
            x_goal = int(ai % size)
            y_cur = int(ci / size)
            x_cur = int(ci % size)
            summ += abs(y_goal-y_cur) + abs(x_goal-x_cur)
    return summ


def random_state():
    # generates a random state by shuffling the string "012345678"
    return ''.join(random.sample("012345678", 9))


def random_solvable():
    # generates a random but solvable state
    state = random_state()   # random state
    while (parity_check(state)) is 1:   # while it's not solvable
        state = random_state()          # shuffle again
    return state


def get_children(state):
    # returns a dictionary of the children from a state, each child's value being the move direction used to get there
    # children = {up(state): "1", right(state): "2", down(state): "3", left(state): "4"}
    children = {up(state): "1", right(state): "2", down(state): "3", left(state): "4"}
    # children.pop(state, None)  # removes states that are the same as the original (i.e. if "moved up" from top row)
    return children


def get_children_taxi(state):
    # returns a dictionary of the children from a state, each child's value being the move direction used to get there
    # find the one it swaps with
    # calculate how far it should be from that

    children = dict()
    o = state.index("0")
    ox = state.index("0") % size
    oy = int(state.index("0") / size)
    # left:
    if ox-1 >= 0:
        current_char = state[ox-1]
        goal_x = goal.index(current_char)
        if goal_x < ox-1:
            children[left(state)] = -1
        else:
            children[left(state)] = 1
    else:
        children[left(state)] = 0

    # right:
    if ox+1 <= len(state)-1:
        current_char = state[ox+1]
        goal_x = goal.index(current_char)
        if goal_x > ox+1:
            children[right(state)] = -1
        else:
            children[right(state)] = 1
    else:
        children[right(state)] = 0

    # up:
    if oy-size >= 0:
        current_char = state[oy-size]
        goal_y = goal.index(current_char)
        if goal_y < oy-size:
            children[up(state)] = -1
        else:
            children[up(state)] = 1
    else:
        children[up(state)] = 0

    # down:
    if oy+size <= len(state)-1:
        current_char = state[oy+size]
        goal_y = goal.index(current_char)
        if goal_y > oy+size:
            children[down(state)] = -1
        else:
            children[down(state)] = 1
    else:
        children[down(state)] = 0



    # children = dict()
    # i = state.index("0")
    # iy = int(state.index("0") / size)
    # ix = state.index("0") % size
    # li = i-1
    # ri = i+1
    # ui = i-size
    # di = i+size
    # if iy != 0: #UP
    #     uc = state[ui]
    #     g = goal.index(uc)
    #     gy = int(g/size)
    #     gx = g%size
    #     cy = int(ui/size) - 1
    #     cx = ui%size
    #     if gy < cy:
    #         children[up(state)] = -1
    #     elif gy > cy:
    #         children[up(state)] = 1
    #     else:
    #         children[up(state)] = 0
    # else:
    #     children[up(state)] = 0
    #
    # if iy != size-1:
    #     dc = state[di]
    #     g = goal.index(dc)
    #     gy = int(g / size)
    #     gx = g % size
    #     cy = int(di / size) + 1
    #     cx = di % size
    #     if gy > cy:
    #         children[down(state)] = -1
    #     elif gy < cy:
    #         children[down(state)] = 1
    #     else:
    #         children[down(state)] = 0
    # else:
    #     children[down(state)] = 0
    #
    # if (ix+1) < 0:
    #     lc = state[li]
    #     g = goal.index(lc)
    #     gy = int(g / size)
    #     gx = g % size
    #     cy = int(li / size)
    #     cx = li % size + 1
    #     if gx > cx:
    #         children[left(state)] = -1
    #     elif gx < cx:
    #         children[left(state)] = 1
    #     else:
    #         children[left(state)] = 0
    # else:
    #     children[left(state)] = 0
    #
    # if ix > size-1:
    #     rc = state[ri]
    #     g = goal.index(rc)
    #     gy = int(g / size)
    #     gx = g % size
    #     cy = int(ri / size)
    #     cx = ri % size - 1
    #     if gx < cx:
    #         children[right(state)] = -1
    #     elif gx > cx:
    #         children[right(state)] = 1
    #     else:
    #         children[right(state)] = 0
    # else:
    #     children[right(state)] = 0



    # children = set()
    # if iy > 0 and ix > 0:
    #     children = {up(state): -1, right(state): 1, down(state): 1, left(state): -1}
    # elif iy > 0 and ix == 0:
    #     children = {up(state): -1, right(state): 1, down(state): 1, left(state): 0}
    # elif iy == 0 and ix > 0:
    #     children = {up(state): 0, right(state): 1, down(state): 1, left(state): -1}
    # else:
    #     children = {up(state): 0, right(state): 1, down(state): 1, left(state): 0}
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


