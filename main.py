import requests
from bs4 import BeautifulSoup


class Crawler:

    def __init__(self,url):
        self.website_url = url
        self.firmware_downloads_url = ''
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
        self.firmware_downloads_url = self.website_url + the_link
        return self.firmware_downloads_url

    def get_next_page_link(self, url):
        soup = self.get_page_content(url)
        try:
            next_page_link = soup.find('li', class_='pages-next last').find('a')['href']
        except TypeError:
            return False   # if there is no link I catch the error and return False
        return next_page_link
    
    def get_pages(self):
        self.pages.append(self.get_firmware_downloads_link()) 
        temp_url = self.firmware_downloads_url
        while temp_url:
            if 'rockchiofirmware' in temp_url: # if this is a self.firmware_downloads_url
                temp_url = self.get_next_page_link(temp_url)
                self.pages.append(self.website_url + temp_url)
            else:
                temp_url = self.get_next_page_link(self.website_url + temp_url)
                if temp_url != False:
                    self.pages.append(self.website_url + temp_url)
        return self.pages


    def get_and_save_firmware_links_from_the_page(self, url):
        soup = self.get_page_content(url)
        table = self.get_elements_from_content(soup, 'td', 'views-field views-field-title')
        for firmware_link in table:
            self.firmware_files_links.append(self.website_url + firmware_link.find('a')['href'].replace('\\', '/'))
            # the line above is long, but you can see there are very simple actions:
            # I just concatenate the website url with the link for specific firmware file
            # and replace '\\' to '/' because it's url I want to visit after
        return

    def get_firmware_links(self):
        for page in self.pages:
            self.get_and_save_firmware_links_from_the_page(page)
        return 

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

