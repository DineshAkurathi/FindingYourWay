import random
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt


class GlobalVar:
    rows = 0
    columns = 0
    grid = []
    drone_index = None
    probability_grid = []
    is_drone_found = False
    move_count = 0


def create_environment():
    with open('Thor23-SA74-VERW-Schematic (Classified).txt') as f:
        i = 0
        count = 0
        a = {}
        for line in f:
            if line != '\n':
                count += 1
                a[i] = line
                i = i + 1
    # Getting the row count
    GlobalVar.rows = count
    # Getting the column count
    GlobalVar.columns = len(a[0]) - 1
    for i in range(0, GlobalVar.rows):
        colm = []
        for j in range(0, GlobalVar.columns):
            t = []
            if a[i][j] == 'X':
                # 0 for Blocked cells
                t = 0
            elif a[i][j] == '_':
                # 1 for unblocked cells
                t = 1
            colm.append(t)
        GlobalVar.grid.append(colm)
    # Printing Grid
    for i in range(0, GlobalVar.rows):
        print(GlobalVar.grid[i])


def create_drone():
    """This function will randomly generate a drone anywhere in the reactor core"""
    # Creating a list to store all the possible drone locations
    available_locations = []
    for row in range(0, GlobalVar.rows):
        for column in range(0, GlobalVar.columns):
            if GlobalVar.grid[row][column] == 1:
                available_locations.append([row, column])
    # print(available_locations)
    location = random.choice(available_locations)
    GlobalVar.drone_index = location
    return location


def calculate_probability():
    """This function is to calculate the probability of each location after n no of iterations"""
    no_of_iterations = 1000
    temp_grid = []
    # Initialising the grid
    for row in range(0, GlobalVar.rows):
        temp_colm = []
        for column in range(0, GlobalVar.columns):
            temp_colm.append(0)
        temp_grid.append(temp_colm)
    while no_of_iterations > 0:
        drone_location = create_drone()
        drone_row = drone_location[0]
        drone_column = drone_location[1]
        temp_grid[drone_row][drone_column] += 1
        no_of_iterations = no_of_iterations - 1
    # Printing Grid
    for row in range(0, GlobalVar.rows):
        print(temp_grid[row])


def initiating_probability_grid():
    """This function will create a probability grid"""
    # Creating a list to store all the possible drone locations to estimate the probability
    available_locations = []
    for row in range(0, GlobalVar.rows):
        for column in range(0, GlobalVar.columns):
            if GlobalVar.grid[row][column] == 1:
                available_locations.append([row, column])
    for i in range(0, GlobalVar.rows):
        colm = []
        for j in range(0, GlobalVar.columns):
            if [i, j] in available_locations:
                probability = 1 / len(available_locations)
                colm.append(probability)
            else:
                colm.append(0)
        GlobalVar.probability_grid.append(colm)
    # Printing Grid
    print("Printing the actual probability grid")
    for row in range(0, GlobalVar.rows):
        print(GlobalVar.probability_grid[row])


def probability_move(command):
    """This function moves the probabilities of each cell when a command is applied"""
    # Initialising a transition grid to calculate the updated probabilities
    transition_grid = []
    heuristic = 0
    # setting every value to zero initially
    for row in range(0, GlobalVar.rows):
        colm = []
        for column in range(0, GlobalVar.columns):
            colm.append(0)
        transition_grid.append(colm)
    # For Right command:
    for row in range(0, GlobalVar.rows):
        for column in range(0, GlobalVar.columns):
            prev_probability = GlobalVar.probability_grid[row][column]
            new_row = 0
            new_column = 0
            if command == 'right':
                # checking if it is in the border or a wall in front
                if column == GlobalVar.columns - 1 or GlobalVar.grid[row][column + 1] == 0:
                    new_row = row
                    new_column = column
                else:
                    new_row = row
                    new_column = column + 1
            elif command == 'left':
                # checking if it is in the border or a wall in back
                if column == 0 or GlobalVar.grid[row][column - 1] == 0:
                    new_row = row
                    new_column = column
                else:
                    new_row = row
                    new_column = column - 1
            elif command == 'up':
                # checking if it is in the border or a wall on top
                if row == 0 or GlobalVar.grid[row - 1][column] == 0:
                    new_row = row
                    new_column = column
                else:
                    new_row = row - 1
                    new_column = column
            elif command == 'down':
                # checking if it is in the border or a wall on bottom
                if row == GlobalVar.rows - 1 or GlobalVar.grid[row + 1][column] == 0:
                    new_row = row
                    new_column = column
                else:
                    new_row = row + 1
                    new_column = column
            transition_grid[new_row][new_column] = transition_grid[new_row][new_column] + prev_probability
    # Verifying the transitioned probabilities
    count = 0
    print('printing the transitioned grid')
    for row in range(0, GlobalVar.rows):
        print(transition_grid[row])
        for column in range(0, GlobalVar.columns):
            count = count + transition_grid[row][column]
    # Updating probability grid as transition grid
    GlobalVar.probability_grid = transition_grid
    print('Total probability after transition: ', end=" ")
    print(count)
    return heuristic


