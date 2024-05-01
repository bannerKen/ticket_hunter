/*
 * date.h
 *
 *  Created on: 2024¦~5¤ë1¤é
 *      Author: Sheep
 */
#ifndef date_H_
#define date_H_

using namespace std;
#include <vector>
#include <utility>
#include <string>       // std::string
#include <iostream>
#include <chrono>
#include <ctime>
#include <ratio>

/* getStartAndEndDay(string year, string month, string day)
 *
 * Description : generate the date (4 group)
 *
 *
 * */
vector<pair<string,string>> getStartAndEndDay(string Startyear, string Startmonth, string Startday,
											  string Endyear, string Endmonth, string Endday);


/* getdayOfTrip
 *
 * Description : return how many day between the two date
 *
 * */
int getdayOfTrip(int syear, int smonth, int sday,
				 int eyear, int emonth, int eday);

#endif
