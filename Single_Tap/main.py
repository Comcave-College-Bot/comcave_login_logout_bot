import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def setup_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    return driver

def login(username, password):
    driver = setup_driver()
    try:
        # Login-Seite öffnen
        driver.get("https://portal.cc-student.com/index.php?cmd=login")
        print("Login-Seite geöffnet")

        time.sleep(1)  # Kurz warten, bis die Seite vollständig geladen ist

        # Login-Daten eingeben
        print("Gebe Anmeldedaten ein...")
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "login_username"))
        )
        password_input = driver.find_element(By.NAME, "login_passwort")
        username_input.send_keys(username)
        password_input.send_keys(password)

        time.sleep(0.5)  # Kurz warten nach Eingabe

        # Login-Button klicken
        print("Führe Login durch...")
        login_button = driver.find_element(By.XPATH, "//input[@type='submit']")
        driver.execute_script("arguments[0].click();", login_button)

        time.sleep(1)  # Warten nach Login

        # Zeiterfassung öffnen
        print("Öffne Zeiterfassung...")
        zeiterfassung_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'cmd=kug')]"))
        )
        driver.execute_script("arguments[0].click();", zeiterfassung_button)

        time.sleep(0.5)  # Warten nach Klick

        zeiterfassung_oeffnen_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@name, 'showDialogButton')]"))
        )
        driver.execute_script("arguments[0].click();", zeiterfassung_oeffnen_button)

        time.sleep(0.5)  # Warten nach Dialog-Öffnung

        # Kommen-Button klicken
        print("Klicke Kommen-Button...")
        kommen_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@class='buttonKommen']"))
        )
        driver.execute_script("arguments[0].click();", kommen_button)
        print("Login erfolgreich")

    except Exception as e:
        print(f"Login nicht möglich: {str(e)}")
    finally:
        driver.quit()

def logout(username, password):
    driver = setup_driver()
    try:
        print("Starte Logout-Prozess...")

        # Login-Seite öffnen
        print("Öffne Login-Seite für Logout...")
        driver.get("https://portal.cc-student.com/index.php?cmd=login")

        time.sleep(1)  # Kurz warten, bis die Seite vollständig geladen ist

        # Login-Daten eingeben
        print("Gebe Anmeldedaten ein...")
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "login_username"))
        )
        password_input = driver.find_element(By.NAME, "login_passwort")
        username_input.send_keys(username)
        password_input.send_keys(password)

        time.sleep(0.5)  # Kurz warten nach Eingabe

        # Login-Button klicken
        print("Führe Login für Logout durch...")
        login_button = driver.find_element(By.XPATH, "//input[@type='submit']")
        driver.execute_script("arguments[0].click();", login_button)

        time.sleep(1)  # Warten nach Login

        # Zeiterfassung öffnen
        print("Öffne Zeiterfassung...")
        zeiterfassung_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'cmd=kug')]"))
        )
        driver.execute_script("arguments[0].click();", zeiterfassung_button)

        time.sleep(0.5)  # Warten nach Klick

        zeiterfassung_oeffnen_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@name, 'showDialogButton')]"))
        )
        driver.execute_script("arguments[0].click();", zeiterfassung_oeffnen_button)

        time.sleep(0.5)  # Warten nach Dialog-Öffnung

        # Gehen-Button klicken
        print("Klicke Gehen-Button...")
        gehen_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@class='buttonGehen']"))
        )
        driver.execute_script("arguments[0].click();", gehen_button)
        print("Logout erfolgreich")

    except Exception as e:
        print(f"Logout nicht möglich: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Nicht genügend Parameter!")
        print("Verwendung: main.py <command> <username> <password>")
        sys.exit(1)

    command = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    if command == "login":
        login(username, password)
    elif command == "logout":
        logout(username, password)
    else:
        print(f"Unbekannter Befehl: {command}")