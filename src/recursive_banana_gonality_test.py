from recursive_banana_gonality import driver
from gonality import gon, setup
import math
import sys
import copy
import csv

n = 0
graph = []
sequences = []

def test(lower_nodes, upper_nodes, multiplier):
    for i in range(lower_nodes, upper_nodes+1):
        construct_sequences(i, 0, [-1]*(i-1), multiplier)

    for sequence in sequences:
        # graph_from_sequence(sequence)
        # print(sequence)

        graph_from_sequence(sequence)
        setup(graph)

        recursive_gon = driver(sequence)
        slow_gon, div = gon(1)

        if recursive_gon != slow_gon:
            print('FAIL', sequence, recursive_gon, slow_gon)

def construct_sequences(nodes, index, sequence, multiplier):
    if index == nodes - 1:
        if sequence[::-1] not in sequences:
            sequences.append(sequence)
        return
    
    for e in range(2, multiplier*nodes+2):
        temp_sequence = copy.deepcopy(sequence)
        temp_sequence[index] = e
        construct_sequences(nodes, index+1, temp_sequence, multiplier)

def graph_from_sequence(sequence):
    global n
    global graph

    n = len(sequence) + 1
    graph = []

    for i in range(n):
        graph.append([])

    for i in range(n-1):
        for j in range(sequence[i]):
            graph[i].append(i+1)
            graph[i+1].append(i)

if __name__ == '__main__':
    test(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))