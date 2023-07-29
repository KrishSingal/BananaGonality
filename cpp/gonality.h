#include <cassert>
#include <queue>
#include <stdio.h>
using namespace std;

int burn(vector<vector<int>> graph, const int* divisor, const int start);

bool check_rank(vector<vector<int>> graph, const int* divisor, int order);

bool has_positive_rank(vector<vector<int>> graph, const int* divisor);

bool find_positive_rank_divisor(vector<vector<int>> graph, const int remaining_chips, const int finished_vertices, int order);

int find_gonality(vector<vector<int>> graph, int order);
