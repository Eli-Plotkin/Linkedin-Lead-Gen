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
        


    def __sign_in(self, email: str, password: str):

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

        

    def __get_data(self, csvFile: str, email: str, password: str, is_test_data: bool) -> dict:
        with open(csvFile, mode='r', newline='') as file:
            csvReader = csv.reader(file)
            rows = list(csvReader)

            self.__sign_in(email=email, password=password)
            organized_data = dict()

            if is_test_data:
                breakpoint = 5
            else:
                breakpoint = len(rows)
            
            for i, row in enumerate(rows):
                if i > breakpoint:
                    break

                url = row[0]
                if url[0] != 'h':
                    continue

                self.driver.get(url=url)

                time.sleep(5)
                
                curr_url = self.driver.current_url
                target = curr_url + "/details/experience/"
                self.driver.get(target)
                print(target)

                time.sleep(3)
                
                try:
                    experiences_element = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "pvs-list__container")))
                except TimeoutError:
                    print(f"Timeout while waiting for experiences container for URL: {url}")
                    continue

                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                experiences = soup.find('div', class_="pvs-list__container")
                if experiences is None:
                    print(f"Could not find experiences container for URL: {url}")
                    continue

                try:
                    current_experience = experiences.find('li', class_="pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column")
                except Exception as e:
                    print(f"Error finding current experience for URL: {url} - {e}")
                    continue

                current_company_section = current_experience.find('div', class_= "display-flex align-items-center mr1 hoverable-link-text t-bold")
                
                if current_company_section is None:
                    current_company_section = current_experience.find('span', class_="t-14 t-normal")
                    current_position_section = current_experience.find('div', class_="display-flex flex-wrap align-items-center full-height")
                else:
                    positions_list = current_experience.find('ul', attrs={'tabindex': '-1'})
                    current_position_section = positions_list.find('div', class_="display-flex align-items-center mr1 hoverable-link-text t-bold")


                company = current_company_section.find('span', class_="visually-hidden").text
                position = current_position_section.find('span', class_="visually-hidden").text

                #Get Company Size
                try:
                    company_link_section = experiences.find('a', class_="optional-action-target-wrapper display-flex")
                except AttributeError:
                    print(f"Error finding company link section for URL: {url}")
                    continue

                company_link = company_link_section['href']
                self.driver.get(company_link)

                time.sleep(3)

                company_data = self.__find_company_data()
                
                organized_data[row[3]] = (company, company_data[0], company_data[1],  company_data[2], position, url)

        #Comparator for company sizes
        def company_size_comparator(val):
            size_order = {
                "2-10 employees": 0,
                "11-50 employees": 1,
                "51-200 employees": 2,
                "201-500 employees": 3,
                "501-1K employees": 4,
                "1K-5K employees": 5,
                "5K-10K employees": 6,
                "10K+ employees": 7
            }
            return size_order.get(val, -1)
        
        sorted_list = sorted(organized_data.items(), key=lambda item: company_size_comparator(item[1][3]), reverse=True) 
        sorted_dict = {k: v for k, v in sorted_list}

  
        return sorted_dict
        

    # REQUIRES: Driver is currently on company page
    def __find_company_data(self) -> tuple:
        check_page_loaded = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "org-top-card-summary-info-list")))
        
        if not check_page_loaded:
            print("Page did not load")
            return

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        data_section = soup.find('div', class_ = "org-top-card-summary-info-list" )

        if data_section is None:
            print("data_section not found")
            return

        data = data_section.find_all('div', class_ = "org-top-card-summary-info-list__info-item")
        industry = data[0].text.strip()
        location = data[1].text.strip()
        size = data_section.find('a', class_ = "ember-view org-top-card-summary-info-list__info-item").text.strip()

        relevant_data = tuple((industry, location, size))

        return relevant_data
        


    def export_organized_data(self, csvFile: str, email: str, password: str, is_test_data: bool = False):
        # Gather all data to export
        data = self.__get_data(csvFile=csvFile, email=email, password=password, is_test_data=is_test_data)

       # Create a new workbook and select the active worksheet
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # Optionally, write a header row
        sheet.append(['Name', 'Company', 'Company Industry', 'Company Location', 'Company Size', 'Position,', 'LinkedIn Profile URL'])


        # Write the key-value pairs
        for key, (value_part1, value_part2, value_part3, value_part_4, value_part_5, value_part_6) in data.items():
            sheet.append([key, value_part1, value_part2, value_part3, value_part_4, value_part_5, value_part_6])


        #Style Sheet
        border_style = Border(bottom=Side(border_style='thin'))

        for col in range(1, 8):  # Columns A, B, C, D, E, F, G (1-based index)
            cell = sheet.cell(row=1, column=col)
            cell.border = border_style

        columns_to_resize = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        column_width = 25
        

        for col_letter in columns_to_resize:
            sheet.column_dimensions[col_letter].width = column_width

        # Save the workbook to a file
        workbook.save('output.xlsx')
