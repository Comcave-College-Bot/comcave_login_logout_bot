#include <iostream>
#include <string>
#include <chrono>
#include <thread>
#include <functional>
#include <sstream>
#include <ctime>
#include <iomanip>  // Für std::setw und std::setfill
#include <windows.h>  // Für die Windows-API-Funktionen zur UTF-8-Unterstützung
#include <fstream>

// Funktion zum Einlesen der setup.ini
std::string read_config(const std::string& key) {
    std::ifstream config_file("setup.ini");
    std::string line, value;
    while (std::getline(config_file, line)) {
        if (line.find(key) != std::string::npos) {
            value = line.substr(line.find("=") + 1);
            // Entfernt mögliche Leerzeichen am Anfang oder Ende
            value.erase(0, value.find_first_not_of(" \t\n\r"));
            value.erase(value.find_last_not_of(" \t\n\r") + 1);
            break;
        }
    }
    return value;
}

// Funktion zum Speichern in der setup.ini
void write_config(const std::string& key, const std::string& value) {
    std::ofstream config_file("setup.ini", std::ios_base::app);
    config_file << key << "=" << value << "\n";
}

void login(const std::string& username, const std::string& password) {
    // Python-Skript für den Web-Automatisierungs-Login aufrufen
    std::string command = "python login.py " + username + " " + password;
    system(command.c_str());

    std::cout << "Login-Vorgang abgeschlossen für Benutzer: " << username << "\n";
}

void logout(const std::string& username, const std::string& password) {
    // Python-Skript für den Web-Automatisierungs-Logout aufrufen
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

    // Überprüft das Format HH:MM und ob Stunden und Minuten im gültigen Bereich liegen
    if (timeStream.fail() || delimiter != ':' || hour < 0 || hour > 23 || minute < 0 || minute > 59) {
        return false;
    }
    return true;
}

bool is_weekday() {
    auto now = std::chrono::system_clock::now();
    std::time_t t = std::chrono::system_clock::to_time_t(now);
    std::tm* local_tm = std::localtime(&t);
    int wday = local_tm->tm_wday; // 0 = Sonntag, 1 = Montag, ..., 6 = Samstag
    return (wday >= 1 && wday <= 5); // Montag (1) bis Freitag (5)
}

int main() {
    // UTF-8 Unterstützung auf Windows aktivieren
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);

    std::string username, password;
    std::string login_time_str, logout_time_str;
    int login_hour, login_minute, logout_hour, logout_minute;

    // Benutzername und Passwort aus der setup.ini lesen
    username = read_config("username");
    password = read_config("password");

    // Falls Benutzername und Passwort nicht in der setup.ini vorhanden sind, abfragen und optional speichern
    if (username.empty() || password.empty()) {
        std::cout << "Bitte geben Sie Ihren Benutzernamen ein: ";
        std::getline(std::cin, username);

        std::cout << "Bitte geben Sie Ihr Passwort ein: ";
        std::getline(std::cin, password);

        std::cout << "Möchten Sie Ihre Anmeldedaten speichern? (ja/nein): ";
        std::string save_credentials;
        std::getline(std::cin, save_credentials);

        if (save_credentials == "ja") {
            write_config("username", username);
            write_config("password", password);
        }
    } else {
        std::cout << "Benutzername und Passwort wurden erfolgreich geladen." << std::endl;
    }

    // Login-Zeit abfragen mit bis zu 5 Versuchen
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

    // Logout-Zeit abfragen mit bis zu 5 Versuchen
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

    while (true) {  // Endlosschleife für wöchentliche Ausführung
        if (is_weekday()) {
            // Aktuelle Zeit
            auto now = std::chrono::system_clock::now();
            auto today = std::chrono::system_clock::to_time_t(now);
            tm* local_tm = localtime(&today);

            // Login-Zeit einstellen
            local_tm->tm_hour = login_hour;
            local_tm->tm_min = login_minute;
            local_tm->tm_sec = 0;  // Sekunden auf 0 setzen
            auto login_time = std::chrono::system_clock::from_time_t(mktime(local_tm));

            // Logout-Zeit einstellen
            local_tm->tm_hour = logout_hour;
            local_tm->tm_min = logout_minute;
            local_tm->tm_sec = 0;  // Sekunden auf 0 setzen
            auto logout_time = std::chrono::system_clock::from_time_t(mktime(local_tm));

            if (now > login_time && now < logout_time) {
                std::cout << "Es ist nach der Login-Zeit und vor der Logout-Zeit. Führe nur Logout durch.\n";
                schedule_task(logout_time, [=]() { logout(username, password); });
            } else if (now > logout_time) {
                std::cout << "Es ist nach der Logout-Zeit. Aktionen werden morgen durchgeführt.\n";
                // Warten bis zum nächsten Tag
                std::this_thread::sleep_for(std::chrono::hours(24));
            } else {
                std::cout << "Login-Zeit geplant für " 
                          << std::setw(2) << std::setfill('0') << login_hour << ":" 
                          << std::setw(2) << std::setfill('0') << login_minute << "\n";
                
                std::cout << "Logout-Zeit geplant für " 
                          << std::setw(2) << std::setfill('0') << logout_hour << ":" 
                          << std::setw(2) << std::setfill('0') << logout_minute << "\n";

                // Login zur geplanten Zeit
                schedule_task(login_time, [=]() {
                    login(username, password);
                    schedule_task(logout_time, [=]() { logout(username, password); });
                });
            }
        }

        // Warten bis zum nächsten Tag
        std::this_thread::sleep_for(std::chrono::hours(24));
    }

    return 0;
}
