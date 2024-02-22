from faker import Faker
import random
import time
import string
from datetime import datetime
# from omkar_temp_mail import TempMail
from bs4 import BeautifulSoup
import re
from pynator import SMSNator, EmailNator


from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import os

import chromedriver_autoinstaller
from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from fake_useragent import UserAgent
# from fake_headers import Headers
# from browsermobproxy import Server
import requests

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# variables
facebook_signup_url = "https://facebook.com/signup"
# image_folder_directory = ""
# image_file_paths = [os.path.join(image_folder_directory, filepath) for filepath in os.listdir(image_folder_directory) if os.path.isfile(os.path.join(image_folder_directory, filepath))]
client_1 = SMSNator()
client_2 = EmailNator()


def wait_for_page(driver, class_name='fb_content', timeout=30):
    """
    Waits for an element with the given class_name to be visible on the page.

    Parameters:
        driver (webdriver): The Selenium WebDriver instance.
        class_name (str): The class name of the element to wait for, default = fb_content
        timeout (int): How long to wait for the element to appear, in seconds, default = 30

    Returns:
        WebElement: True, or False if not found within the timeout.
    """
    try:
        # Wait for the element to be visible
        element = EC.visibility_of_element_located((By.CLASS_NAME, class_name))
        WebDriverWait(driver, timeout).until(element)
        return True
    except TimeoutException:
        print(f"Timed out waiting for element with class {class_name} to appear.")
        return False

def check_connectivity(proxy):
    try:
        proxy = {'https': proxy}
        response = requests.get("https://ident.me",proxies=proxy, verify=False)
        # print(f'Current Public IP: {response.json().get("query")}')
        print(f'Current Public IP : {response.text}')
        return True
    except:
        return False
    
def start_driver():
    """
    Initializes and returns a Chrome WebDriver

    This function utilizes `chromedriver_autoinstaller` to ensure the ChromeDriver is installed 
    The returned WebDriver is configured with several options including disabling the GPU, sandbox, and dev shm usage, 
    along with adjustments intended to prevent the detection of automated browser control
    It also makes sure to change the user agent but only when the function is called

    Returns:
        WebDriver: An instance of Chrome WebDriver configured with specified options for automation tasks.
    """
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("--dom-automation=disabled")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    ua = UserAgent()
    user_agent = ua.random
    chrome_options.add_argument(f'user-agent={user_agent}')

    with open('./Desktop/https.txt', 'r') as public_proxy_file:
        proxies = [":".join(proxy.split(":")[:2]).strip() for proxy in public_proxy_file]
    with open('./Desktop/https2.txt', 'r') as public_proxy_file2:
        for proxy in public_proxy_file2:
            proxy = proxy.strip()
            proxies.append(proxy)
    with open('./Desktop/https3.txt', 'r') as public_proxy_file3:
        for proxy in public_proxy_file3:    
            proxy = proxy.strip()
            proxies.append(proxy)
    while True:
        proxy = f"https://{random.choice(proxies)}"
        working = check_connectivity(proxy)
        if working:
            break
    chrome_options.add_argument(f'--proxy-server={proxy}')
    chrome_options.add_argument('--ignore-certificate-errors')

    driver = webdriver.Chrome(options=chrome_options)

    return driver

def generate_random_data():
    """
    Generates random user data including first name, surname, email, and password using the Faker and random libraries

    Returns:
        tuple: Contains the generated first name, surname, email, and password.
    """
    # Initialize Faker
    fake = Faker()
    # Generate a random first name
    first_name = fake.first_name()
    # Generate a random surname
    surname = fake.last_name()

    # generate a phone number
    phone = client_1.generate_number()
    email = client_2.generate_email()

    # # Generate a random email
    # username = fake.user_name()
    # valid_domains =  ['1secmail.com', '1secmail.org', '1secmail.net', 'kzccv.com', 'qiott.com', 'wuuvo.com', 'icznn.com'] # from the library
    # domain = fake.random_element(valid_domains)
    # email = f"{username}@{domain}"

    # Define the characters to include in the password
    letters = string.ascii_letters
    numbers = string.digits
    punctuation = "!?"  # Specific punctuation marks as mentioned by facebook

    # Ensure the password includes at least one of each required character type
    password_chars = [
        random.choice(letters),
        random.choice(numbers),
        random.choice(punctuation)
    ]
    # Fill the rest of the password length with a random selection of all allowed characters
    for _ in range(6 - len(password_chars)):
        password_chars.append(random.choice(letters + numbers + punctuation))
    # Shuffle the characters to ensure randomness
    random.shuffle(password_chars)
    # Join the characters into a single string
    password = ''.join(password_chars)

    return first_name, surname, email, phone, password


