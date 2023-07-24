#include "includes/gonality.h"
#include <stdio.h>
#include <cstring>
#include <iostream>
#include <fstream>
using namespace std;

vector<int*> sequences;

void construct_sequences(int n, int index, int* sequence){
     if(index == n-1){
        sequences.push_back(sequence);
     }

    for(int edges = 1; edges <=n; edges++){
        int temp_sequence[n-1];
        for(int j = 0; j < sizeof(sequence) / sizeof(int); j++){
            temp_sequence[j] = sequence[j];
        }
        temp_sequence[index] = edges;
        construct_sequences(n, index+1, temp_sequence);
    }
}

vector<vector<int>> graph(int* sequence){
    int n = sizeof(sequence) / sizeof(int) + 1;
    vector<vector<int>> graph = vector<vector<int>>();

    for(int i = 0; i < n; i++){
        graph.push_back(vector<int>());
    }

    for(int i = 0; i < n-1; i++){
        for(int j = 0; j < sequence[i]; j++){
            graph[i].push_back(i+1);
            graph[i+1].push_back(i);
        }
    }

    return graph;
}

int main(){
    ofstream MyFile("answers.txt");
    MyFile << "hello!";
    
    int nodes_start = 2;
    int nodes_end = 5;

    for(int nodes = 2; nodes_start < nodes_end; nodes++){
        int sequence[nodes];
        construct_sequences(nodes, 0, sequence);
    }

    MyFile << "Completed Sequences";

    for(int i = 0; i < sequences.size(); i++){
        printf("gonality = %d", find_gonality(graph(sequences[i]), 1));
    }

    MyFile.close();
}