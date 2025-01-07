from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # Automatically manage ChromeDriver
from selenium.webdriver.chrome.options import Options  # To pass arguments to Chrome
import time
import urllib.parse  # To encode the message
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from email_sender import  send_email

try:
    # Set up Chrome options to use your Chrome profile
    chrome_options = Options()
    chrome_profile_path = "/Users/user/Library/Application Support/Google/Chrome/User Data/"  # Adjust this path
    chrome_options.add_argument(f"user-data-dir={chrome_profile_path}")
    chrome_options.add_argument("profile-directory=Profile 1")  # Replace with the correct profile name (e.g., "Default")

    # chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    # chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (optional)
    # chrome_options.add_argument("--no-sandbox")  # Bypass OS security model (useful
    # Docker)
    # chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource issues in containers

    # Use webdriver_manager to automatically download and manage ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Prepare the phone number and message # 393756497700
    phone_number = "3(9)3 7564977 00"  # Replace with the recipient's phone number

    # Sanitize numer
    if "(" in phone_number or ")" in phone_number:
        numberL = phone_number.replace("(", "")
        numberR = numberL.replace(")", "")
        Newphone_number = numberR.replace(" ", "")

        if "+" not in Newphone_number:
            phone_number = "+" + Newphone_number
            print(phone_number)



    message = "prodotto arrivato"  # Replace with your message
    encoded_message = urllib.parse.quote(message)  # URL-encode the message

    # Construct the WhatsApp API URL
    whatsapp_url = f"https://api.whatsapp.com/send?phone={phone_number}&text={encoded_message}"
    # Open WhatsApp Web using the link
    driver.get(whatsapp_url)

    # USE presence_of_element_located tp find element with new condition, time.sleep is not executed until xpath was found
    WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.XPATH, "//*[@id='action-button']")))
    continuewapp = driver.find_element("xpath", "//*[@id='action-button']")
    continuewapp.click()
    time.sleep(5)

    WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.XPATH, "//*[@id='fallback_block']/div/div/h4[2]")))
    continuewappWeb = driver.find_element("xpath", "//*[@id='fallback_block']/div/div/h4[2]")
    continuewappWeb.click()
    time.sleep(11)

    try:
        CheckIfNumerIsValid = WebDriverWait(driver, 30).until(
            ec.presence_of_element_located((By.XPATH, "//*[@id='app']/div/span[2]/div/span/div/div/div/div")))
        raise Exception("numer is not valid")
    except TimeoutException:
        print("numer is ok")

    # check if you need toLogin
    try:
        checklogin = WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.XPATH, "//*[@id='app']/div/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div[1]/div[1]")))
        # If the element is found, login is required
        raise Exception("Need to login")
    except TimeoutException:
        WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.XPATH, "//*[@id='main']/footer/div[1]/div/span/div/div[2]/div[2]")))
        Sendwapp = driver.find_element("xpath", "//*[@id='main']/footer/div[1]/div/span/div/div[2]/div[2]")

        Sendwapp.click()
        if Sendwapp:
            sendIsOK = "OK"
            print(sendIsOK)
        time.sleep(30)

        # Close the driver
        driver.quit()

except Exception as e:
    print("qualcosa e andato storto: ", e)
    error_script = f"An error occurred:\n\n{str(e)}"
    # Call send_email with just the body
    send_email(error_script)