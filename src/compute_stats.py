import sys
import csv
import matplotlib.pyplot as plt
import numpy as np
import math

results_per_n = dict()
min_genus_gon_n = dict()

def compute(files, max_nodes):
    results_per_n[max_nodes+1] = []
    for file in files:
        with open(file) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0][0] == 'E':
                    continue
                seq_len = (len(row[0]) + 1) // 2
                # print(row)
                # print(seq_len)
                n = seq_len + 1
                genus = int(row[1])
                gonality = int(row[2].split(':')[1])

                if n not in results_per_n:
                    results_per_n[n] = [gonality]
                    min_genus_gon_n[n] = n**3
                else:
                    results_per_n[n].append(gonality)

                if gonality > math.floor( float(genus + 3) / 2):
                    print('counterexample!')
                    print(row)
                if gonality == n and genus < min_genus_gon_n[n]:
                    min_genus_gon_n[n] = genus

                results_per_n[max_nodes+1].append(gonality)
                
                # enter into dict based on length
                    # expected gonality
                    # expected genus
                    # histogram
                # check gonality conjecture
                # check for lowest genus with gonality n
def draw(max_nodes):
    for key in results_per_n:
        # print(key, list(range(key)))
        # print(results_per_n[key])

        bins = np.arange(0, min(key, max_nodes) + 1.5) - 0.5

        # then you plot away
        fig, ax = plt.subplots()
        values, bins, bars = ax.hist(results_per_n[key], bins)
        ax.set_xticks(bins + 0.5)

        # plt.hist(results_per_n[key], bins=list(range(key)))
        plt.bar_label(bars)
        plt.text(0, len(results_per_n[key])/2, 'Mean: {}'.format(round(np.mean(results_per_n[key]), 3), fontsize = 10) )
        plt.xlabel('Gonality')
        plt.ylabel('Number of Graphs')

        nodes = ''
        if key > max_nodes:
            nodes = '2-{}'.format(max_nodes)
        else:
            nodes = '{}'.format(key)

        plt.title('Banana Graphs on {} Nodes'.format(nodes))
        
        plt.savefig('../stats/{}-node-results.png'.format(nodes))
        plt.close()

if __name__ == '__main__':
    files = ['../results/recursive_banana_gonality_2_8_1.csv']
    compute(files, 8)
    draw(8)

