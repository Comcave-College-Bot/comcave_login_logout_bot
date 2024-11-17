import sys







import time







from datetime import datetime, timedelta







from web_automation import WebAutomation







import random















def get_random_time(base_time):







    """Berechnet eine zufällige Zeitvariation (±5 Minuten)"""







    base = datetime.strptime(base_time, "%H:%M")







    minutes_variation = random.randint(-5, 5)







    return base + timedelta(minutes=minutes_variation)















def wait_until_time(target_time):







    """Wartet bis zur angegebenen Zielzeit"""







    target = datetime.strptime(target_time, "%H:%M").time()







    while datetime.now().time() < target:







        time.sleep(1)















def main():







    if len(sys.argv) < 6:







        print("Nicht genügend Parameter!")







        return















    command = sys.argv[1]







    if command == "schedule":







        username = sys.argv[2]







        password = sys.argv[3]







        login_time = sys.argv[4]







        logout_time = sys.argv[5]







        random_variation = sys.argv[6].lower() == 'true' if len(sys.argv) > 6 else False















        print(f"Geplante Zeiten - Login: {login_time}, Logout: {logout_time}")







        # Wenn Zufallsvariation aktiviert ist, berechne zufällige Zeiten







        if random_variation:







            login_time = get_random_time(login_time).strftime("%H:%M")







            logout_time = get_random_time(logout_time).strftime("%H:%M")







            print(f"Zufällige Zeiten - Login: {login_time}, Logout: {logout_time}")















        # Warte bis zur Login-Zeit







        print("Warte auf Login-Zeit...")







        print(f"Warte bis {login_time}")







        wait_until_time(login_time)







        







        # Login durchführen







        print("Starte Login...")







        automation = WebAutomation()







        if not automation.login_to_portal(username, password):







            automation.cleanup()







            return















        # Warte bis zur Logout-Zeit







        print("Warte auf Logout-Zeit...")







        print(f"Warte bis {logout_time}")







        wait_until_time(logout_time)







        







        # Logout durchführen







        print("Starte Logout...")







        if not automation.logout_from_portal(username, password):







            automation.cleanup()







            return















        # Cleanup







        automation.cleanup()















if __name__ == "__main__":







    main() 






