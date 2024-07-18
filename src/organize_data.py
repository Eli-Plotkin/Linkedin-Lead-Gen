import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


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
        


    def signIn(self, email: str, password: str):

        self.driver.get('https://www.linkedin.com/')
        time.sleep(1)
        try:
            signInOneXPATH = '//*[@href="https://www.linkedin.com/login?fromSignIn=true&trk=public_profile_not-found-log-in_nav-header-signin"]'
            signInOne = self.driver.find_element(By.XPATH, signInOneXPATH)
            if signInOne is not None:
                signInOne.click()
        except Exception as e: 
            print("Couldn't find first sign in button")

        time.sleep(1)

        try:
            correctSignInXPATH = '//*[@id="fastrack-div"]/div[4]/div[4]/a'
            correctSignIn = self.driver.find_element(By.XPATH, correctSignInXPATH)

            if correctSignIn is not None:
                correctSignIn.click()
        except Exception as e: 
            print("No button to change to correct sign in ")


        time.sleep(3)

        try:
            inputXPATH = '//*[@id="username"]'
            emailInput = self.driver.find_element(By.XPATH, inputXPATH)
            emailInput.click()
            emailInput.send_keys(email)

            time.sleep(1)
            passwordXPATH = '//*[@id="password"]'
            passwordInput = self.driver.find_element(By.XPATH, passwordXPATH)
            passwordInput.click()
            passwordInput.send_keys(password)

            signInButtonTwoXPATH = '//*[@id="organic-div"]/form/div[3]/button'
            signInButtonTwo = self.driver.find_element(By.XPATH, signInButtonTwoXPATH)
            signInButtonTwo.click()
        except Exception as e: 
            print("Error entering email and password")

        

    def findBigPlayers(self, csvFile: str):
            with open(csvFile, mode='r', newline='') as file:
                csvReader = csv.reader(file)
                for row in csvReader:
                    print(row)

                    url = row[0]
                    if url[0] != 'h':
                        continue


                    self.signIn(email="aeplotkin@gmail.com", password="MonkeyMilo1")

                    time.sleep(2)

                    self.driver.get(url=url)

                    time.sleep(3)

                    companyXPATH = '//*[@id="profile-content"]/div/div[2]/div/div/main/section[1]/div[2]/div[2]/ul/li[1]/button'
                    company_button = self.driver.find_element(By.XPATH, companyXPATH)
                    company_button.click()

