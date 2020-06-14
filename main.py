import requests
from bs4 import BeautifulSoup


class Crawler:

    def __init__(self,url):
        self.website_url = url
        self.firmware_downloads = ''
        self.pages = []
        self.firmware_files_links = []

    def get_page_content(self, url):
        page = requests.get(url)
        return BeautifulSoup(page.content, 'html.parser')
    
    def get_element_from_content(self, content, element, class_or_id=None):
        if class_or_id is None:
            return content.find(element)
        return content.find(element, class_or_id)
    
    def get_elements_from_content(self, content, element, class_or_id=None):
        if class_or_id is None:
            return content.find_all(element)
        return content.find_all(element, class_=class_or_id)
    
    def get_firmware_downloads_link(self):
        soup = self.get_page_content(self.website_url)
        the_link = self.get_element_from_content(soup, 'tr').find('a')['href']
        self.firmware_downloads = self.website_url + the_link
        return self.firmware_downloads


    def get_next_page_link(self, url):
        pass
    
    def get_pages(self):
        pass
    
    def get_firmware_links_from_the_page(self, url):
        pass
    
    def get_firmware_links(self):
        pass

    def get_date_of_submit(self, year, month):
        pass

    def get_metadata_from_link(self, url):
        pass

    def add_to_db(self):
        pass
    
    def get_metadata_and_add_to_db(self):
        pass
    
    def check_changes(self, url):
        pass

    def check_metadata_for_all_firmware_links(self):
        pass

    def print_summary(self):
        pass

    def start_web_crawler(self):
        pass

