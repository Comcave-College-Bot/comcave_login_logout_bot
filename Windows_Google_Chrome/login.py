import subprocess
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Überprüft und installiert Pakete, falls sie nicht vorhanden sind
def check_and_install_packages():
    try:
        import selenium
    except ImportError:
        install_package('selenium')

    try:
        from webdriver_manager.chrome import ChromeDriverManager
    except ImportError:
        install_package('webdriver-manager')

# Funktion zur Installation von Python-Paketen
def install_package(package_name):
    try:
        print(f"Installiere {package_name}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])
        print(f"{package_name} wurde erfolgreich installiert.")
    except Exception as e:
        print(f"Fehler bei der Installation von {package_name}: {e}")

# Führt den Login-Vorgang durch
def login(username, password):
    from webdriver_manager.chrome import ChromeDriverManager
    chrome_service = Service(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--incognito")

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    try:
        driver.get("https://portal.cc-student.com/index.php?cmd=login")
        username_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "login_username"))
        )

        password_input = driver.find_element(By.NAME, "login_passwort")
        username_input.send_keys(username)
        password_input.send_keys(password)

        login_button = driver.find_element(By.XPATH, "//input[@type='submit']")
        login_button.click()

        zeiterfassung_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'cmd=kug')]"))
        )
        zeiterfassung_button.click()

        zeiterfassung_oeffnen_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@name, 'showDialogButton')]"))
        )
        zeiterfassung_oeffnen_button.click()

        kommen_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@class='buttonKommen']"))
        )

        driver.execute_script("arguments[0].click();", kommen_button)
        print("Kommen Button erfolgreich geklickt!")

    except Exception as e:
        print(f"Fehler aufgetreten: {str(e)}")
        print(driver.page_source)
    finally:
        driver.quit()

if __name__ == "__main__":
    check_and_install_packages()
    username = sys.argv[1]
    password = sys.argv[2]
    login(username, password)
