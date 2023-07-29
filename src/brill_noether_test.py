from gonality import genus, gon, mfgon, setup
import sys
import copy
import csv

n = 0
graphs = []

def parse_graphs():
    global graphs

    f = open('../graphs/brill_noether_graphs.lst', 'r')
    line = 'blah'

    while line:
        graph = []
        line = f.readline()
        while line and line != '\n':
            neighbors = line[line.index(':')+1:].strip().split(' ')
            graph.append([int(x)-1 for x in neighbors])            
            line = f.readline()
        graphs.append(graph)

    f.close()

def conjecture_checking():
    parse_graphs()

    results = []

    for graph in graphs:
        setup(graph)
        g = genus()

        result = [graph, g]
        
        fgon, winning_divisor = gon(1)
        result.append("gonality: {}".format(fgon))
        result.append(winning_divisor)

        if fgon > (g + 3) / 2:
            result.append('Counterexample!')
        else:
            result.append('')

        results.append(result)

        # Things to check
        # - if gon_2(G) = gon_1(G) + 1, then g = (gon_1(G) choose 2)
        # - look for graph with smallest genus g such that gon(G) = n
        
    fields = ['Graph', 'Genus', '1st order gonality', 'Divisor', 'Counterexample?'] 

    filename = "../results/brill_noether_results.csv"
 
    with open(filename, 'w') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(fields) 
        csvwriter.writerows(results) 

if __name__ == '__main__':
    conjecture_checking()
    # lower_nodes, upper_nodes, multiplier for edges
    # test()