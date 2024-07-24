import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import requests
from bs4 import BeautifulSoup
import re


class organizeData():
    def __init__(self):
        self.driver = None
        try:
            self.options = webdriver.ChromeOptions()
            self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
            self.options.add_experimental_option("useAutomationExtension", False)
        except Exception as e:
            print("Error setting up options")

        try:
            self.driver = webdriver.Chrome(options=self.options)
        except Exception as e: 
            print("Error creating webdriver instance")
        


    def sign_in(self, email: str, password: str):

        self.driver.get('https://www.linkedin.com/')
        self.driver.maximize_window()
        time.sleep(1)
        try:
            signInOneXPATH = '//a[@class="nav__button-secondary btn-md btn-secondary-emphasis"]'
            signInOne = self.driver.find_element(By.XPATH, signInOneXPATH)
            if signInOne is not None:
                signInOne.click()
        except Exception as e: 
            print("Couldn't find first sign in button")

        time.sleep(1)

        try:
            inputXPATH = '//input[@id="username"]'
            emailInput = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, inputXPATH)))
            emailInput = self.driver.find_element(By.XPATH, inputXPATH)
            emailInput.click()
            emailInput.clear()
            emailInput.send_keys(email)

            time.sleep(1)
            passwordXPATH = '//input[@id="password"]'
            passwordInput = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, passwordXPATH)))
            passwordInput = self.driver.find_element(By.XPATH, passwordXPATH)
            passwordInput.click()
            passwordInput.clear()
            passwordInput.send_keys(password)

            signInButtonTwoXPATH = '//*[@id="organic-div"]/form/div[3]/button'
            signInButtonTwo = self.driver.find_element(By.XPATH, signInButtonTwoXPATH)
            signInButtonTwo.click()
        except Exception as e: 
            print("Error entering email and password")

        
        msgXPATH = '//*[@id="global-nav"]/div/nav/ul/li[4]/a/div'
        itWorks = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, msgXPATH)))
        itWorks = self.driver.find_element(By.XPATH, msgXPATH)
        assert itWorks is not None, "Sign in credentials incorrect"

        

    def get_company_and_position(self, csvFile: str) -> dict:
        with open(csvFile, mode='r', newline='') as file:
            csvReader = csv.reader(file)

            self.sign_in(email="hiring@brighthire.ai", password="XZP5mac5zdw-cda4ktk")
            company_and_position = dict()

            for row in csvReader:

                url = row[0]
                if url[0] != 'h':
                    continue

                time.sleep(2)

                self.driver.get(url=url)

                time.sleep(3)

                companyXPATH = '//*[@id="profile-content"]/div/div[2]/div/div/main/section[1]/div[2]/div[2]/ul/li[1]/button'
                try:
                    company_button = None
                    company_button = self.driver.find_element(By.XPATH, companyXPATH)
                    if company_button is None:
                        raise e
                    
                except Exception as e:
                    print(f'Error Finding Company {row[3]}')

                

                company_name = company_button.text

                time.sleep(1)

                curr_url = self.driver.current_url
                self.driver.get(curr_url + '/details/experience/')

                #NOW ON EXPERIENCES PAGE
                r = requests.get(self.driver.current_url)

                time.sleep(2)
                
                soup = BeautifulSoup(r.text, 'html.parser')
                position_html = None
                position_html = soup.find('span', attrs=({"class": "pvs-entity__caption-wrapper"})).parent.parent.parent.find(
                    'div', attrs=({"class": "display-flex align-items-center mr1 hoverable-link-text t-bold"}))
                if position_html is None:
                    print("BS4 DIDN'T WORK")
                else:
                    print(position_html)
                    

                position = position_html.text
                print(position)

                company_and_position = {company_name, position}
                company_and_position[row[3]] = company_and_position
                print(row[3] + ": " + company_and_position[row[3]][0] + ", " + company_and_position[row[3]][1])

            file.close()
            return company_and_position