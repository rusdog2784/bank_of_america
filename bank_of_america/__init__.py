"""
The Bank of America module's main functions.
"""
from bank_of_america.helper import create_webdriver, login, get_credentials


def get_checking_account_balance():
    """
    Function that uses selenium to connect to my Bank of America
    account and grab my current checking account balance.
    :return: Bank of America checking account balance.
    """
    try:
        browser = create_webdriver()
        browser.get("https://bankofamerica.com")
    except Exception as err:
        print(
            "[bank_of_america.__init__.get_checking_account_balance]: "
            "Error creating the webdriver: {}".format(err)
        )
        exit()
    browser = login(browser, get_credentials())
    try:
        checking_account_balance = browser.find_element_by_xpath(
            '//*[@id="Traditional"]/li[1]/div[1]/div[1]/span'
        ).text
        return checking_account_balance
    except Exception as err:
        print(
            "[bank_of_america.__init__.get_checking_account_balance]: "
            "Error finding the actual balance. So close... sorry. "
            "Error: {}".format(err)
        )
        exit()
