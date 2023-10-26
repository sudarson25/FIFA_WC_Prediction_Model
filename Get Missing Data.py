from selenium import webdriver
# Selenium library helps automate web browsers
# "Automating web browsers" means using code to perform actions in a web browser just like a human would.
# This includes tasks like opening web pages, clicking links, filling out forms, and extracting data from web pages.

# The webdriver module, specifically, is a core component of Selenium that allows you to create and interact
# with web browser instances in your code.
# This module to control the browser.
# The webdriver module provides methods for simulating interactions with web pages,
# such as clicking buttons, submitting forms, and extracting data.

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.chrome.service import Service

# Here, you're importing a specific class called 'Service' from a submodule called chrome.service within
# the Selenium library.
# This class helps configure and manage the settings for the Chrome web browser when you're automating it.
# It's part of the setup to make sure your automation works correctly with Chrome.

import time
import pandas as pd

# chromedriver.exe # This is the file that will allow your script to control the Chrome browser.
# Setting the 'path' variable to the file path of the Chrome WebDriver executable
path = 'C:\\Users\\sudar\\Downloads\\chromedriver-win64\\chromedriver.exe'

# 'service' is a variable used to store an instance(object) of the 'Service' class from the Selenium library.
# Creating a new instance of the 'Service' class from Selenium
# 'executable_path' parameter takes the file path to the Chrome WebDriver executable.
service = Service(executable_path=path)

# 'driver' variable will store an instance(object) of the Chrome web browser controlled by Selenium.
# service is a parameter that takes an instance of the Service class as argument
driver = webdriver.Chrome(service=service)


def get_misssing_data(year):
    web = f'https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup'

    # This line tells the driver to open the web page specified by the web URL.
    # It's like manually typing a web address into the browser.
    driver.get(web)

    # find_elements() is used to find multiple web elements on the web page
    # xpath is a powerful language for selecting elements in an HTML document.

    # xpath language is used to find and collect elements on the web page that match one of two criteria:
    # either they have the align attribute set to "right" or
    # they have a style attribute with the value text-align:right.

    # matches is a list that can hold a collection of web elements found on a web page using the specified XPath expression.
    # Each element in the list is represented as an object with attributes and methods

    matches = driver.find_elements(by='xpath', value='//td[@align="right"]/.. | //td[@style="text-align:right;"]/..')
    # matches = driver.find_elements(by='xpath', value='//tr[@style="font-size:90%"]')

    home = []
    score = []
    away = []

    for match in matches:
        # For each match, you're finding and collecting the text inside the first, second, and third
        # table cells (td) within that match.
        home.append(match.find_element(by='xpath', value='./td[1]').text)
        score.append(match.find_element(by='xpath', value='./td[2]').text)
        away.append(match.find_element(by='xpath', value='./td[3]').text)

    dict_football = {'home': home, 'score': score, 'away': away}
    df_football = pd.DataFrame(dict_football)
    df_football['year'] = year
    # You're adding a pause (2 seconds in this case) to wait before moving on.
    # This can be useful to allow the webpage to fully load.
    time.sleep(2)
    return df_football


years = [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974,
         1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014,
         2018]

fifa = [get_misssing_data(year) for year in years]
# You're telling the Chrome browser to close. This is like shutting down the browser after you've finished using it.
driver.quit()
df_fifa = pd.concat(fifa, ignore_index=True)
df_fifa.to_csv("FIFA_WC_Missing_Data.csv", index=False)
