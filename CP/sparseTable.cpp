#include <bits/stdc++.h>

using namespace std;

#define rep(i, a, b) for(int i=a; i<b; i++)
#define trav(arr, x) for(auto x: arr)
#define printArr(arr, n) cout << #arr << ": "; rep(i, 0, n) cout << arr[i] << " \n"[i == n-1];
#define printVar(var) cout << #var << ": " << var << endl;

typedef long long int lld;
typedef vector<int> vi;
typedef pair<int, int> ii;
typedef vector<ii> vii;

struct SparseTable {
	// Stores indexes of minimum values
	// table[i][j] = index of minimum value in interval [i, i + (1 << j)]
	vector<vector<int>> table;

	SparseTable(vector<int> arr){
		int i, j;
		table.resize(arr.size() + 2);
		for(i = 0; i < (int)arr.size(); i++)
			table[i].push_back(i);
		for(j = 1; (1 << j) <= (int)arr.size(); j++)
		for(i = 0; i + (1 << j) - 1 < (int)arr.size(); i++)
		if(arr[table[i][j-1]] < arr[table[i+(1 << (j-1))][j-1]])
		table[i].push_back(table[i][j-1]);
		else
		table[i].push_back(table[i + (1 << (j-1))][j-1]);
	}

	int RMQA(int i, int j){
		int k = (int)log2(j-i + 1);

		if(table[i][k] <= table[j - (1 << k) + 1][k])
			return table[i][k];
		else
			return table[j - (1 << k) + 1][k];
	}
};

int main(void){
	/* Sparse table */
	int n;
	cin >> n;
	vector<int> arr(n);
	rep(i, 0, n)
		arr[i] = rand()/(RAND_MAX/n + 1);
	SparseTable tab(arr);
	cout << "Enter bounds for RMQ: " << endl;
	int i, j;
	cin >> i >> j;
	cout << "Minimum (index) is: " << tab.RMQA(i, j) << endl;
	cout << "Minimum (element) is: " << arr[tab.RMQA(i, j)] << endl;
	printArr(arr, n);
	return 0;
}
