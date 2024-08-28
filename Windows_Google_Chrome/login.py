from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

def login(username, password):
    chrome_service = Service(r'C:\Users\CC-Student\projects\comcave_login_bot\chromedriver.exe')
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
    username = sys.argv[1]
    password = sys.argv[2]
    login(username, password)
