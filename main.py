import requests
from bs4 import BeautifulSoup
from datetime import date
from database import Database
import sys
import time
from bson.objectid import ObjectId




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
            next_page_link = soup.find('li', class_='pager-next last').find('a')['href']
        except TypeError:
            return False   # if there is no link I catch the error and return False
        return next_page_link
    
    def get_pages(self):
        temp_url = self.get_firmware_downloads_link()
        self.pages.append(temp_url) 
        while temp_url:
            if 'rockchipfirmware' in temp_url: # if this is a self.firmware_downloads_url
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

    def get_date_of_submit(self, year, months):
        today = date.today()
        if int(months) >= today.month:
            return  str(today.year - int(year) - 1) + '-' + str(today.month + 12 - int(months)) 
        return str(today.year - int(year)) + '-' + str(today.month - int(months))

    def get_metadata_from_link(self, url):
        soup = self.get_page_content(url)
        device_name = soup.find('div', class_='field-name-title').text
        last_modified = None
        if self.get_element_from_content(soup, 'div', ' field-name-changed-date') is not None:
            last_modified = soup.find('div', class_='field field-name-changed-date').find('div', class_='field-item even').text
        submittion = self.get_element_from_content(soup, 'div', 'field-name-submitted-by').text
        submitted_day = submittion.split(' ')[1:4:2]
        submitted_day = self.get_date_of_submit(submitted_day[0], submitted_day[1])
        submitted_by = submittion.split(' ')[-1][:-1]
        brand = self.get_element_from_content(soup, 'div', 'field-name-field-brand').find( 'div', class_='field-item even').text
        model = self.get_element_from_content(soup, 'div', 'field-name-field-model').find( 'div', class_='field-item even').text
        return [url, device_name, last_modified, submitted_day, submitted_by, brand, model]

    def add_to_db(self, url, device_name, last_modified, submitted_day, submitted_by, brand, model):
        Database.insert('metadata', {
            'url': url,
            'device_name': device_name,
            'last_modified': last_modified,
            'submitted_day': submitted_day,
            'submitted_by': submitted_by,
            'brand': brand,
            'model': model
        })
        return 
    
    def get_metadata_and_add_to_db(self):
        for firmware_link in self.firmware_files_links:
            self.add_to_db(*self.get_metadata_from_link(firmware_link)) # I unpack arguments and call self.add_to_db function
        return

    def check_changes(self, url):
        url, device_name, last_modified, submitted_day, submitted_by, brand, model = self.get_metadata_from_link(url)
        doc_counter = Database.count_documents('metadata', { 'url': url,
            'device_name': device_name,
            'last_modified': last_modified,
            'submitted_day': submitted_day,
            'submitted_by': submitted_by,
            'brand': brand,
            'model': model })
        if doc_counter == 0:
                id = ''
                for itm in Database.find('pages', { 'url': url}):
                    id = itm.get('_id')
                print(id)
                Database.update('pages', ObjectId(id), { '$set' : { 'url': url,
                    'device_name': device_name,
                    'last_modified': last_modified,
                    'submitted_day': submitted_day,
                    'submitted_by': submitted_by,
                    'brand': brand,
                    'model': model }})
                return 1
        return 0

    def check_metadata_for_all_firmware_links(self):
        counter = 0
        self.get_pages()
        self.get_firmware_links()
        for firmware_link in self.firmware_files_links:
            counter += self.check_changes(firmware_link)
        if counter == 0:
            print('There are no changes in firmware files')
        if counter == 1:
            print("1 firmware file was changed")
        elif counter > 1:
            print("There are " + str(counter) + "firmware files been changed")
        return

    def print_summary(self):
        firebase_amount = Database.count_documents('metadata', {})
        PiPO = Database.count_documents('metadata', { 'brand': 'PiPO'})
        Cube  = Database.count_documents('metadata', { 'brand': 'Cube'})
        Yuandao = Database.count_documents('metadata', { 'brand': 'Yuandao'})
        Ployer = Database.count_documents('metadata', { 'brand': 'Ployer'})
        Teclast = Database.count_documents('metadata', { 'brand': 'Teclast'})
        d = { 'Cube': Cube, 'PiPO': PiPO, 'Ployer': Ployer, 'Teclast': Teclast, 'Yuandao': Yuandao}
        print('There are', firebase_amount, 'firmware files in the database')
        print('The most popular brands are:')
        for key, value in d.items():
            print(value, key, 'brands') 
        return 

    def start_web_crawler(self):
        start = time.perf_counter()
        self.get_pages()
        self.get_firmware_links()
        self.get_metadata_and_add_to_db()
        finish = time.perf_counter()
        print("Finished in" , round(finish - start, 2), "seconds")

if __name__ == '__main__':
    if sys.argv[-1] != 'https://www.rockchipfirmware.com/':
        print('Incorect website url. Please try again.')
    else:
        my_crawler = Crawler(sys.argv[-1])
        action = sys.argv[1]
        if action == 'start_web_crawler':
            my_crawler.start_web_crawler()
        elif action == 'check_changes':
            my_crawler.check_metadata_for_all_firmware_links()
        elif action == 'summary':
            my_crawler.print_summary()
        else:
            print('Something went wrong. It happens to the best of us.')