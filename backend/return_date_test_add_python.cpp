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

    // defind POST terminalŒgset JavaScript request
    svr.Post("/date", [](const Request& req, Response& res) {

        try {
        json req_json = json::parse(req.body);

        // Sabrina{4/24}:
        std::cout << "Received JSON data: " << req.body << std::endl;

        // get key value from json
        string sdate = req_json["startDate"];
        string edate = req_json["endDate"];
        string departure = req_json["departure"];
        string arrival = req_json["arrival"];
        string adult = req_json["adult"];
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
            dateGroup[i]["departure"] = departure;
            dateGroup[i]["arrival"] = arrival;
            dateGroup[i]["adult"] = adult;
        }

        // Sabrina{4/24}:handle CORS
        res.set_header("Access-Control-Allow-Origin", "*");
        res.set_header("Access-Control-Allow-Methods", "POST, OPTIONS");
        res.set_header("Access-Control-Allow-Headers", "Content-Type, X-Requested-With");

            /* for send to python start */

            // create python port
            Client client("localhost", 5000);
            //send to python port
            auto res = client.Post("/process_data", json(dateGroup).dump(), "application/json");

            //check send success or fail
            if (res && res->status == 200) {
                // 解析返回的 JSON 數據
                //json res_json = json::parse(res->body);
                vector<json> vec_json_from_python = json::parse(res_body);

                // 提取返回的結果
                //int result_a = res_json["result_a"];

                // 打印返回的結果
                //std::cout << "Result a: " << result_a << std::endl;
            } else {
                std::cerr << "Error: Cannot connect to the server or invalid response" << std::endl;
            }

            /* for send to python end */

        //
        res.set_content(json(vec_json_from_python).dump(), "application/json");
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

    //™¨
    svr.listen("localhost", 8080);

    return 0;
}
