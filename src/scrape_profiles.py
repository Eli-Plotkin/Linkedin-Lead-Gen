import csv
import openpyxl
from openpyxl.styles import Border, Side
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from bs4 import BeautifulSoup
import re

class scrape_profiles():
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
            signInOneXPATH1 = '//a[@class="nav__button-secondary btn-md btn-secondary-emphasis"]'
            signInOneXPATH2 = '//a[@class="nav__button-secondary btn-sm btn-primary"]'

            path1 = True

            signInOneV1 = self.driver.find_element(By.XPATH, signInOneXPATH1)

            if signInOneV1 is not None:
                signInOneV1.click()

            else:
                signInOneV2 = self.driver.find_element(By.XPATH, signInOneXPATH2)
                signInOneV2.click()
                path1 = False

        except Exception as e: 
            print("Couldn't find first sign in button")
            return

        time.sleep(1)

        if not path1:
            goToCredentialsXPATH = '//a[@class="main__sign-in-link"]'
            goToCredentials = self.driver.find_element(By.XPATH, goToCredentialsXPATH)
            goToCredentials.click()

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


    def get_likers_from_post(self, post_link: str):
        all_likers = list()

        self.driver.get(post_link)

        likers_section = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((
            By.CLASS_NAME, "social-details-social-counts__reactions-count")))
                
        likers_section.click()

        time.sleep(2)

        likers_list = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "artdeco-modal__content")))

        # Scroll to load all likers
        last_height = self.driver.execute_script("return arguments[0].scrollHeight", likers_list)
    
        while True:
            self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", likers_list)
            time.sleep(2)  # Give it time to load more likers
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", likers_list)
            if new_height == last_height:
                break
            last_height = new_height

        likers = likers_list.find_elements(By.CLASS_NAME, "artdeco-list__item")


        if not likers :
            print("Could not find Likers")
            return

        for liker in likers:
            try:
                liker_html = liker.get_attribute('outerHTML')
                soup = BeautifulSoup(liker_html, 'html.parser')
                profile_link_element = soup.find('a', attrs={"rel": "noopener noreferrer"})
                profile_link = profile_link_element['href']
                name_element = soup.find('span', attrs={"dir": "ltr", "class": "text-view-model"})
                name = name_element.text

                name_parts = name.split()
                if len(name_parts) >= 2:
                    first_name = name_parts[0]
                    last_name = ' '.join(name_parts[1:])

                all_likers.append((profile_link, first_name, last_name, name))
            except Exception as e:
                print(f"Error processing liker: {e}")


        return all_likers
    


    def export_data(self, post_link: str):
        # Gather all data to export
        data = self.get_likers_from_post(post_link=post_link)

        with open('scraped_profiles.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Profile Link', 'First Name', 'Last Name', 'Full Name'])  # Write header
            for person_data in data:
                writer.writerow([person_data[0], person_data[1], person_data[2], person_data[3]])

        self.driver.close()

    #    # Create a new workbook and select the active worksheet
    #     workbook = openpyxl.Workbook()
    #     sheet = workbook.active

    #     # Optionally, write a header row
    #     sheet.append(['Profile Link', 'Name'])


    #     # Write the key-value pairs
    #     for person_data in data:
    #         sheet.append([person_data[0], person_data[1], person_data[2]])


    #     #Style Sheet
    #     border_style = Border(bottom=Side(border_style='thin'))

    #     for col in range(1, 3):  # Columns A, B(1-based index)
    #         cell = sheet.cell(row=1, column=col)
    #         cell.border = border_style

    #     columns_to_resize = ['A', 'B']
    #     column_width = 28
        

    #     for col_letter in columns_to_resize:
    #         sheet.column_dimensions[col_letter].width = column_width



        # Save the workbook to a file
        # workbook.save('scraped_profiles.xlsx')



        