"""
Helper functions for the Bank of America module.
"""
import os
import pathlib
import configparser
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WINDOWS_OS = "WINDOWS"
CHROMEDRIVERS_DIRECTORY = os.path.join(
    pathlib.Path(__file__).parent.absolute(), 
    "chromedrivers"
)


def create_webdriver():
    """
    Creates a selenium webdriver object given the executable path and options.
    :param executable_path: The path to a valid selenium webdriver executable.
    :param options: The browser options to use for the selenium webdriver.
    :return: Selenium webdriver object.
    """
    browser = webdriver.Chrome(
        executable_path=get_chromedriver_path(),
        options=get_chromedriver_options()
    )
    return browser


def get_chromedriver_path():
    """
    Depending on the operating system this module is running in, this
    function returns the proper chromedriver executable path per the
    operating system.
    :return: For Windows, a windows specific chromedriver executable.
        For MacOS, a MacOS specific chromedriver executable.
    """
    current_operating_system = platform.system()
    if current_operating_system.upper() == WINDOWS_OS:
        path = os.path.join(CHROMEDRIVERS_DIRECTORY, "windows_chromedriver")
    else:
        path = os.path.join(CHROMEDRIVERS_DIRECTORY, "macOS_chromedriver")
    return path


def get_chromedriver_options():
    """
    Creates and returns a selenium chrome Options object containing the
    necessary options for the selenium webdriver.
    :return: Selenium Options object.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")
    return options


def login(browser, credentials):
    """
    Using the provided browser *browser*, this function enters the login
    credentials and, if needed, the answers to security questions, then
    logs into the user's Bank of America account.
    :param browser: Selenium webdriver object.
    :param credentials: A dictionary containing the user's Bank of America
        credentials and security question answers.
    :return: Updated selenium webdriver object.
    """
    current_url = browser.current_url
    browser.find_element_by_xpath('//*[@id="onlineId1"]').send_keys(
        credentials.get('username')
    )
    browser.find_element_by_xpath('//*[@id="passcode1"]').send_keys(
        credentials.get('password')
    )
    browser.find_element_by_xpath('//*[@id="signIn"]').click()
    WebDriverWait(browser, 10).until(EC.url_changes(current_url))
    new_url = browser.current_url
    if "https://secure.bankofamerica.com/myaccounts" not in new_url:
        print("[bank_of_america.__init__.login]: Security questions are required.")
        return answer_security_questions(browser, credentials)
    return browser


def answer_security_questions(browser, credentials):
    """
    In the event that Bank of America is requiring the end user to input
    an answer to a security question, this function takes care of it
    assuming the question and the answer to the question have been provided
    by the user in the '.env'.
    :param browser: Selenium webdriver object.
    :param credentials: A dictionary containing the user's Bank of America
        credentials and security question answers.
    :return: Updated selenium webdriver object.
    """
    question_answered = False
    security_questions = credentials.get('security_questions')
    for question in security_questions.keys():
        if question.lower() in browser.page_source.lower():
            browser.find_element_by_id(
                'tlpvt-challenge-answer'
            ).send_keys(
                security_questions.get(question)
            )
            question_answered = True
    if question_answered:
        browser.find_element_by_id('yes-recognize').click()
        browser.find_element_by_id('verify-cq-submit').click()
    else:
        print(
            "[bank_of_america.__init__.answer_security_question]: Security "
            "question was never answered. Check the 'security-question-error.png' "
            "screenshot."
        )
        browser.get_screenshot_as_file("security-question-error.png")
    return browser


def get_credentials():
    """
    Gathers all the necessary Bank of America credentials from the .env
    file and saves them to a dict object for use later.
    :return: Dict containing Bank of America credentials and security
        questions in the format: {
            'username': 'B of A username',
            'password': 'B of A password',
            'security_questions': {
                'question1': 'answer1'
            }
        }
    """
    env_path = os.path.join(
        pathlib.Path(__file__).parent.parent.absolute(),
        ".env"
    )
    try:
        config_parser = configparser.ConfigParser()
        config_parser.read(env_path)
        credentials = dict()
        credentials['username'] = config_parser.get(
            "credentials", 
            "BANK_OF_AMERICA_USERNAME"
        )
        credentials['password'] = config_parser.get(
            "credentials", 
            "BANK_OF_AMERICA_PASSWORD"
        )
        credentials['security_questions'] = {}
        for question, answer in config_parser.items('security_questions'):
            credentials['security_questions'][question] = answer
        return credentials
    except Exception as err:
        print(
            "[bank_of_america.__init__.get_credentials]: Error getting Bank of America "
            "credentials. Please ensure your '.env' file is setup properly. "
            "Error: {}".format(err)
        )
        exit()