def get_code_by_email(email):
    # body = TempMail.get_body(email)
    # soup = BeautifulSoup(body, 'html.parser')
    # confirmation_code = soup.get_text()
    # code = re.search(r'\d+', confirmation_code).group()
    # return code
    messages = client_2.get_messages(email)
    for message in messages:
        message_body = client_2.get_message(email, message.message_id)
        if 'facebook' in message_body:
            print(message)
            code = re.search(r'\d+', message_body).group()
            return code
        else:
            pass

def get_code_by_phone(phone_number):
    messages = client_1.get_messages(phone_number)
    for message in messages:
        if 'facebook' in message.message:
            print(message)
            code = re.search(r'\d+', message).group()
            return code
        else:
            pass

# def get_a_selfie():
#     response = google_images_download.googleimagesdownload()
#     arguments = {"keywords":"test","limit":20,"print_urls":True, "chromedriver": chromedriver_autoinstaller.install()}
#     paths = response.download(arguments)
#     return paths 

def fill_fields(driver: webdriver, first_name, surname, email, password):
    """
    Fills in registration fields with provided user details and randomly selects date of birth and gender.

    Parameters:
        driver: Selenium WebDriver instance to interact with the webpage.
        first_name (str): User's first name.
        surname (str): User's surname.
        email (str): User's email address.
        password (str): User's password.
    """

    # Locate the input fields by their names attribute and input the required data
    first_name_field = driver.find_element(By.NAME, 'firstname')
    first_name_field.clear()  # Clear any pre-filled value
    first_name_field.send_keys(first_name)

    last_name_field = driver.find_element(By.NAME, 'lastname')
    last_name_field.clear()
    last_name_field.send_keys(surname)

    email_field = driver.find_element(By.NAME, 'reg_email__')
    email_field.clear()
    email_field.send_keys(email)

    email_field_confirmation = driver.find_element(By.NAME, 'reg_email_confirmation__')
    email_field_confirmation.clear()
    email_field_confirmation.send_keys(email)

    password_field = driver.find_element(By.NAME, 'reg_passwd__')
    password_field.clear()
    password_field.send_keys(password)

    # Locate the dropdown by its id
    day_dropdown = Select(driver.find_element(By.ID, 'day'))
    # Get all options within the dropdown
    day_options = day_dropdown.options
    valid_day_options = [option for option in day_options if int(option.text) <= 28] # avoid selecting from higher numbers to avoid the mapping of month and its maximum days
    # Select a random option
    random_day = random.choice(valid_day_options)
    day_dropdown.select_by_visible_text(random_day.text)

    month_dropdown = Select(driver.find_element(By.ID, 'month'))
    month_options = month_dropdown.options
    random_month = random.choice(month_options)
    month_dropdown.select_by_visible_text(random_month.text)

    # Calculate the current year minus 14 years (legal age is 13, no strict conditions for months and days so minus 14)
    current_year = datetime.now().year
    latest_valid_year = current_year - 14
    year_dropdown = Select(driver.find_element(By.ID, 'year'))
    valid_options = [option for option in year_dropdown.options if int(option.text) <= latest_valid_year]
    random_year = random.choice(valid_options)
    year_dropdown.select_by_visible_text(random_year.text)

    # Map gender labels to their corresponding XPath expressions
    gender_xpath_map = {
        'Female':   "//*[@name='sex' and @value='1'] ",
        'Male': "//*[@name='sex' and @value='2']"
    }
    # Randomly select a gender label
    gender_label = random.choice(list(gender_xpath_map.keys()))
    # Construct the XPath expression for the selected gender
    radio_button_xpath = gender_xpath_map[gender_label]
    radio_button = driver.find_element(By.XPATH, radio_button_xpath)
    radio_button.click()

