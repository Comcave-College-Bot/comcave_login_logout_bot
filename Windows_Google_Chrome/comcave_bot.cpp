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

// Funktion zum Einlesen der setup.ini
std::string read_config(const std::string& key, const std::string& section) {
    std::ifstream config_file("setup.ini");
    std::string line, value;
    bool in_section = false;

    while (std::getline(config_file, line)) {
        if (line == "[" + section + "]") {
            in_section = true;
        } else if (in_section && line[0] == '[') {
            in_section = false;
        }

        if (in_section && line.find(key) != std::string::npos) {
            value = line.substr(line.find("=") + 1);
            value.erase(0, value.find_first_not_of(" \t\n\r"));
            value.erase(value.find_last_not_of(" \t\n\r") + 1);
            break;
        }
    }
    return value;
}

// Funktion zum Löschen und Neuschreiben der Benutzerdaten in der setup.ini
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

// Funktion zur Überprüfung und Installation von Python-Paketen
void install_python_packages() {
    std::string install_command = "python -m pip install selenium webdriver-manager";
    std::cout << "Überprüfe und installiere benötigte Python-Pakete...\n";
    int result = system(install_command.c_str());

    if (result == 0) {
        std::cout << "Python-Pakete wurden erfolgreich überprüft und installiert.\n";
    } else {
        std::cout << "Fehler bei der Installation der Python-Pakete. Bitte überprüfen Sie die Python-Umgebung.\n";
        exit(1);
    }
}

void login(const std::string& username, const std::string& password) {
    std::string command = "python login.py " + username + " " + password;
    system(command.c_str());
    std::cout << "Login-Vorgang abgeschlossen für Benutzer: " << username << "\n";
}

void logout(const std::string& username, const std::string& password) {
    std::string command = "python logout.py " + username + " " + password;
    system(command.c_str());
    std::cout << "Logout-Vorgang abgeschlossen für Benutzer: " << username << "\n";
}

// Funktion zum Planen einer Aufgabe mit zeitlicher Verzögerung
void schedule_task(const std::chrono::time_point<std::chrono::system_clock>& time, std::function<void()> task) {
    auto now = std::chrono::system_clock::now();
    if (time > now) {
        std::this_thread::sleep_for(time - now);
    }
    task();
}

// Funktion zum Parsen von Zeitangaben im Format HH:MM
bool parseTime(const std::string& timeStr, int& hour, int& minute) {
    char delimiter;
    std::istringstream timeStream(timeStr);
    timeStream >> hour >> delimiter >> minute;
    if (timeStream.fail() || delimiter != ':' || hour < 0 || hour > 23 || minute < 0 || minute > 59) {
        return false;
    }
    return true;
}

// Funktion zur Überprüfung, ob der aktuelle Tag ein Wochentag ist (Montag bis Freitag)
bool is_weekday(const std::tm& date) {
    int wday = date.tm_wday;
    return (wday >= 1 && wday <= 5);
}

// Funktion zur Überprüfung, ob das aktuelle Datum in einem Urlaubs- oder Feiertagszeitraum liegt
bool is_in_date_range(const std::tm& date, const std::vector<std::pair<std::tm, std::tm>>& date_ranges) {
    std::tm temp_date = date;
    for (const auto& range : date_ranges) {
        if (std::difftime(std::mktime(&temp_date), std::mktime(const_cast<std::tm*>(&range.first))) >= 0 &&
            std::difftime(std::mktime(&temp_date), std::mktime(const_cast<std::tm*>(&range.second))) <= 0) {
            std::cout << "Datum " << std::put_time(&date, "%d.%m.%Y") << " liegt im Zeitraum "
                      << std::put_time(&range.first, "%d.%m.%Y") << " bis "
                      << std::put_time(&range.second, "%d.%m.%Y") << ".\n";
            return true;
        }
    }
    std::cout << "Datum " << std::put_time(&date, "%d.%m.%Y") << " liegt nicht im Urlaubs- oder Feiertagszeitraum.\n";
    return false;
}

