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

// Funktion zum Einlesen der setup.ini
std::string read_config(const std::string& key) {
    std::ifstream config_file("setup.ini");
    std::string line, value;
    while (std::getline(config_file, line)) {
        if (line.find(key) != std::string::npos) {
            value = line.substr(line.find("=") + 1);
            value.erase(0, value.find_first_not_of(" \t\n\r"));
            value.erase(value.find_last_not_of(" \t\n\r") + 1);
            break;
        }
    }
    return value;
}

// Funktion zum Löschen und Neuschreiben der Credentials in der setup.ini
void clear_and_write_credentials(const std::string& username, const std::string& password) {
    std::ifstream config_file("setup.ini");
    std::string line;
    std::stringstream buffer;

    bool in_credentials_section = false;

    // Einlesen der aktuellen Datei und Überspringen der alten Credentials
    while (std::getline(config_file, line)) {
        if (line == "[Credentials]") {
            in_credentials_section = true;
        } else if (in_credentials_section && line.empty()) {
            in_credentials_section = false; // Nach einer leeren Zeile nach [Credentials] endet die Sektion
        } else if (!in_credentials_section) {
            buffer << line << "\n";
        }
    }
    config_file.close();

    // Neues Schreiben der Datei mit den neuen Credentials
    std::ofstream config_file_out("setup.ini");
    config_file_out << buffer.str(); // Schreibe den vorherigen Inhalt ohne alte Credentials
    config_file_out << "[Credentials]\n"; // Überschreibe oder füge die Credentials hinzu
    config_file_out << "username=" << username << "\n";
    config_file_out << "password=" << password << "\n";
    config_file_out.close();
}

// Funktion zur Überprüfung und Installation von Python-Paketen
void install_python_packages() {
    // Befehl zur Installation der benötigten Python-Pakete
    std::string install_command = "python -m pip install selenium webdriver-manager";

    std::cout << "Überprüfe und installiere benötigte Python-Pakete...\n";
    int result = system(install_command.c_str());

    if (result == 0) {
        std::cout << "Python-Pakete wurden erfolgreich überprüft und installiert.\n";
    } else {
        std::cout << "Fehler bei der Installation der Python-Pakete. Bitte überprüfen Sie die Python-Umgebung.\n";
        exit(1); // Programm beenden, wenn die Installation fehlschlägt
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

void schedule_task(const std::chrono::time_point<std::chrono::system_clock>& time, std::function<void()> task) {
    auto now = std::chrono::system_clock::now();
    if (time > now) {
        std::this_thread::sleep_for(time - now);
    }
    task();
}

bool parseTime(const std::string& timeStr, int& hour, int& minute) {
    char delimiter;
    std::istringstream timeStream(timeStr);
    timeStream >> hour >> delimiter >> minute;
    if (timeStream.fail() || delimiter != ':' || hour < 0 || hour > 23 || minute < 0 || minute > 59) {
        return false;
    }
    return true;
}

bool is_weekday() {
    auto now = std::chrono::system_clock::now();
    std::time_t t = std::chrono::system_clock::to_time_t(now);
    std::tm* local_tm = std::localtime(&t);
    int wday = local_tm->tm_wday;
    return (wday >= 1 && wday <= 5);
}

int main() {
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);

    // Überprüfung und Installation der benötigten Python-Pakete
    install_python_packages();

    std::string username, password;
    std::string login_time_str, logout_time_str;
    int login_hour, login_minute, logout_hour, logout_minute;

    username = read_config("username");
    password = read_config("password");

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
        if (is_weekday()) {
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
                schedule_task(logout_time, [=]() { logout(username, password); });
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
                    schedule_task(logout_time, [=]() { logout(username, password); });
                });
            }
        }
        std::this_thread::sleep_for(std::chrono::hours(24));
    }

    return 0;
}
