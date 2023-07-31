import math
import sys
import copy
import csv

def driver(sequence):
    subgraphs = []
    queue = [sequence]
    gon = 0

    while len(queue) != 0:
        curr_sequence = queue.pop()
        if len(curr_sequence) == 0:
            gon += 1
        else:
            max_edge_count = max(curr_sequence)
            max_edge_index = curr_sequence.index(max_edge_count)

            if max_edge_count > len(curr_sequence) + 1:
                queue.append(curr_sequence[:max_edge_index])
                queue.append(curr_sequence[max_edge_index+1:])
            else:
                subgraphs.append(curr_sequence)

    # print(subgraphs)

    for sequence in subgraphs:
        dp = []
        for i in range(len(sequence)+1):
            dp.append([-1]*(len(sequence)**2 + 2))
        gon += recurrence(sequence, 0, dp)

    return gon

def recurrence(sequence, k, dp):
    n = len(sequence)

    # print(sequence, k)

    if dp[n][k] != -1: # dp cache
        # print('returning cached answer')
        return dp[n][k]

    if n == 0: # f(G, 0) when G is one vertex
        if k == 0:
            dp[n][k] = 1
            return dp[n][k]
        else:
            dp[n][k] = 0
            return dp[n][k]
    
    if k == 0:
        dp[n][k] = min(1 + recurrence(sequence[1:], 0, dp), sequence[0] + recurrence(sequence[1:], sequence[0], dp))
    else:
        dp[n][k] = min(
            recurrence(sequence[1:], sequence[0] * int(math.floor(float(k)/sequence[0])), dp), 
            sequence[0] - (k % sequence[0]) + recurrence(sequence[1:], sequence[0] * int(math.ceil(float(k)/sequence[0])), dp)
                )

    return dp[n][k]

# if __name__ == '__main__':
    # print(2/3)
    # print(driver([2,3,2]))
    
    
