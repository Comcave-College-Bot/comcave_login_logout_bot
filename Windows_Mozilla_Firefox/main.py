from web_automation import WebAutomation
from datetime import datetime, timedelta
import schedule
import time
import sys
import random
import configparser
import os

class AutomationManager:
    def __init__(self):
        self.web_automation = WebAutomation()

    def add_random_variation(self, time_str):
        # Fügt ±5 Minuten zufällige Variation hinzu
        time_obj = datetime.strptime(time_str, "%H:%M")
        variation = random.randint(-5, 5)
        new_time = time_obj + timedelta(minutes=variation)
        return new_time.strftime("%H:%M")

    def adjust_past_time(self, time_str):
        now = datetime.now()
        time_obj = datetime.strptime(time_str, "%H:%M").replace(
            year=now.year, month=now.month, day=now.day)

        if time_obj < now:
            # Zeit liegt in der Vergangenheit, plane für eine Minute später
            next_time = now + timedelta(minutes=1)
            return next_time.strftime("%H:%M")
        return time_str

    def schedule_tasks(self, username, password, login_time, logout_time, exit_after_logout=True, random_time=False):
        config = configparser.ConfigParser()
        config.read('setup.ini')
        use_random = config.getboolean('Zeiten', 'random_time', fallback=False)

        # Prüfe und passe Zeiten an
        login_time = self.adjust_past_time(login_time)
        logout_time = self.adjust_past_time(logout_time)

        if random_time or use_random:
            current_login = self.add_random_variation(login_time)
            current_logout = self.add_random_variation(logout_time)
            print("\nZeitplanung (mit Zufallsvariation):")
            print(f"Login:  {login_time} → {current_login}")
            print(f"Logout: {logout_time} → {current_logout}\n")
        else:
            current_login = login_time
            current_logout = logout_time
            print("\nZeitplanung (ohne Zufallsvariation):")
            print(f"Login:  {login_time}")
            print(f"Logout: {logout_time}\n")

        while True:
            schedule.clear()
            schedule.every().day.at(current_login).do(
                self.web_automation.login_to_portal,
                username,
                password
            )
            schedule.every().day.at(current_logout).do(
                self.web_automation.logout_from_portal,
                username,
                password
            )

            # Warte auf die geplanten Zeiten
            logout_done = False
            while not logout_done:
                schedule.run_pending()
                time.sleep(0.1)

                now = datetime.now()
                logout_hour, logout_minute = map(int, current_logout.split(':'))

                # Prüfe, ob der Logout ausgeführt werden soll
                if now.hour == logout_hour and now.minute >= logout_minute:
                    # Führe Logout aus
                    self.web_automation.logout_from_portal(username, password)
                    logout_done = True

                    if exit_after_logout:
                        print("\nTag abgeschlossen. Programm wird beendet...")
                        time.sleep(1)
                        self.web_automation.cleanup()
                        os._exit(0)
                    else:
                        next_day = datetime.now() + timedelta(days=1)
                        next_login = datetime.strptime(current_login, "%H:%M").replace(
                            year=next_day.year, month=next_day.month, day=next_day.day)
                        next_logout = datetime.strptime(current_logout, "%H:%M").replace(
                            year=next_day.year, month=next_day.month, day=next_day.day)

                        print(f"\nTag abgeschlossen. Nächster Login geplant für:")
                        print(f"Datum: {next_login.strftime('%d.%m.%Y')}")
                        print(f"Login-Zeit: {current_login}")
                        print(f"Logout-Zeit: {current_logout}")
                        print("\nWarte auf Mitternacht für den nächsten Tag...")

                        # Warte bis Mitternacht
                        midnight = next_day.replace(hour=0, minute=0, second=0, microsecond=0)
                        time.sleep((midnight - datetime.now()).total_seconds())
                        print("\nNeuer Tag beginnt. Starte Automatisierung...")
                        break

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Fehler: Nicht genügend Argumente")
        sys.exit(1)

    command = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    automation = AutomationManager()

    try:
        if command == "login":
            automation.web_automation.login_to_portal(username, password)
        elif command == "logout":
            automation.web_automation.logout_from_portal(username, password)
        elif command == "schedule":
            if len(sys.argv) < 6:
                print("Fehler: Zeitangaben fehlen")
                sys.exit(1)
            login_time = sys.argv[4]
            logout_time = sys.argv[5]
            exit_after_logout = True
            if len(sys.argv) > 6:
                exit_after_logout = sys.argv[6].lower() == 'true'
            automation.schedule_tasks(username, password, login_time, logout_time, exit_after_logout)
    except Exception as e:
        print(f"Fehler: {str(e)}")
        sys.exit(1)
    finally:
        automation.web_automation.cleanup()
