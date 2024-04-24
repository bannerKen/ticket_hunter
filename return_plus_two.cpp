#include <iostream>
#include <string>
#include <cstdlib>

#include <cpp_httplib/httplib.h>
#include <nlohmann/json.hpp>

using namespace httplib;
using json = nlohmann::json;

int main() {
    Server svr;

    // 定義 POST 端點，接收 JavaScript 的請求
    svr.Post("/add", [](const Request& req, Response& res) {
        // 解析 JSON 請求主體，假設其格式為 { "number": 5 }
        json req_json = json::parse(req.body);

        // 從 JSON 中取得數字
        int number = req_json["number"];

        // 執行運算
        int result = number + 2;

        // 將結果轉換為 JSON 格式
        json res_json;
        res_json["result"] = result;

        // 設置回應
        res.set_content(res_json.dump(), "application/json");
    });

    std::cout << "C++ API Server is running on port 8080" << std::endl;

    // 啟動伺服器
    svr.listen("localhost", 8080);

    return 0;
}