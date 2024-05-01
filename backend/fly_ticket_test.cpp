//============================================================================
// Name        : fly_ticket_test.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include <vector>
#include "date.h"

using namespace std;

int main() {
	cout << "!!!Hello World!!!" << endl; // prints !!!Hello World!!!

	vector<pair<string,string>> test;
	test = getStartAndEndDay("2024", "5", "5","2024", "5", "9");
	for(int i=0; i<test.size(); i++){
		cout<<test[i].first<< " -> " <<test[i].second<<endl;
	}

	return 0;
}
