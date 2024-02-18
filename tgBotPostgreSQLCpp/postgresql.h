#pragma once

#include <string>
#include <iostream>
#include <pqxx/pqxx>


auto postgreSQLCheck(const std::string passPhrase) {
    std::string connectionString = "host=81.31.245.131 port=5432 dbname=SMBHosts user=tgbot password=tgbot";

    try {
        pqxx::connection connectionObject(connectionString.c_str());
        pqxx::work worker(connectionObject);
        pqxx::result response = worker.exec(passPhrase);

        return response;
    }
    catch (const std::exception& e) {
        std::cerr << e.what() << std::endl;
    }
}