def probability_move_simulator(command):
    """This function moves the probabilities of each cell when a command is applied"""
    # Initialising a transition grid to calculate the updated probabilities
    transition_grid = []
    heuristic = 0
    # setting every value to zero initially
    for row in range(0, GlobalVar.rows):
        colm = []
        for column in range(0, GlobalVar.columns):
            colm.append(0)
        transition_grid.append(colm)
    # For Right command:
    for row in range(0, GlobalVar.rows):
        for column in range(0, GlobalVar.columns):
            prev_probability = GlobalVar.probability_grid[row][column]
            new_row = 0
            new_column = 0
            if command == 'right':
                # checking if it is in the border or a wall in front
                if column == GlobalVar.columns - 1 or GlobalVar.grid[row][column + 1] == 0:
                    new_row = row
                    new_column = column
                else:
                    new_row = row
                    new_column = column + 1
            elif command == 'left':
                # checking if it is in the border or a wall in back
                if column == 0 or GlobalVar.grid[row][column - 1] == 0:
                    new_row = row
                    new_column = column
                else:
                    new_row = row
                    new_column = column - 1
            elif command == 'up':
                # checking if it is in the border or a wall on top
                if row == 0 or GlobalVar.grid[row - 1][column] == 0:
                    new_row = row
                    new_column = column
                else:
                    new_row = row - 1
                    new_column = column
            elif command == 'down':
                # checking if it is in the border or a wall on bottom
                if row == GlobalVar.rows - 1 or GlobalVar.grid[row + 1][column] == 0:
                    new_row = row
                    new_column = column
                else:
                    new_row = row + 1
                    new_column = column
            transition_grid[new_row][new_column] = transition_grid[new_row][new_column] + prev_probability
    # Calculating the heuristic value
    for row in range(0, GlobalVar.rows):
        for column in range(0, GlobalVar.columns):
            if transition_grid[row][column] > 0:
                heuristic += 1
    return heuristic


def neighbour_list(node):
    """This function gives the list of neighbours of the given index"""
    # Initialising neighbour list
    n_list = []
    # print(node)
    row = int(node[0])
    column = int(node[1])
    if column != GlobalVar.columns - 1 and GlobalVar.grid[row][column + 1] != 0:
        # Checking right and adding it to neighbour list
        n_list.append([row, column + 1])
    if column != 0 and GlobalVar.grid[row][column - 1] != 0:
        # Checking left and adding it to neighbour list
        n_list.append([row, column - 1])
    if row != GlobalVar.rows - 1 and GlobalVar.grid[row + 1][column] != 0:
        # Checking down and adding it to neighbour list
        n_list.append([row + 1, column])
    if row != 0 and GlobalVar.grid[row - 1][column] != 0:
        # Checking up and adding it to neighbour list
        n_list.append([row - 1, column])
    return n_list


def a_star_path_new(index, goal):
    """This A star path calculates the priority queue and moves to the shortest node"""
    a_star_queue = [index]
    visited_indexes = []
    while a_star_queue:
        queue_element = a_star_queue.pop()
        visited_indexes.append(queue_element)
        list_of_neighbours = neighbour_list(queue_element)
        # Initialising cost dictionary
        costs = {}
        movement = None
        # Initialising shortest neighbour
        shortest_neighbour = list_of_neighbours[0]
        # Calculating the costs for each neighbour
        for neighbour in list_of_neighbours:
            if queue_element[0] - neighbour[0] > 0:
                movement = 'up'
            elif queue_element[0] - neighbour[0] < 0:
                movement = 'down'
            elif queue_element[1] - neighbour[1] > 0:
                movement = 'left'
            elif queue_element[1] - neighbour[1] < 0:
                movement = 'right'
            temp = (neighbour[0], neighbour[1])
            costs[temp] = probability_move_simulator(movement)
        for neighbour in list_of_neighbours:
            if neighbour not in a_star_queue and neighbour not in visited_indexes:
                f_shortest = GlobalVar.rows - shortest_neighbour[0] + GlobalVar.columns - shortest_neighbour[1] - 4
                f_current = GlobalVar.rows - neighbour[0] + GlobalVar.columns - neighbour[1] - 4
                temp = (neighbour[0], neighbour[1])
                h_shortest = f_shortest - costs[temp]
                h_current = f_current - costs[temp]
                if h_current > h_shortest:
                    shortest_neighbour = neighbour
                if shortest_neighbour not in a_star_queue:
                    a_star_queue.append(shortest_neighbour)
        if queue_element == goal:
            return visited_indexes


