import copy
import csv 
import sys

winning_divisor = []
graph = []
n = 0
sequences = []

'''
Runs one iteration of Dhar's burning algorithm to compute a legal firing set

v: integer label of target vertex of q-reduction
divisor: map from V \to Z
'''
def burn(v, divisor):
    visited = set()
    burnt_edges = [0]*n
    q = []
        
    visited.add(v)
    q.append(v)

    while len(q) != 0: 
        curr = q.pop()

        for node in graph[curr]:
            burnt_edges[node] += 1

            if burnt_edges[node] > divisor[node] and node not in visited:
                visited.add(node)
                q.append(node)
    

    legal_firing_set = set()
    for i in range(n):
        if i not in visited:
            legal_firing_set.add(i)
    
    return legal_firing_set

'''
Checks whether graph is simple
'''
def simple_graph():
    for u in range(n):
        if len(graph[u]) != len(set(graph[u])):
            return False
    return True

'''
Implementation of Edmond-Karp Max-Flow algorithm
'''
def edmond_karp(src, sink):
    max_flow = 0

    edmond_karp.limiting_flow = []
    edmond_karp.parent = [-1]*n
    edmond_karp.residual_capacity = []

    for i in range(n):
        edmond_karp.residual_capacity.append([])
        for j in range(n):
            edmond_karp.residual_capacity[i].append(0)

    # print(edmond_karp.residual_capacity)
    # print(graph)

    for u in range(n):
        for v in graph[u]:
            edmond_karp.residual_capacity[u][v]+=1
            # print(u,v)
            # print(edmond_karp.residual_capacity)
    

    def bfs():
        q = []
        visited = set()
        edmond_karp.limiting_flow = [n]*n

        q.append(src)
        visited.add(src)
        while len(q) != 0:
            u = q.pop()
            
            for v in range(n):
                if v not in visited and edmond_karp.residual_capacity[u][v] != 0:
                    edmond_karp.limiting_flow[v] = min(edmond_karp.limiting_flow[v], edmond_karp.residual_capacity[u][v])
                    edmond_karp.parent[v] = u
                    visited.add(v)
                    q.append(v)
                    if v == sink:
                        return 1
        
        return 0

    while bfs():
        max_flow += edmond_karp.limiting_flow[sink]

        v = sink
        u = -1
        while v!=src:
            u = edmond_karp.parent[v]
            edmond_karp.residual_capacity[u][v] -= edmond_karp.limiting_flow[sink]
            edmond_karp.residual_capacity[v][u] += edmond_karp.limiting_flow[sink]
            v = u

    return max_flow

'''
Computes lowerbound on rth-gonality
For simple graphs, delta(G) leq gon(G)
In general, min(n, lambda(G)) leq gon(G)
'''
def gonalityLowerBound():
    if simple_graph():
        min_degree = n

        for u in range(n):
            min_degree = min(min_degree, len(graph[u]))

        # print('simple graph lower bound: ', min_degree)
        return min_degree
    
    else: 
        lambda_g = 10000000
        
        for u in range(n):
            for v in range(u+1, n):
                lambda_g = min(lambda_g, edmond_karp(u,v))

        # print('multi graph lower bound: ', min(n, lambda_g))
        return min(n, lambda_g)

'''
Check whether rank of divisor is order
'''
def check_rank(divisor, order):
    if order == 1:
        return check_positive_rank(divisor)
    
    for i in range(n):
        temp_divisor = copy.deepcopy(divisor)
        temp_divisor[i] -= 1

        if not check_rank(temp_divisor, order-1):
            return False
    
    return True

'''
Checks whether rank(divisor) geq 0
'''
def check_positive_rank(divisor):
    running_divisor = copy.deepcopy(divisor)
    dp = []

    for i in range(n):
        if divisor[i] > 0:
            dp.append(1)
        else:
            dp.append(0)
        
    for i in range(n):
        while dp[i] == 0:
            firing_set = burn(i, running_divisor)
            # print('burn({}, {}): '.format(i, running_divisor), burn(i, running_divisor))
            if len(firing_set) == 0:
                return False
            
            for u in firing_set:
                for v in graph[u]:
                    running_divisor[u] -= 1
                    running_divisor[v] += 1
                
            for j in range(n):
                if running_divisor[j] > 0:
                    dp[j] = 1
    return True

