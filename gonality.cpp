// This header defines all divisor-related functions, and as such constitutes the core of our program.
// 
// This file defines the following functions:
// 
//      * int burn(const my_graph& G, const int* divisor, const int start)
//        Dhar's burning algorithm.
//      
//      * bool is_reduced(const my_graph& G, const int* divisor, const int target = -1)
//        Test whether a divisor is reduced with respect to a given vertex or with respect to any vertex.
//	
//	* void reduce(const my_graph& G, const int* divisor, const int target, int* script = NULL)
//        Reduce the given divisor to the given target vertex.
//	
//	* bool has_positive_rank(const my_graph& G, const int* divisor, bool check_graph_validity = true)
//        Test whether the given divisor has positive rank.
//	
//	* bool find_positive_rank_divisor(const my_graph& G, const int remaining_chips, const int finished_vertices = 0)
//        Brute force search for a positive rank effective divisor of prescribed degree. Somewhat optimized for performance.
//	
//	* void find_all_positive_rank_v0_reduced_divisors(const my_graph& G, const int remaining_chips, void (*const fn)(), const int finished_vertices = 0)
//        Brute force search for ALL positive rank v0-reduced divisors of prescribed degree. Somewhat optimized for performance.
//	
//      * int find_gonality(const my_graph& G)
//        Determine the (divisorial) gonality of G by brute force search.
// 

// #ifndef __DIVISORS_H__
// #define __DIVISORS_H__


#include <cassert>
#include <queue>
#include <stdio.h>
using namespace std;
const long long MAX_N = 100;
// #include "graphs.h"

// Global variables.
// Do NOT use these to store valuable data, as their contents will be overwritten by the functions from this file.
bool __pushed_to_queue[MAX_N];
int __burnt_edges[MAX_N];
int __firing_set[MAX_N];
int __partial_divisor[MAX_N];
int __tmp_divisor[MAX_N];
bool __can_reach[MAX_N];



// Dhar's burning algorithm.
// 
// Input values:
//     * the graph is given as the first input (my_graph data structure; passed by const reference);
//     * the divisor is given as the second input (C array; passed as const pointer);
//     * the starting vertex is given as the third input.
// 
// Output values:
//     * the firing set is stored in the global array __firing_set;
//     * the size of the firing set is returned as an integer.
// 
// Changes global variables __pushed_to_queue, __burnt_edges, __firing_set.
int burn(vector<vector<int>> graph, const int* divisor, const int start) {
	assert(start >= 0 && start < graph.size());
	for (int i = 0; i < graph.size(); i++) {
		__pushed_to_queue[i] = false;
		__burnt_edges[i] = 0;
		assert(i == start || divisor[i] >= 0);
	}
	std::queue<int> q;
	q.push(start);
	__pushed_to_queue[start] = true;
	while (!q.empty()) {
		int i = q.front();
		q.pop();
		for (auto j : graph[i]) {
			__burnt_edges[j]++;
			if (__burnt_edges[j] > divisor[j] && !__pushed_to_queue[j]) {
				q.push(j);
				__pushed_to_queue[j] = true;
			}
		}
	}
	int ret = 0;
	for (int i = 0; i < graph.size(); i++) {
		if (!__pushed_to_queue[i]) {
			__firing_set[ret] = i;
			ret++;
		}
	}
	return ret;
}

// Test whether a given divisor has positive rank.
// 
// Input values:
//     * the graph is given as the first input (my_graph data structure; passed by const reference);
//     * the divisor is given as the second input (C array; passed as const pointer);
//     * the option third argument enables or disables a sanity check of the input graph.
//       Set this option to false if you're doing a brute force search (e.g. find_positive_rank_divisor),
//       or you'll waste a lot of time!
// 
// Output values:
//     * the return value is a boolean indicating whether or not the divisor has positive rank.
// 
// Changes global variables __pushed_to_queue, __burnt_edges, __firing_set, __tmp_divisor, __can_reach.
bool has_positive_rank(vector<vector<int>> graph, const int* divisor) {
	for (int i = 0; i < graph.size(); i++) {
		assert(divisor[i] >= 0);
		__tmp_divisor[i] = divisor[i];
		__can_reach[i] = (divisor[i] > 0);
	}
	for (int u = 0; u < graph.size(); u++) {
		while (!__can_reach[u]) {
			int firing_set_size = burn(graph, __tmp_divisor, u);
			if (firing_set_size == 0) {
				return false;
			}
			for (int j = 0; j < firing_set_size; j++) {
				int v = __firing_set[j];
				for (auto w : graph[v]) {
					__tmp_divisor[v]--;
					__tmp_divisor[w]++;
				}
			}
			// record intermediate steps to save time
			for (int v = 0; v < graph.size(); v++) {
				if (__tmp_divisor[v] > 0) {
					__can_reach[v] = true;
				}
			}
		}
	}
	return true;
}