def find_my_drone():
    """This function will find the drone in least possible steps"""
    # possible_list = []
    probability_array = np.array(GlobalVar.probability_grid)
    current_max = probability_array.max()
    # Finding two indices with high probability
    # Initialising probabilities dictionary
    probabilities_dictionary = {}
    # copying the probabilities dictionary
    for row in range(0, GlobalVar.rows):
        for column in range(0, GlobalVar.columns):
            if GlobalVar.grid[row][column] == 1:
                probability = GlobalVar.probability_grid[row][column]
                probabilities_dictionary[(row, column)] = probability
    # Most common probabilities are taken
    probabilities = Counter(probabilities_dictionary)
    highest_indexes = probabilities.most_common(2)
    from_index = highest_indexes[0][0]
    to_index = highest_indexes[1][0]
    from_index_row = from_index[0]
    from_index_column = from_index[1]
    to_index_row = to_index[0]
    to_index_column = to_index[1]
    # Finding the shortest path
    current_path = a_star_path_new([from_index_row, from_index_column], [to_index_row, to_index_column])
    print('current path : ', current_path)
    # getting the from and to indexes from path for following the path
    from_index = current_path.pop(0)
    to_index = current_path.pop(0)
    # Executing a move command
    movement = None
    if from_index[0] - to_index[0] > 0:
        movement = 'up'
    elif from_index[0] - to_index[0] < 0:
        movement = 'down'
    elif from_index[1] - to_index[1] > 0:
        movement = 'left'
    elif from_index[1] - to_index[1] < 0:
        movement = 'right'
    probability_move(movement)
    # Incrementing the move count
    GlobalVar.move_count += 1
    while GlobalVar.is_drone_found is False:
        # Initialising probabilities dictionary
        probabilities_dictionary = {}
        new_max_probability = current_max
        for row in range(0, GlobalVar.rows):
            for column in range(0, GlobalVar.columns):
                if GlobalVar.grid[row][column] == 1:
                    probability = GlobalVar.probability_grid[row][column]
                    probabilities_dictionary[(row, column)] = probability
                    # Calculating the new max probability
                    if probability > new_max_probability:
                        new_max_probability = probability
        # If there is a new maximum probability
        if new_max_probability > current_max or len(current_path) == 0:
            print('Calculating new path !!!')
            # Changing the path
            current_max = new_max_probability
            # Finding the new high probabilities
            probabilities = Counter(probabilities_dictionary)
            highest_indexes = probabilities.most_common(2)
            from_index = highest_indexes[0][0]
            to_index = highest_indexes[1][0]
            from_index_row = from_index[0]
            from_index_column = from_index[1]
            to_index_row = to_index[0]
            to_index_column = to_index[1]
            # Generating a new path
            # Finding the new shortest path
            new_path = a_star_path([from_index_row, from_index_column], [to_index_row, to_index_column])
            print('new path :', new_path)
            # getting the from and to indexes from path for following the path
            from_index = new_path.pop(0)
            to_index = new_path.pop(0)
            # Adding the remaining new path to current path
            current_path = new_path
            # Checking which direction to move and moving in that direction
            movement = None
            if from_index[0] - to_index[0] > 0:
                movement = 'up'
            elif from_index[0] - to_index[0] < 0:
                movement = 'down'
            elif from_index[1] - to_index[1] > 0:
                movement = 'left'
            elif from_index[1] - to_index[1] < 0:
                movement = 'right'
            probability_move(movement)
            # Incrementing the move count
            GlobalVar.move_count += 1
        else:
            print('using the same path !!!')
            from_index = to_index
            to_index = current_path.pop(0)
            print('From index, to index')
            print(from_index, to_index)
            # Checking which direction to move and moving in that direction
            movement = None
            if from_index[0] - to_index[0] > 0:
                movement = 'up'
            elif from_index[0] - to_index[0] < 0:
                movement = 'down'
            elif from_index[1] - to_index[1] > 0:
                movement = 'left'
            elif from_index[1] - to_index[1] < 0:
                movement = 'right'
            print(movement)
            probability_move(movement)
            # Incrementing the move count
            GlobalVar.move_count += 1
        # Checking the termination criteria
        for row in range(0, GlobalVar.rows):
            for column in range(0, GlobalVar.columns):
                # Checking if any indexes are sure
                if GlobalVar.probability_grid[row][column] >= 0.89:
                    print('Drone is at: ', end=" ")
                    print(row, column)
                    print(GlobalVar.move_count)
                    GlobalVar.is_drone_found = True
                    break
        print('Printing probability grid')
        for row in range(0, GlobalVar.rows):
            print(GlobalVar.probability_grid[row])


create_environment()
create_drone()
print('Current drone index', end=" ")
print(GlobalVar.drone_index)
# plt.imshow(GlobalVar.grid, cmap='')
initiating_probability_grid()
# probability_move('right')
# probability_move('right')
# probability_move('right')
# probability_move('down')
find_my_drone()
