class Crawler:

    def __init__(self,url):
        self.url = url
        self.firmware_downloads = ''
        self.pages = []
        self.firmware_files_links = []

    def get_page_content(self, url):
        pass
    
    def get_element_from_content(self, content, element, class_or_id=None):
        pass
    
    def get_elements_from_content(self, content, element, class_or_id=None):
        pass
    
    def get_firmware_download_link(self):
        pass
    
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

    def add_to_db(self)
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

