#include <iostream>
#include <string>
#include <chrono>
#include <thread>
#include <functional>
#include <sstream>
#include <ctime>
#include <iomanip>
#include <windows.h>
#include <fstream>
#include <vector>

// Function to read configuration from setup.ini
std::string read_config(const std::string& key, const std::string& section) {
    std::ifstream config_file("setup.ini");
    std::string line, value;
    bool in_section = false;
    std::string section_header = "[" + section + "]";
    while (std::getline(config_file, line)) {
        if (line == section_header) {
            in_section = true;
        } else if (in_section && line.find('=') != std::string::npos) {
            std::string current_key = line.substr(0, line.find("="));
            if (current_key == key) {
                value = line.substr(line.find("=") + 1);
                value.erase(0, value.find_first_not_of(" \t\n\r"));
                value.erase(value.find_last_not_of(" \t\n\r") + 1);
                break;
            }
        } else if (!line.empty() && line[0] == '[') {
            in_section = false;
        }
    }
    return value;
}

// Function to clear and write credentials in setup.ini
void clear_and_write_credentials(const std::string& username, const std::string& password) {
    std::ifstream config_file("setup.ini");
    std::string line;
    std::stringstream buffer;

    bool in_credentials_section = false;

    while (std::getline(config_file, line)) {
        if (line == "[Benutzerdaten]") {
            in_credentials_section = true;
        } else if (in_credentials_section && line.empty()) {
            in_credentials_section = false;
        } else if (!in_credentials_section) {
            buffer << line << "\n";
        }
    }
    config_file.close();

    std::ofstream config_file_out("setup.ini");
    config_file_out << buffer.str();
    config_file_out << "[Benutzerdaten]\n";
    config_file_out << "username=" << username << "\n";
    config_file_out << "password=" << password << "\n";
    config_file_out.close();
}

// Function to install Python packages
void install_python_packages() {
    std::string install_command = "python -m pip install selenium webdriver-manager";
    std::cout << "Checking and installing required Python packages...\n";
    int result = system(install_command.c_str());

    if (result == 0) {
        std::cout << "Python packages checked and installed successfully.\n";
    } else {
        std::cout << "Error installing Python packages. Please check your Python environment.\n";
        exit(1);
    }
}

void login(const std::string& username, const std::string& password) {
    std::string command = "python login.py " + username + " " + password;
    system(command.c_str());
    std::cout << "Login process completed for user: " << username << "\n";
}

void logout(const std::string& username, const std::string& password) {
    std::string command = "python logout.py " + username + " " + password;
    system(command.c_str());
    std::cout << "Logout process completed for user: " << username << "\n";
}

// Function to schedule a task with a delay
void schedule_task(const std::chrono::time_point<std::chrono::system_clock>& time, std::function<void()> task) {
    auto now = std::chrono::system_clock::now();
    if (time > now) {
        std::this_thread::sleep_for(time - now);
    }
    task();
}

// Function to parse time in HH:MM format
bool parseTime(const std::string& timeStr, int& hour, int& minute) {
    char delimiter;
    std::istringstream timeStream(timeStr);
    timeStream >> hour >> delimiter >> minute;
    return !timeStream.fail() && delimiter == ':' && hour >= 0 && hour <= 23 && minute >= 0 && minute <= 59;
}

// Function to check if the current day is a weekday (Monday to Friday)
bool is_weekday() {
    auto now = std::chrono::system_clock::now();
    std::time_t t = std::chrono::system_clock::to_time_t(now);
    std::tm* local_tm = std::localtime(&t);
    return (local_tm->tm_wday >= 1 && local_tm->tm_wday <= 5);
}

// Function to check if the current date is within a holiday or vacation period
bool is_in_date_range(const std::vector<std::pair<std::tm, std::tm>>& date_ranges) {
    auto now = std::chrono::system_clock::now();
    std::time_t t = std::chrono::system_clock::to_time_t(now);
    std::tm* local_tm = std::localtime(&t);

    for (const auto& range : date_ranges) {
        if (std::difftime(std::mktime(local_tm), std::mktime(const_cast<std::tm*>(&range.first))) >= 0 &&
            std::difftime(std::mktime(local_tm), std::mktime(const_cast<std::tm*>(&range.second))) <= 0) {
            return true;
        }
    }
    return false;
}

// Function to parse date ranges from setup.ini
std::vector<std::pair<std::tm, std::tm>> parse_date_ranges(const std::string& date_str) {
    std::vector<std::pair<std::tm, std::tm>> date_ranges;
    if (date_str.empty()) return date_ranges;

    std::istringstream date_stream(date_str);
    std::string range;

    while (std::getline(date_stream, range, ',')) {
        std::tm start = {}, end = {};
        std::istringstream range_stream(range);
        range_stream >> std::get_time(&start, "%d.%m.%Y");

        if (range_stream.peek() == '-') {
            range_stream.ignore(1, '-');
            range_stream >> std::get_time(&end, "%d.%m.%Y");
        } else {
            end = start;
        }

        if (!range_stream.fail()) {
            date_ranges.emplace_back(start, end);
        }
    }

    return date_ranges;
}

