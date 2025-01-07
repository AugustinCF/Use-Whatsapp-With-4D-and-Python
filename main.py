import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import urllib.parse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from email_sender import  send_email

try:
    # Get the phone number and message from the arguments
    phone_number = sys.argv[1]  # Phone number passed as the first argument

    # Sanitize numer
    if "(" in phone_number or ")" in phone_number:
        numberL = phone_number.replace("(", "")
        numberR = numberL.replace(")", "")
        Newphone_number = numberR.replace(" ", "")

        if "+" not in Newphone_number:
            phone_number = "+" + Newphone_number
            print(phone_number)

    message = sys.argv[2]       # Message passed as the second argument

    # enable print to see in 4D respondse
    # print(f"Phone Number: {phone_number}")# 4D var
    # print(f"Message: {message}")# 4D var

    # Set up Chrome options to use your Chrome profile
    # Chromne driver adesso deve essere installao con pip o pip3 // NON E PIU NECESSARIO  SCARICARE
    chrome_options = Options()
    chrome_profile_path = "/Users/magazzino_lol_gen_2/Library/Application Support/Google/Chrome/Profile 1"  # use profile chrome to use  session
    chrome_options.add_argument(f"user-data-dir={chrome_profile_path}")
    chrome_options.add_argument("profile-directory=Profile 1")  # u can use  ("Default")
    #### hide chrome browser
    # chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    # chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (optional)
    # chrome_options.add_argument("--no-sandbox")  # Bypass OS security model (useful in Docker)
    # chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource issues in ≤
    #####
    # Use webdriver_manager to automatically download and manage ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # URL encode the message
    encoded_message = urllib.parse.quote(message)

    # Construct the WhatsApp API URL
    whatsapp_url = f"https://api.whatsapp.com/send?phone={phone_number}&text={encoded_message}"
    driver.get(whatsapp_url)

    # Convention is to use time sleep 5 sec, u can use 1 sec but is not recommended
    # USE presence_of_element_located tp find element with new condition, time.sleep is not executed until xpath was found
    WebDriverWait(driver, 30).until(
        ec.presence_of_element_located((By.XPATH, "//*[@id='action-button']"))
    )
    continuewapp = driver.find_element("xpath", "//*[@id='action-button']")
    continuewapp.click()
    time.sleep(5)


    WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.XPATH, "//*[@id='fallback_block']/div/div/h4[2]")))
    continuewappWeb = driver.find_element("xpath", "//*[@id='fallback_block']/div/div/h4[2]")
    continuewappWeb.click()
    time.sleep(5)

    # check if you need toLogin
    try:
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, "//*[@id='app']/div/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div[1]/div[1]")))
        # If the element is found, login is required
        raise Exception("Need to login")

    except TimeoutException:
        WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.XPATH, "//*[@id='main']/footer/div[1]/div/span/div/div[2]/div[2]")))
        Sendwapp = driver.find_element("xpath", "//*[@id='main']/footer/div[1]/div/span/div/div[2]/div[2]")
        Sendwapp.click()
        if Sendwapp:
            # print("messaggio mandato con successo !")
            sendIsOK = "OK"
            print(sendIsOK)


        time.sleep(5)

        # Close the driver
        driver.quit()

except Exception as e:
    print("qualcosa e andato storto: ", e)
    error_script = f"An error occurred:\n\n{str(e)}"
    # Call send_email with just the body
    send_email(error_script)
