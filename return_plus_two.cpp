#include <iostream>
#include <string>
#include <cstdlib>

#include "httplib.h"
#include "json.hpp"

using namespace httplib;
using json = nlohmann::json;

int main() {
    Server svr;

    // 定義 POST 端點，接收 JavaScript 的請求
    svr.Post("/add", [](const Request& req, Response& res) {

        try {
        // 解析 JSON 請求主體，假設其格式為 { "number": 5 }
        json req_json = json::parse(req.body);

        // Sabrina{4/24}:
        std::cout << "Received JSON data: " << req.body << std::endl;

        // 從 JSON 中取得數字
        int number = req_json["number"];

        // 執行運算
        int result = number + 2;

        // 將結果轉換為 JSON 格式
        json res_json;
        res_json["result"] = result;

        // Sabrina{4/24}:handle CORS
        res.set_header("Access-Control-Allow-Origin", "*");
        res.set_header("Access-Control-Allow-Methods", "POST, OPTIONS");
        res.set_header("Access-Control-Allow-Headers", "Content-Type, X-Requested-With");



        // 設置回應
        res.set_content(res_json.dump(), "application/json");
        } catch (const std::exception& e) {
            std::cerr << "Error processing request: " << e.what() << std::endl;
            res.status = 500;
            res.set_content("Internal Server Error", "text/plain");
        }
        
    });

     // Sabrina{4/24}:handle CORS
    svr.Options("/add", [](const Request& req, Response& res) {
        res.set_header("Access-Control-Allow-Origin", "*");
        res.set_header("Access-Control-Allow-Methods", "POST, OPTIONS");
        res.set_header("Access-Control-Allow-Headers", "Content-Type");
        res.status = 200;
    });
    
    std::cout << "C++ API Server is running on port 8080" << std::endl;

    // 啟動伺服器
    svr.listen("localhost", 8080);

    return 0;
}