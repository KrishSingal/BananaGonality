from gonality import gon, mfgon, setup
from recursive_banana_gonality import driver
import sys
import copy
import csv

sequences = []
n = 0
graph = []

def test():
    sequence = [3,1,2]
    graph_from_sequence(sequence)
    # print(mfgon(1))

def genus(sequence):
    return sum(sequence) - len(sequence)

def banana_conj(lower_nodes, upper_nodes, multiplier):
    for i in range(lower_nodes, upper_nodes+1):
        construct_sequences(i, 0, [-1]*(i-1), multiplier)

    # Things to check
    # - if gon_2(G) = gon_1(G) + 1, then g = (gon_1(G) choose 2)
    # - look for graph with smallest genus g such that gon(G) = n
        
    fields = ['Edge Sequence', 'Genus', '1st order gonality', 'Divisor', '2nd order gonality', 'Divisor', '3rd order gonality', 'Divisor', 'Multiplicty free gonality', 'Divisor', 'Counterexample?']

    filename = "../results/banana_conj_{}_{}_{}.csv".format(lower_nodes, upper_nodes, multiplier)
 
    with open(filename, 'w') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(fields) 

        for sequence in sequences:
            graph_from_sequence(sequence)
            
            g = genus(sequence)

            result = [",".join([str(x) for x in sequence]), genus(sequence)]
            
            setup(graph)

            fgon, winning_divisor = gon(1)
            result.append("gonality: {}".format(fgon))
            result.append(winning_divisor)

            sgon, winning_divisor = gon(2)
            result.append("gonality: {}".format(sgon))
            result.append(winning_divisor)

            tgon, winning_divisor = gon(3)
            result.append("gonality: {}".format(tgon))
            result.append(winning_divisor)

            fmfgon, winning_divisor = mfgon(1)
            result.append("gonality: {}".format(fmfgon))
            result.append(winning_divisor)

            if sgon == fgon + 1:
                result[0] += '(*)'
                if g != fgon * (fgon-1) / 2:
                    result.append('Counterexample to g = (gon_1(G) choose 2)!')
                elif fgon >=2 and tgon != 2*fgon:
                    result.append('Counterexample to gon_3(G) = 2gon_1(G)!')
            else:
                result.append('')

            csvwriter.writerow(result)

def banana_gonality(lower_nodes, upper_nodes, multiplier):
    for i in range(lower_nodes, upper_nodes+1):
        construct_sequences(i, 0, [-1]*(i-1), multiplier)

    # Things to check
    # - if gon_2(G) = gon_1(G) + 1, then g = (gon_1(G) choose 2)
    # - look for graph with smallest genus g such that gon(G) = n
    
    fields = ['Edge Sequence', 'Genus', '1st order gonality', 'Divisor']

    filename = "../results/banana_gonality_{}_{}_{}.csv".format(lower_nodes, upper_nodes, multiplier)
 
    with open(filename, 'w') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(fields) 

        for sequence in sequences:
            graph_from_sequence(sequence)
            
            g = genus(sequence)

            result = [",".join([str(x) for x in sequence]), genus(sequence)]
            
            setup(graph)

            fgon, winning_divisor = gon(1)
            result.append("gonality: {}".format(fgon))
            result.append(winning_divisor)

            csvwriter.writerow(result)

def recursive_banana_gon(lower_nodes, upper_nodes, multiplier):
    for i in range(lower_nodes, upper_nodes+1):
        construct_sequences(i, 0, [-1]*(i-1), multiplier)

    fields = ['Edge Sequence', 'Genus', '1st order gonality']

    filename = "../results/recursive_banana_gonality_{}_{}_{}.csv".format(lower_nodes, upper_nodes, multiplier)
 
    with open(filename, 'w') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(fields) 

        for sequence in sequences:
            result = [",".join([str(x) for x in sequence]), genus(sequence)]

            fgon = driver(sequence)
            result.append("gonality: {}".format(fgon))

            csvwriter.writerow(result)

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
    if sys.argv[4] == 'conj':
        banana_conj(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    elif sys.argv[4] == 'gon':
        banana_gonality(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    elif sys.argv[4] == 'recursive':
        recursive_banana_gon(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    
    # lower_nodes, upper_nodes, multiplier for edges
    # test()