'''
Finds r-gonality winning divisor with degree = chips if one exists
'''
def find_winner(chips, divisor_length, order):
    
    if divisor_length >= n:
        if order == 1:
            # print('checking divisor ', winning_divisor)
            # print('chips: ', chips)
            # print('burn(0, winning_divisor): ', burn(0, winning_divisor))
            # print('check_positive_rank(winning_divisor): ', check_positive_rank(winning_divisor))

            return chips == 0 and winning_divisor[0] > 0 and len(burn(0, winning_divisor)) == 0 and check_positive_rank(winning_divisor) 
        else:
            return chips == 0 and winning_divisor[0] > 0 and len(burn(0, winning_divisor)) == 0 and check_rank(winning_divisor, order) 
    
    stop = 0
    if divisor_length == 0:
        stop = 1

    for i in reversed(range(stop, chips+1)):
        # print(winning_divisor, divisor_length)
        winning_divisor[divisor_length] = i
        if find_winner(chips - i, divisor_length + 1, order):
            return True

    winning_divisor[divisor_length] = -1
    return False

'''
Finds r-multiplicity free gonality winning divisor with degree = chips if one exists
'''
def find_mf_winner(chips, divisor_length, order):
    if divisor_length >= n:
        if order == 1:
            # print('checking divisor ', winning_divisor)
            # print('chips: ', chips)
            # # print('burn(0, winning_divisor): ', burn(0, winning_divisor))
            # print('check_positive_rank(winning_divisor): ', check_positive_rank(winning_divisor))
            return chips == 0 and check_positive_rank(winning_divisor)
        else:
            return chips == 0 and check_rank(winning_divisor, order) 
    
    allowable_chips = 0
    if chips > 0:
        allowable_chips = 1

    for i in reversed(range(allowable_chips+1)):
        winning_divisor[divisor_length] = i
        if find_mf_winner(chips-i, divisor_length+1, order):
            return True

    winning_divisor[divisor_length] = -1
    return False

'''
Driver function for optimized gonality computation
'''
def gonality(order):
    global winning_divisor
    gon = n
    winning_divisor = [0]*n
    
    degree = gonalityLowerBound()

    while True:
        if find_winner(degree, 0, order):
            gon = degree
            break
        degree += 1

    return gon

'''
Driver function for multiplicity free gonality computation
'''
def mfgon(order):
    global winning_divisor
    gon = n
    winning_divisor = [0]*n

    degree = gonalityLowerBound()

    for i in range(degree, n+1):
        if find_mf_winner(i, 0, order):
            gon = i
            break
    
    if winning_divisor[0] < 0:
        return -1
    else:
        return gon

'''
GONALITY OF BANANA GRAPHS
'''
def test():
    sequence = [3,1,2]
    graph_from_sequence(sequence)
    # print(mfgon(1))

def genus(sequence):
    return sum(sequence) - len(sequence)

def banana_gonality(lower_nodes, upper_nodes):
    for i in range(lower_nodes, upper_nodes+1):
        construct_sequences(i, 0, [-1]*(i-1))

    results = []

    for sequence in sequences:
        graph_from_sequence(sequence)
        
        g = genus(sequence)

        result = [",".join([str(x) for x in sequence]), genus(sequence)]
        
        fgon = gonality(1)
        result.append("gonality: {}".format(fgon))
        result.append(winning_divisor)

        sgon = gonality(2)
        result.append("gonality: {}".format(sgon))
        result.append(winning_divisor)

        tgon = gonality(3)
        result.append("gonality: {}".format(tgon))
        result.append(winning_divisor)

        fmfgon = mfgon(1)
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

        results.append(result)

        # Things to check
        # - if gon_2(G) = gon_1(G) + 1, then g = (gon_1(G) choose 2)
        # - look for graph with smallest genus g such that gon(G) = n
        
    fields = ['Edge Sequence', 'Genus', '1st order gonality', 'Divisor', '2nd order gonality', 'Divisor', '3rd order gonality', 'Divisor', 'Multiplicity free gonality', 'Divisor', 'Counterexample?'] 

    filename = "banana_graphs_{}_{}.csv".format(lower_nodes, upper_nodes)
 
    with open(filename, 'w') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(fields) 
        csvwriter.writerows(results)

def construct_sequences(nodes, index, sequence):
    if index == nodes - 1:
        if sequence[::-1] not in sequences:
            sequences.append(sequence)
        return
    
    for e in range(1, nodes+1):
        temp_sequence = copy.deepcopy(sequence)
        temp_sequence[index] = e
        construct_sequences(nodes, index+1, temp_sequence)

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
    banana_gonality(int(sys.argv[1]), int(sys.argv[2]))
    # test()