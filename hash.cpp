#include <string>
#include <iostream>

int main(int argc, char** argv){
    std::string username = argv[1];
    std::string password = argv[2];
    auto uhash = std::hash<std::string>{}(username);
    auto phash = std::hash<std::string>{}(password);

    std::cout << (uhash ^ (phash << 1));
}