# def captcha_solver(driver):
#     driver.get("https://chromewebstore.google.com/detail/buster-captcha-solver-for/mpbjkejclgfgadiemmefgebjfooflfhl?hl=en")

def main():
    chromedriver_autoinstaller.install()

    driver = start_driver()
    time.sleep(5)

    driver.get(facebook_signup_url)
    ok_to_go = wait_for_page(driver) # use default values

    if ok_to_go:
        first_name, surname, email, phone, password = generate_random_data()
        print(phone)
        fill_fields(driver, first_name, surname, email, password)
        for _ in range(2):
            try:
                sign_up_button = driver.find_element(By.XPATH, "//div/button[@type='submit']")
                sign_up_button.click()
                time.sleep(10)
            except Exception as e:
                print(e)
                pass


        page_source = driver.page_source
        if 'We need more information' in page_source:
            press_continue_on_WeNeedMoreInfoPage = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div/div').click()
            time.sleep(20)
        
            # Implement Captcha Solver here and make sure to press the button below
            '''
            captcha_button = "/html/body/div[2]/div[3]/div[1]/div/div/span/div[1]"
            press_continue_on_CaptchaPage = "/html/body/div[1]/div/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[3]/div/div/div/div"
            '''
            # input email again
            driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[2]/div/label/div/div[2]/input').send_keys(email)
            # press the button
            send_login_code_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[3]/div/div/div/div")
            send_login_code_button.click()

            # get and write the code
            while True:
                try:
                    code = get_code_by_email(email)
                    code_area = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[2]/div/label/div/div/input")
                    code_area.send_keys(code)
                    time.sleep(2)
                    break
                except Exception as e:
                    print(e)
            # press next after email code
            press_next_on_enterCodeFromEmailPage = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[4]/div/div[2]/div[1]/div/div[1]")
            press_next_on_enterCodeFromEmailPage.click()

            # page appears again
            press_continue_on_WeNeedMoreInfoPage = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div/div').click()
            press_continue_on_WeNeedMoreInfoPage.click()

            # try:
            #     press_next = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[4]/div/div[2]/div[1]/div/div[1]").click()
            # except Exception:
            #     press_continue_on_WeNeedMoreInfoPage = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div/div').click()
                
                # press_continue = driver.find_element(By.NAME, "confirm").click() only if the code is asked for without a captcha

            # needs fixing: add number, press next loop if inner_error != "", get code, enter code, press continue
            page_source = driver.page_source
            if 'phone number' in page_source: 
                # enter phone number and press the button, no need to set a country
                code = get_code_by_phone(phone)
                driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[2]/div/label/div/div/input').send_keys(code)
                time.sleep(2)
                press_continue = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[4]/div/div/div/div/div[1]/div/span/span')
                press_continue.click()

            page_source = driver.page_source
            if 'Upload a verification selfie' in page_source:
                # upload a selfie or get it from a google search?
                upload_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div/div")
                # upload_button.send_keys(random.choice(image_file_paths))
                press_continue = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[4]/div/div/div/div/div[1]/div/span/span')
                press_continue.click()

            # finally, there is something to press too

        # IF i want to start with a phone number instead of an email
        # while True:
        #     try:
        #         inner_errors = driver.find_elements(By.XPATH, "/html/body/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div/div[1]/div[1]/div")
                
        #         for inner_error in inner_errors:
        #             inner_error = inner_error.text
        #             print(inner_error)
        #             if inner_error != '':
        #                 first_name, surname, email, password = generate_random_data()
        #                 fill_fields(driver, first_name, surname, email, password)
        #                 sign_up_button = driver.find_element(By.XPATH, "//div/button[@type='submit']")
        #                 sign_up_button.click()
        #                 time.sleep(30)
        #             else:
        #                 break
        #     except Exception:
        #         break

        else:
            while True:
                try:
                    code = get_code_by_email(email)
                    code_area = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[2]/div/label/div/div/input")
                    code_area.send_keys(code)
                    time.sleep(2)
                    break
                except Exception as e:
                    print(e)

            press_continue = driver.find_element(By.NAME, "confirm").click() # only if the code is asked for without a captcha
            time.sleep(600)
        driver.quit()

if __name__ == '__main__':
    main()
