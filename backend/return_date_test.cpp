#include <iostream>
#include <string>
#include <cstdlib>

#include "date.h"
#include "httplib.h"
#include "json.hpp"

using namespace std;
using namespace httplib;
using json = nlohmann::json;

int main() {
    Server svr;

    // defind POST terminalågset JavaScript request
    svr.Post("/date", [](const Request& req, Response& res) {

        try {
        json req_json = json::parse(req.body);

        // Sabrina{4/24}:
        std::cout << "Received JSON data: " << req.body << std::endl;

        // get key value from json
        string sdate = req_json["startDate"];
        string edate = req_json["endDate"];
        string sy = sdate.substr (0,4);
        string sm = sdate.substr (5,2);
        string sd = sdate.substr (8,2);
        string ey = edate.substr (0,4);
        string em = edate.substr (5,2);
        string ed = edate.substr (8,2);

        // generate date
        vector<pair<string,string>> date;
        date = getStartAndEndDay(sy, sm, sd, ey, em, ed);

        vector<json> dateGroup(date.size());

        for(int i=0; i<date.size(); i++){
            dateGroup[i]["startDate"] = date[i].first;
            dateGroup[i]["endDate"] = date[i].second;
        }

        // Sabrina{4/24}:handle CORS
        res.set_header("Access-Control-Allow-Origin", "*");
        res.set_header("Access-Control-Allow-Methods", "POST, OPTIONS");
        res.set_header("Access-Control-Allow-Headers", "Content-Type, X-Requested-With");



        //
        res.set_content(json(dateGroup).dump(), "application/json");
        } catch (const std::exception& e) {
            std::cerr << "Error processing request: " << e.what() << std::endl;
            res.status = 500;
            res.set_content("Internal Server Error", "text/plain");
        }
        
    });

     // Sabrina{4/24}:handle CORS
    svr.Options("/date", [](const Request& req, Response& res) {
        res.set_header("Access-Control-Allow-Origin", "*");
        res.set_header("Access-Control-Allow-Methods", "POST, OPTIONS");
        res.set_header("Access-Control-Allow-Headers", "Content-Type");
        res.status = 200;
    });
    
    std::cout << "C++ API Server is running on port 8080" << std::endl;

    //ô®
    svr.listen("localhost", 8080);

    return 0;
}
