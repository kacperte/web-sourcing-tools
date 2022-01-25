import time
import urllib
import pandas as pd
import os

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .data_processing import CommonWords


class Scraper(CommonWords):
    """Scrap Linedin proile and build most common words raport"""

    def __init__(
        self, username: str, password: str, query: str, n_pages: int, quantity=50
    ) -> None:
        """

        :param username: LinkedIn login
        :param password: LinkedIn password
        :param query: Search string
        :param n_pages: How many pages in google you want to scarp - one page give us 10 profiles
        :param quantity: How many common words you want to list eg. "50" give us top 50 common words
        """
        super().__init__(quantity)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        prefs = {
            "download_restrictions": 3,
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        driver = webdriver.Chrome(
            executable_path=os.environ.get("CHROMEDRIVER_PATH"),
            chrome_options=chrome_options,
        )
        self.driver = driver
        self.username = username
        self.password = password
        self.query = query
        self.n_pages = n_pages

    def login(self) -> None:
        """
        Log into Linkedin accout
        :return: None
        """

        print("## Logging")
        try:
            self.driver.find_elements(By.XPATH, "//*[contains(text(),'Skip']").click()
        except:
            pass

        self.driver.get("https://www.linkedin.com/login")
        self.driver.find_element(By.ID, "username").send_keys(self.username)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        self.driver.find_element(By.ID, "password").send_keys("\n")
        print("## Success!")

    def url_parse(self) -> str:
        """
        Function that bulid google serach link
        :return: List of links
        """

        url = "https://google.com/search?q="
        parse_query = urllib.parse.quote_plus(self.query)
        link = url + parse_query + "&start="

        return link

    def search_list(self) -> list:
        """
        Scrap Linkedin profile links from google
        :return: list
        """

        print(f"## Search query: {self.query}")
        links = []
        for page in range(1, self.n_pages):
            time.sleep(0.25)
            url = self.url_parse()
            self.driver.get(url + str(page))
            try:
                self.driver.find_element(By.XPATH, "//input[@type='submit']").click()
            except:
                pass

            time.sleep(2)
            search = self.driver.find_elements(
                By.XPATH, '//div[@class="yuRUbf"]//a[@href]'
            )
            if len(search) <= 0:
                search = self.driver.find_elements(
                    By.XPATH, '//div[@class="kCrYT"]//a[@href]'
                )
            for h in search:
                href = h.get_attribute("href")
                if "google" not in href:
                    links.append(href)
        return links

    def scroll_down(self) -> None:
        """
        Scroll page to the bottom
        :return: None
        """

        total_height = int(
            self.driver.execute_script("return document.body.scrollHeight")
        )

        for i in range(1, total_height, 5):
            self.driver.execute_script(f"window.scrollTo(0, {i});")
        time.sleep(1)

    def loading_all_elements(self) -> None:
        """
        Load Linkedin profile info
        :return: None
        """

        containers = self.driver.find_elements(
            By.XPATH, "//li-icon[@class='pv-profile-section__toggle-detail-icon']"
        )
        for button in containers:
            try:
                self.driver.execute_script("arguments[0].click()", button)
            except:
                pass
            try:
                button.click()
            except:
                pass

        # Load more skills
        try:
            self.driver.execute_script(
                "arguments[0].click();",
                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//button[@class='pv-profile"
                            "-section__card-action-bar "
                            "pv-skills-section__additional-skills "
                            "artdeco-container-card-action-bar "
                            "artdeco-button "
                            "artdeco-button--tertiary "
                            "artdeco-button--3 "
                            "artdeco-button--fluid "
                            "artdeco-button--muted']",
                        )
                    )
                ),
            )
        except:
            pass
        self.scroll_down()

    def talent_mapping(self) -> None:
        """
        Function to scrap info from profile and save it to .csv file
        :return: None
        """

        self.login()
        links = ['https://www.linkedin.com/in/peter-graczykowski/?originalSubdomain=pl']
        list_of_lists = []
        n_links = len(links)
        print(f"## Profiles to scrap: {n_links}")
        for i, link in enumerate(links):
            print(f"## Proccessing {i + 1}/{n_links}\n## Link: {link}")
            list_of_page = []
            self.driver.get(link)
            time.sleep(1)
            self.scroll_down()
            self.loading_all_elements()

            try:
                # Accomplishments
                accomplishments_list = []
                try:
                    accomplishments = self.driver.find_elements(
                        By.XPATH,
                        "//li["
                        "@class='pv-accomplishments-block__summary-list"
                        "-item']",
                    )
                    for i in accomplishments:
                        accomplishments_list.append(i.text)
                except selenium.common.exceptions.NoSuchElementException:
                    pass

                # Licences and certifications
                licences_and_certifications = ""
                try:
                    licences_and_certifications = self.driver.find_element(
                        By.XPATH,
                        "//li["
                        "@class='pv"
                        "-profile"
                        "-section__sortable"
                        "-item "
                        "pv-certification"
                        "-entity "
                        "ember-view']",
                    ).text

                except selenium.common.exceptions.NoSuchElementException:
                    pass
                except IndexError:
                    pass

                # Name, gender, localization and headline
                name = self.driver.find_element(
                    By.XPATH,
                    "//h1[@class='text-heading-xlarge "
                    "inline t-24 v-align-middle "
                    "break-words']",
                ).text
                name = name.split()
                gender = ""
                if name[0].endswith("a") is True:
                    gender += "F"
                else:
                    gender += "M"

                localization = self.driver.find_element(
                    By.XPATH,
                    "//span[@class='text-body-small inline t-black--light "
                    "break-words']",
                ).text
                headline = self.driver.find_element(
                    By.XPATH, "//div[@class='text-body-medium break-words']"
                ).text
                summary = self.clear_text(
                    self.driver.find_element(
                        By.XPATH,
                        "//section[@class='pv-profile-section "
                        "pv-about-section artdeco-card p5 mt4 "
                        "ember-view']",
                    ).text
                )

                # Education
                schools = self.driver.find_elements(
                    By.XPATH,
                    "//li[@class='pv-profile-section__list-item "
                    "pv-education-entity pv-profile-section__card-item "
                    "ember-view']",
                )
                schools_info = []
                for info in schools:
                    schools_info.append(self.clear_text(info.text))

                # Work experience
                jobs = self.driver.find_elements(
                    By.XPATH,
                    "//li[@class='pv-entity__position-group-pager "
                    "pv-profile-section__list-item ember-view']",
                )
                jobs_info = []
                for info in jobs:
                    jobs_info.append(self.clear_text(info.text))

                # Skills
                skills = self.driver.find_elements(
                    By.XPATH,
                    "//p[@class='pv-skill-category-entity__name tooltip-container']",
                )
                skills_list = []
                for skill in skills:
                    skills_list.append(skill.text)

                # Marge and clear text
                profile_text = (
                    " ".join(str(elem) for elem in jobs_info)
                    + " "
                    + " ".join(str(elem) for elem in schools_info)
                    + " "
                    + " ".join(str(elem) for elem in skills_list)
                    + " "
                    + " ".join(str(elem) for elem in accomplishments_list)
                    + " "
                    + licences_and_certifications
                )

                final_text = self.clear_text(profile_text)

                # Adding values to the list of page than adding to the list of list
                list_of_page.append(name[0])
                list_of_page.append(name[1])
                list_of_page.append(gender)
                list_of_page.append(localization)
                list_of_page.append(final_text)
                list_of_lists.append(list_of_page)

            except:
                print('Lipa')
        # Scraped information from profile to csv
        print(list_of_lists)
        df = pd.DataFrame(
            list_of_lists,
            columns=["firstname", "lastname", "gender", "localization", "profile_text"],
        )

        return self.common_words_to_df(df)

    @staticmethod
    def clear_text(text: str) -> str:
        format_text = (
            text.replace(",", " ")
            .replace("•", " ")
            .replace(":", " ")
            .replace("-", " ")
            .replace("…", " ")
            .replace("(", " ")
            .replace(")", " ")
            .replace("–", " ")
            .replace("/", " ")
            .replace("?", " ")
            .replace("+", " ")
            .replace("☑", " ")
            .replace("[", " ")
            .replace("]", " ")
            .replace("\n", " ")
        )

        return format_text