bool check_rank(vector<vector<int>> graph, const int* divisor, int order){
    if(order == 1){
        return has_positive_rank(graph, divisor);
    }
    
    for(int i = 0; i < graph.size(); i++){
        int temp_divisor [graph.size()];
        for(int j = 0; j< graph.size(); j++){
            temp_divisor[j] = divisor[j];
        }
        temp_divisor[i]--;

        // temp_divisor = [...divisor]
        // temp_divisor[i]--

        if(!check_rank(graph, temp_divisor, order-1)){
            return false;
        }
    }

    return true;
}

// Brute force search for a positive rank effective divisor of prescribed degree. Somewhat optimized for performance.
// 
// This function returns immediately after such a divisor is found; it does not proceed to find all such examples.
// To find all positive rank effective divisors, use the function find_all_positive_rank_v0_reduced_divisors() below.
// 
// Input values:
//     * the graph is given as the first input (my_graph data structure; passed by const reference);
//     * the requested degree is given as the second input;
//     * the third input is used for the purpose of recursion and should be omitted when calling this function.
// 
// Output values:
//     * the return value is a boolean indicating whether or not a positive rank divisor was found;
//     * in case of success, the found divisor is stored in the global variable __partial_divisor.
// 
// Changes global variables __pushed_to_queue, __burnt_edges, __firing_set, __partial_divisor, __tmp_divisor, __can_reach.
bool find_positive_rank_divisor(vector<vector<int>> graph, const int remaining_chips, const int finished_vertices, int order) {
	assert(remaining_chips >= 0);
	assert(finished_vertices >= 0 && finished_vertices <= graph.size());
	if (finished_vertices == 0) {
		// Sanity check. Only carried out once at the very beginning, when finished_vertices == 0.
		// (Other initializations should also go here.)
		// assert(G.is_valid_undirected_graph());
	}
	if (finished_vertices >= graph.size()) {
		// Found a divisor defined on all of G. Don't recurse any further.
		// Check whether this divisor has rank 1, but only if:
		//    * it has the right degree (i.e. all chips have been distributed);
		//    * there is at least one chip on v0;
		//    * it is already v0-reduced (to save time).
		// 
		// Note: logical and (&&) statements in C++ are short-circuiting, so the tests are carried out
		// from left to right and aborted as soon as any one of them returns false. This is especially
		// important because calls to the function has_positive_rank() dictate the total runtime.
		if(order == 1){
            return remaining_chips == 0 && __partial_divisor[0] > 0 && burn(graph, __partial_divisor, 0) == 0 && has_positive_rank(graph, __partial_divisor);
        }
        else{
            return remaining_chips == 0 && __partial_divisor[0] > 0 && burn(graph, __partial_divisor, 0) == 0 && check_rank(graph, __partial_divisor, order);
        }
	}
	
	// Recursively construct all possible effective divisors of the requested degree.
	// 
	// We start with as many chips as possible on the current vertex, and test all possible distributions
	// of the remaining chips over the remaining vertices before removing another chip from this vertex.
	// The advantage of this approach is that we will have dominated all effective divisors of degree k
	// before bringing the (k + 1)-th chip into play (i.e. putting it on another vertex than v0).
	// 
	// In particular, if you just want to know whether a positive rank divisor of degree d exists (i.e. if
	// you only want to know whether dgon(G) <= d), then instead of first calling this function for all
	// smaller degrees, it is just as fast to simply call find_positive_rank_divisor(G, d).
	// 
	// This function only looks for positive rank v0-reduced divisors, so we only need to consider
	// configurations with at least 1 chip on v0.
	const int stop = (finished_vertices == 0 ? 1 : 0);
	for (int i = remaining_chips; i >= stop; i--) {
		__partial_divisor[finished_vertices] = i;
		if (find_positive_rank_divisor(graph, remaining_chips - i, finished_vertices + 1, order)) {
			return true;
		}
	}
	__partial_divisor[finished_vertices] = -1;
	return false;
}

// Determine the (divisorial) gonality by brute force search.
// 
// Input values:
//     * the graph is given as the first and only input (my_graph data structure; passed by const reference).
// 
// Output values:
//     * the gonality of the graph is returned;
//     * a positive rank effective divisor of minimal degree is stored in the global variable __partial_divisor.
// 
// Changes global variables __pushed_to_queue, __burnt_edges, __firing_set, __partial_divisor, __tmp_divisor, __can_reach.
int find_gonality(vector<vector<int>> graph, int order) {
	// assert(G.is_valid_undirected_graph());
    
    for (int deg = 1; true; deg++) {
		if (find_positive_rank_divisor(graph, deg, 0, order)) {
			return deg;
		}
		assert(deg <= graph.size());
	}
}


// #endif