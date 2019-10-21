#include <bits/stdc++.h>

using namespace std;

#define rep(i, a, b) for(int i=a; i<b; i++)

typedef long long int lld;
typedef vector<int> vi;
typedef pair<int, int> ii;
typedef vector<ii> vii;


// Sqrt decomposition test
int main(void){
	int n;
	cin >> n;
	int s = ceil(sqrt(n));
	vi nums(n);
	rep(i, 0, n)
		nums[i] = rand()/(RAND_MAX/200 + 1);
	vi b(n/s + 2, 0);
	rep(i, 0, n)
		b[i/s] += nums[i];
	cout << "Enter bounds to get subarray sum (inclusive): ";
	int x, y;
	cin >> x >> y;
	int res = 0;
	int i = x;
	while(i <= y){
		if(i%s == 0 && i+s <= y){
			res += b[i/s];
			i += s;
		}
		else{
			res += nums[i++];
		}
	}	
	cout << "Subarray sum is: " << res << endl;
	cout << "Elements are: ";
	rep(i, x, y+1){
		cout << nums[i] << " \n"[i==y];
	}
	return 0;
}
