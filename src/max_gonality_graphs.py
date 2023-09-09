from recursive_banana_gonality import driver
import sys
import copy
import csv
import math

def find_all_max_graphs():
    prefixes = [[2], [3], [4], [2,2], [2,3], [2,4]]

    q = [[], [2], [3]]
    max_graphs = [[], [2], [3]]
    visited = [[], [2], [3]]

    while len(q) != 0:
        curr_sequence = q.pop(0)

        for prefix in prefixes:
            new_sequence = prefix + curr_sequence
            print("curr_sequence: ", curr_sequence)
            print("considering new sequence: ", new_sequence)
            if new_sequence not in visited:
                visited.append(new_sequence)
                gon = driver(new_sequence)
                genus = sum(new_sequence) - len(new_sequence)
                if gon == math.floor((genus+3)/2):
                    print("max sequence: ", new_sequence)
                    q.append(new_sequence)
                    max_graphs.append(new_sequence)

    return max_graphs
        
if __name__ == '__main__':
    mg = find_all_max_graphs()
    for seq in mg:
        print(",".join([str(x) for x in seq]))
