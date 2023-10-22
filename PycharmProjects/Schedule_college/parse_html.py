import os
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager  # type: ignore
from selenium.webdriver.common.by import By
from icecream import ic  # type: ignore


class Parser:
    def __init__(self):
        ic("Installing driver")
        start_time = time.time()
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))  # type: ignore
        end_time = time.time()
        execution_time = round(end_time - start_time, 2)
        ic(execution_time, "sec")

    def prepare_download_link(self, link_orig):
        string_new = link_orig.replace("/file/d/", "/uc?id=").replace("/view?usp=drive_web", "&export=download")
        return string_new

    def download_tables(self, links):
        folder_name = 'Tables'
        os.makedirs(folder_name, exist_ok=True)

        for text, link in links.items():
            start_time = time.time()
            response = requests.get(self.prepare_download_link(link))
            file_name = f'{folder_name}/{text}'
            with open(file_name, 'wb') as file:
                file.write(response.content)
            end_time = time.time()
            execution_time = round(end_time - start_time, 2)
            ic(f"Файл {file_name} скачан за {execution_time} sec")

    def parse_html(self, url="https://mck-ktits.ru/portfolio-overviews/расписание/"):
        ic("Parse html")
        start_time = time.time()
        self.driver.get(url)
        end_time = time.time()
        execution_time = round(end_time - start_time, 2)
        ic(execution_time, "sec")

    def get_table(self):
        ic("Get table")
        table = self.driver.find_element(By.CLASS_NAME, "FileListFromGoogle")
        return table

    def parse_table(self, table):
        ic("Table parse")
        cells = table.find_elements(By.TAG_NAME, "a")

        links = {}
        for cell in cells:
            link = cell.get_attribute('href')
            text = cell.text
            if link not in links and text != "View":
                links[text] = link
        self.driver.quit()
        return links

if __name__ == "__main__":
    first_links = Parser()
    first_links.parse_html()
    table = first_links.get_table()
    links = first_links.parse_table(table)
    first_links.download_tables(links)