int main() {
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);

    install_python_packages();

    std::string username, password;
    std::string login_time_str, logout_time_str, holiday_str, legal_holiday_str;
    int login_hour, login_minute, logout_hour, logout_minute;

    username = read_config("username", "Benutzerdaten");
    password = read_config("password", "Benutzerdaten");
    holiday_str = read_config("dates", "Urlaub");
    legal_holiday_str = read_config("dates", "Gesetzliche Feiertage");

    std::vector<std::pair<std::tm, std::tm>> holiday_ranges = parse_date_ranges(holiday_str);
    std::vector<std::pair<std::tm, std::tm>> legal_holiday_ranges = parse_date_ranges(legal_holiday_str);

    if (username.empty() || password.empty()) {
        std::cout << "Please enter your username: ";
        std::getline(std::cin, username);
        std::cout << "Please enter your password: ";
        std::getline(std::cin, password);
        std::cout << "Would you like to save your credentials? (yes/no): ";
        std::string save_credentials;
        std::getline(std::cin, save_credentials);

        if (save_credentials == "yes") {
            clear_and_write_credentials(username, password);
        }
    } else {
        std::cout << "Username and password loaded successfully.\n";
    }

    int attempts = 0;
    while (attempts < 5) {
        std::cout << "Please enter the login time (HH:MM): ";
        std::getline(std::cin, login_time_str);
        if (parseTime(login_time_str, login_hour, login_minute)) {
            break;
        } else {
            std::cout << "Invalid time format. Please enter in HH:MM format.\n";
            attempts++;
        }
    }
    if (attempts == 5) {
        std::cout << "Maximum number of attempts reached. Program will terminate.\n";
        return 1;
    }

    attempts = 0;
    while (attempts < 5) {
        std::cout << "Please enter the logout time (HH:MM): ";
        std::getline(std::cin, logout_time_str);
        if (parseTime(logout_time_str, logout_hour, logout_minute)) {
            break;
        } else {
            std::cout << "Invalid time format. Please enter in HH:MM format.\n";
            attempts++;
        }
    }
    if (attempts == 5) {
        std::cout << "Maximum number of attempts reached. Program will terminate.\n";
        return 1;
    }

    while (true) {
        if (is_weekday() && !is_in_date_range(holiday_ranges) && !is_in_date_range(legal_holiday_ranges)) {
            auto now = std::chrono::system_clock::now();
            auto today = std::chrono::system_clock::to_time_t(now);
            tm* local_tm = localtime(&today);

            local_tm->tm_hour = login_hour;
            local_tm->tm_min = login_minute;
            local_tm->tm_sec = 0;
            auto login_time = std::chrono::system_clock::from_time_t(mktime(local_tm));

            local_tm->tm_hour = logout_hour;
            local_tm->tm_min = logout_minute;
            local_tm->tm_sec = 0;
            auto logout_time = std::chrono::system_clock::from_time_t(mktime(local_tm));

            if (now > login_time && now < logout_time) {
                std::cout << "After login time and before logout time. Only performing logout.\n";
                schedule_task(logout_time, [=]() {
                    logout(username, password);
                    std::cout << "Next login scheduled for: "
                              << std::put_time(local_tm, "%d.%m.%Y %H:%M") << "\n";
                });
            } else if (now > logout_time) {
                std::cout << "After logout time. Actions will be performed tomorrow.\n";
                std::this_thread::sleep_for(std::chrono::hours(24));
            } else {
                std::cout << "Login time scheduled for "
                          << std::setw(2) << std::setfill('0') << login_hour << ":"
                          << std::setw(2) << std::setfill('0') << login_minute << "\n";

                std::cout << "Logout time scheduled for "
                          << std::setw(2) << std::setfill('0') << logout_hour << ":"
                          << std::setw(2) << std::setfill('0') << logout_minute << "\n";

                schedule_task(login_time, [=]() {
                    login(username, password);
                    std::cout << "Next logout scheduled for: "
                              << std::put_time(local_tm, "%d.%m.%Y %H:%M") << "\n";
                    schedule_task(logout_time, [=]() {
                        logout(username, password);
                        std::cout << "Next login scheduled for: "
                                  << std::put_time(local_tm, "%d.%m.%Y %H:%M") << "\n";
                    });
                });
            }
        } else {
            std::cout << "Today is a holiday, legal holiday, or weekend. No actions will be performed.\n";
        }
        std::this_thread::sleep_for(std::chrono::hours(24));
    }

    return 0;
}
