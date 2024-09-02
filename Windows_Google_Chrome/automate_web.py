import subprocess
import sys
import configparser
import os
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Function to read configuration from setup.ini
def read_config(key, section='DEFAULT'):
    config = configparser.ConfigParser()
    config.read('setup.ini')
    return config[section].get(key, '')

# Function to write configuration to setup.ini
def write_config(key, value, section='DEFAULT'):
    config = configparser.ConfigParser()
    config.read('setup.ini')
    if section not in config:
        config[section] = {}
    config[section][key] = value
    with open('setup.ini', 'w') as configfile:
        config.write(configfile)

# Function to install Python packages
def install_package(package_name):
    try:
        print(f"Installing {package_name}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])
        print(f"{package_name} was successfully installed.")
        return True
    except Exception as e:
        print(f"Error installing {package_name}: {e}")
        return False

# Function to check and install required packages
def check_and_install_packages():
    selenium_installed = False
    webdriver_manager_installed = False

    try:
        import selenium
        selenium_installed = True
    except ImportError:
        print("selenium is not installed.")

    try:
        from webdriver_manager.chrome import ChromeDriverManager
        webdriver_manager_installed = True
    except ImportError:
        print("webdriver-manager is not installed.")

    if not selenium_installed:
        if install_package('selenium'):
            write_config('selenium_installed', 'true')
        else:
            print("Installation of selenium failed.")
    
    if not webdriver_manager_installed:
        if install_package('webdriver-manager'):
            write_config('webdriver_manager_installed', 'true')
        else:
            print("Installation of webdriver-manager failed.")

# Function to check if today is a holiday or vacation
def is_holiday_or_vacation():
    today = datetime.now().date()
    holiday_str = read_config('dates', section='Urlaub')
    legal_holiday_str = read_config('dates', section='Gesetzliche Feiertage')
    holiday_ranges = parse_date_ranges(holiday_str)
    legal_holiday_ranges = parse_date_ranges(legal_holiday_str)
    
    for start, end in holiday_ranges + legal_holiday_ranges:
        if start <= today <= end:
            print(f"No action, as today ({today.strftime('%d.%m.%Y')}) is a holiday or vacation.")
            return True
    return False

# Function to parse date ranges from setup.ini
def parse_date_ranges(date_str):
    date_ranges = []
    if not date_str:
        return date_ranges

    for part in date_str.split(','):
        try:
            dates = part.split('-')
            start_date = datetime.strptime(dates[0].strip(), '%d.%m.%Y').date()
            end_date = start_date if len(dates) == 1 else datetime.strptime(dates[1].strip(), '%d.%m.%Y').date()
            date_ranges.append((start_date, end_date))
        except ValueError:
            print(f"Invalid date format: {part}. Expected: DD.MM.YYYY or DD.MM.YYYY-DD.MM.YYYY.")
    return date_ranges

# Function to perform web automation
def automate_web():
    if is_holiday_or_vacation():
        return

    chrome_service = Service(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--incognito")

    try:
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    except Exception as e:
        print(f"Error starting WebDriver: {e}")
        return

    username = read_config("username", section="Benutzerdaten")
    password = read_config("password", section="Benutzerdaten")

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

        gehen_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@class='buttonGehen']"))
        )
        driver.execute_script("arguments[0].click();", gehen_button)
        print("Gehen button clicked successfully!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print(driver.page_source)
    finally:
        driver.quit()

    next_action_time = datetime.now() + timedelta(days=1)
    print(f"Next planned action on: {next_action_time.strftime('%d.%m.%Y %H:%M')}")

# Main function
def main():
    check_and_install_packages()
    automate_web()

if __name__ == "__main__":
    main()
