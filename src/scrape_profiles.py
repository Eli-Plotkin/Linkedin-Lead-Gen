import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from bs4 import BeautifulSoup

class scrapeProfiles():
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

            signInOne = self.driver.find_element(By.LINK_TEXT, "Sign in")

            if signInOne:
                signInOne.click()

        except Exception as e: 
            print("Couldn't find sign in button")
            return

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


    def get_likers_from_post(self, post_link: str):
        all_likers = list()

        self.driver.get(post_link)

        time.sleep(1)

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        post_date_section = soup.find('a', class_ = "app-aware-link update-components-actor__sub-description-link")
        post_date = post_date_section['aria-label']

        likers_section = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((
            By.CLASS_NAME, "social-details-social-counts__count-value")))
        
        if not likers_section:
            return all_likers
                
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
                full_name = name_element.text

                name_parts = full_name.split()
                if len(name_parts) >= 2:
                    first_name = name_parts[0]
                    last_name = ' '.join(name_parts[1:])

                all_likers.append((profile_link, first_name, last_name, full_name, post_date))
            except Exception as e:
                print(f"Error processing liker: {e}")


        return all_likers
    



    def get_commenters_from_post(self, post_link: str):
        all_commenters = list()

        self.driver.get(post_link)

        time.sleep(3)

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        post_date_section = soup.find('a', class_ = "app-aware-link update-components-actor__sub-description-link")
        post_date = post_date_section['aria-label']

        # Scroll incrementally until the commenters section is found or we reach the bottom
        last_height = self.driver.execute_script("return document.body.scrollHeight;")
        scroll_to_class = "update-v2-social-activity"
        commenters_section_css = ".feed-shared-update-v2__comments-container"
        commenters_section = None

        while True:
            # Scroll down a bit
            self.driver.execute_script("window.scrollBy(0, 400);")
            time.sleep(2)  # Give it time to load

            try:
                scroll_to = self.driver.find_element(By.CLASS_NAME, scroll_to_class)
                break  # Exit the loop if commenters section is found
            except:
                new_height = self.driver.execute_script("return document.body.scrollHeight;")
                if new_height == last_height:
                    return all_commenters  # Return the empty list if we reach the bottom and commenters section is not found
                last_height = new_height

        if not scroll_to:
            return all_commenters  # Return the empty list if commenters section is not found
        
        try:
            commenters_button = self.driver.find_element(By.CSS_SELECTOR, ".social-details-social-counts__item--right-aligned")
            commenters_button.click()
        except:
            return all_commenters
        
        time.sleep(1)

        commenters_section = self.driver.find_element(By.CSS_SELECTOR, commenters_section_css)
        commenters_list = commenters_section.find_element(By.CLASS_NAME, "comments-comment-list__container")

        # Scroll to load all commenters
        last_height = self.driver.execute_script("return arguments[0].scrollHeight", commenters_list)

        while True:
            self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", commenters_list)
            time.sleep(2)  # Give it time to load more commenters
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", commenters_list)
            if new_height == last_height:
                # Add a short delay to ensure final comments load
                time.sleep(3)
                new_height = self.driver.execute_script("return arguments[0].scrollHeight", commenters_list)
                final_height = self.driver.execute_script("return arguments[0].scrollHeight", commenters_list)
                if final_height == new_height:
                    break

            last_height = new_height

        commenters = commenters_list.find_elements(By.CLASS_NAME, "comments-comment-entity")



        for com in commenters:
            try:
                commenter_html = com.get_attribute('outerHTML')
                soup = BeautifulSoup(commenter_html, 'html.parser')
                profile_link = soup.find('a', class_="app-aware-link tap-target overflow-hidden")['href']
                full_name = soup.find('span', class_="comments-comment-meta__description-title").text

                name_parts = full_name.split()
                if len(name_parts) >= 2:
                    first_name = name_parts[0]
                    last_name = ' '.join(name_parts[1:])

                all_commenters.append((profile_link, first_name, last_name, full_name, post_date))

            except Exception as e:
                print(f"Error processing commenter: {e}")

        return all_commenters




    def export_data(self, email: str, password: str, post_link: str):
        self.sign_in(email=email, password=password)

        # Gather all data to export
        likers_data = self.get_likers_from_post(post_link=post_link)
        commenters_data = self.get_commenters_from_post(post_link=post_link)

        with open('scraped_profiles.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Profile Link', 'First Name', 'Last Name', 'Full Name', 'Post Date'])  # Write header

            for liker_data in likers_data:
                writer.writerow([liker_data[0], liker_data[1], liker_data[2], liker_data[3], liker_data[4]])

            for commenter_data in commenters_data:
                writer.writerow([commenter_data[0], commenter_data[1], commenter_data[2], commenter_data[3], commenter_data[4]])

        self.driver.close()