// Funktion zum Parsen von Zeiträumen aus der setup.ini
std::vector<std::pair<std::tm, std::tm>> parse_date_ranges(const std::string& date_str) {
    std::vector<std::pair<std::tm, std::tm>> date_ranges;
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

// Funktion zum Finden des nächsten gültigen Tages (kein Wochenende, Urlaub oder Feiertag)
std::tm find_next_valid_day(const std::tm& current_date, int login_hour, int login_minute,
                            const std::vector<std::pair<std::tm, std::tm>>& holiday_ranges,
                            const std::vector<std::pair<std::tm, std::tm>>& legal_holiday_ranges) {
    std::tm next_date = current_date;
    do {
        next_date.tm_mday += 1;
        mktime(&next_date); // Normalisiert das Datum
        std::cout << "Überprüfe nächstes Datum: " << std::put_time(&next_date, "%d.%m.%Y") << "\n";
    } while (!is_weekday(next_date) || is_in_date_range(next_date, holiday_ranges) || is_in_date_range(next_date, legal_holiday_ranges));

    next_date.tm_hour = login_hour;
    next_date.tm_min = login_minute;
    return next_date;
}

// Funktion zur korrekten Ausgabe des nächsten Login-Datums und -Uhrzeit
void print_next_login_time(const std::tm& calculated_tm, int login_hour, int login_minute) {
    std::tm next_valid_day = calculated_tm;
    next_valid_day.tm_hour = login_hour;
    next_valid_day.tm_min = login_minute;
    auto next_login_time = std::chrono::system_clock::from_time_t(mktime(&next_valid_day));

    std::cout << "Nächster Login geplant für: " 
              << std::put_time(&next_valid_day, "%d.%m.%Y %H:%M") << "\n";
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
    holiday_str = read_config("urlaub_dates", "Urlaub");
    legal_holiday_str = read_config("feiertag_dates", "Gesetzliche Feiertage");

    std::vector<std::pair<std::tm, std::tm>> holiday_ranges = parse_date_ranges(holiday_str);
    std::vector<std::pair<std::tm, std::tm>> legal_holiday_ranges = parse_date_ranges(legal_holiday_str);

    if (username.empty() || password.empty()) {
        std::cout << "Bitte geben Sie Ihren Benutzernamen ein: ";
        std::getline(std::cin, username);
        std::cout << "Bitte geben Sie Ihr Passwort ein: ";
        std::getline(std::cin, password);
        std::cout << "Möchten Sie Ihre Anmeldedaten speichern? (ja/nein): ";
        std::string save_credentials;
        std::getline(std::cin, save_credentials);

        if (save_credentials == "ja") {
            clear_and_write_credentials(username, password);
        }
    } else {
        std::cout << "Benutzername und Passwort wurden erfolgreich geladen." << std::endl;
    }

    int attempts = 0;
    while (attempts < 5) {
        std::cout << "Bitte geben Sie die Login-Zeit ein (HH:MM): ";
        std::getline(std::cin, login_time_str);
        if (parseTime(login_time_str, login_hour, login_minute)) {
            break;
        } else {
            std::cout << "Ungültiges Zeitformat. Bitte im Format HH:MM eingeben." << std::endl;
            attempts++;
        }
    }
    if (attempts == 5) {
        std::cout << "Maximale Anzahl an Versuchen erreicht. Programm wird beendet." << std::endl;
        return 1;
    }

    attempts = 0;
    while (attempts < 5) {
        std::cout << "Bitte geben Sie die Logout-Zeit ein (HH:MM): ";
        std::getline(std::cin, logout_time_str);
        if (parseTime(logout_time_str, logout_hour, logout_minute)) {
            break;
        } else {
            std::cout << "Ungültiges Zeitformat. Bitte im Format HH:MM eingeben." << std::endl;
            attempts++;
        }
    }
    if (attempts == 5) {
        std::cout << "Maximale Anzahl an Versuchen erreicht. Programm wird beendet." << std::endl;
        return 1;
    }

    while (true) {
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
            std::cout << "Es ist nach der Login-Zeit und vor der Logout-Zeit. Führe nur Logout durch.\n";
            schedule_task(logout_time, [=]() {
                logout(username, password);
                std::tm next_login_tm = find_next_valid_day(*local_tm, login_hour, login_minute, holiday_ranges, legal_holiday_ranges);
                print_next_login_time(next_login_tm, login_hour, login_minute);
            });
        } else if (now > logout_time) {
            std::cout << "Es ist nach der Logout-Zeit. Aktionen werden morgen durchgeführt.\n";
            std::this_thread::sleep_for(std::chrono::hours(24));
        } else {
            std::cout << "Login-Zeit geplant für "
                      << std::setw(2) << std::setfill('0') << login_hour << ":"
                      << std::setw(2) << std::setfill('0') << login_minute << "\n";

            std::cout << "Logout-Zeit geplant für "
                      << std::setw(2) << std::setfill('0') << logout_hour << ":"
                      << std::setw(2) << std::setfill('0') << logout_minute << "\n";

            schedule_task(login_time, [=]() {
                login(username, password);
                std::cout << "Nächster Logout geplant für: " << std::put_time(local_tm, "%d.%m.%Y %H:%M") << "\n";

                schedule_task(logout_time, [=]() {
                    logout(username, password);
                    std::tm next_login_tm = find_next_valid_day(*local_tm, login_hour, login_minute, holiday_ranges, legal_holiday_ranges);
                    print_next_login_time(next_login_tm, login_hour, login_minute);
                });
            });
        }
        std::this_thread::sleep_for(std::chrono::hours(24));
    }

    return 0;
}
