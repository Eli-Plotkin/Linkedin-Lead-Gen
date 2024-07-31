import csv
import openpyxl
from openpyxl.styles import Border, Side
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

        

    def get_companies_and_positions(self, csvFile: str) -> dict:
        with open(csvFile, mode='r', newline='') as file:
            csvReader = csv.reader(file)

            self.sign_in(email="aeplotkin@gmail.com", password="MonkeyMilo1")
            company_and_position = dict()

            for i, row in enumerate(csvReader):

                if i > 2:
                    break

                url = row[0]
                if url[0] != 'h':
                    continue

                time.sleep(2)

                self.driver.get(url=url)

                time.sleep(1)
                
                curr_url = self.driver.current_url
                target = curr_url + "/details/experience/"
                self.driver.get(target)
                print(target)

                time.sleep(4)
                
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                main_page = soup.find('main', class_= "scaffold-layout__main")
                experiences = main_page.find('div', class_="pvs-list__container")
                current_experience = experiences.find('li', class_="pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column")

                current_company_section = current_experience.find('div', class_= "display-flex align-items-center mr1 hoverable-link-text t-bold")
                
                if current_company_section is None:
                    current_company_section = current_experience.find('span', class_="t-14 t-normal")
                    current_position_section = current_experience.find('div', class_="display-flex flex-wrap align-items-center full-height")
                else:
                    positions_list = current_experience.find('ul', attrs={'tabindex': '-1'})
                    current_position_section = positions_list.find('div', class_="display-flex align-items-center mr1 hoverable-link-text t-bold")


                company = current_company_section.find('span', class_="visually-hidden").text
                position = current_position_section.find('span', class_="visually-hidden").text
                
                
                this_company_and_position = (company, position)
                company_and_position[row[3]] = this_company_and_position
                print(row[3] + ": " + company_and_position[row[3]][0] + ", " + company_and_position[row[3]][1])

            file.close()
            return company_and_position
    
    def export_data(self, data: dict):
       # Create a new workbook and select the active worksheet
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # Optionally, write a header row
        sheet.append(['Name', 'Company', 'Position'])


        # Write the key-value pairs
        for key, (value_part1, value_part2) in data.items():
            sheet.append([key, value_part1, value_part2])


        #Style Sheet
        border_style = Border(bottom=Side(border_style='thin'))

        for col in range(1, 4):  # Columns A, B, C (1-based index)
            cell = sheet.cell(row=1, column=col)
            cell.border = border_style

        columns_to_resize = ['A', 'B', 'C']
        column_width = 20
        

        for col_letter in columns_to_resize:
            sheet.column_dimensions[col_letter].width = column_width

        # Save the workbook to a file
        workbook.save('output.xlsx')
