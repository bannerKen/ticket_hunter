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
											  string Endyear, string Endmonth, string Endday){
	int syear = stoi(Startyear); //start year
	int smonth = stoi(Startmonth); //start month
	int sday = stoi(Startday); //start day
	int eyear = stoi(Endyear); //end year
	int emonth = stoi(Endmonth); //end month
	int eday = stoi(Endday); //end day
	vector<pair<string,string>> ans(5);

	// push the first date
	ans[0] = {to_string(syear)+"-"+to_string(smonth)+"-"+to_string(sday), to_string(eyear)+"-"+to_string(emonth)+"-"+to_string(eday)};

	//get how many day of trip
	int dayOfTrip = getdayOfTrip(syear,smonth,sday,eyear,emonth,eday);

    std::tm start_date = {};
    start_date.tm_year = syear - 1900; //
    start_date.tm_mon = smonth-1; // 5
    start_date.tm_mday = sday;

    std::chrono::system_clock::time_point start_tp = std::chrono::system_clock::from_time_t(std::mktime(&start_date));

    for (int i = 1; i < 5; ++i) {
        std::chrono::system_clock::time_point next_week = start_tp + std::chrono::hours(24 * 7 * i);

        std::time_t next_week_time = std::chrono::system_clock::to_time_t(next_week);
        std::tm* next_week_tm = std::localtime(&next_week_time);

        ans[i].first = to_string(next_week_tm->tm_year + 1900)+"-"+to_string(next_week_tm->tm_mon + 1)+"-"+to_string(next_week_tm->tm_mday);

        std::chrono::system_clock::time_point next_week_end = next_week + std::chrono::hours(24 * dayOfTrip);

        std::time_t next_week_end_time = std::chrono::system_clock::to_time_t(next_week_end);
        std::tm* next_week_end_tm = std::localtime(&next_week_end_time);

        ans[i].second = to_string(next_week_end_tm->tm_year + 1900)+"-"+to_string(next_week_end_tm->tm_mon + 1)+"-"+to_string(next_week_end_tm->tm_mday);
    }

	return ans;
}


/* getdayOfTrip
 *
 * Description : return how many day between the two date
 *
 * */
int getdayOfTrip(int syear, int smonth, int sday,
				 int eyear, int emonth, int eday){

	tm start_date = {};
	start_date.tm_year = syear - 1900;
	start_date.tm_mon = smonth-1; // 2
	start_date.tm_mday = sday;

	tm end_date = {};
	end_date.tm_year = eyear - 1900;
	end_date.tm_mon = emonth-1; // 4
	end_date.tm_mday = eday;


	chrono::system_clock::time_point start_tp = chrono::system_clock::from_time_t(std::mktime(&start_date));
	chrono::system_clock::time_point end_tp = chrono::system_clock::from_time_t(std::mktime(&end_date));


	chrono::duration<double> duration = end_tp - start_tp;
	double days = duration.count() / (60 * 60 * 24);


	return days;
}

#endif
