import requests
from bs4 import BeautifulSoup
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

#Creates a class with methods which can extract web data using a generalized 
#format found in darktide_gameslantern_requests_text.json

class ScrapeGamesLantern:
    def __init__(self, request_json):
        self.gameslantern_request = request_json    

        url = self.gameslantern_request["url"]
        response = requests.get(url)
        html_source_code = response.text

        #If selenium argument is true the the page data is dynamically loaded and we need the browser to run the JS functions.
        options = Options()
        options.headless = True
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        driver = webdriver.Chrome(options=options) 
        if self.gameslantern_request["selenium"]:
            driver.get(url)
            time.sleep(5) 
            html_source_code = driver.page_source

        #Get soup or return
        self.soup = BeautifulSoup(html_source_code, 'html.parser')
        # Check if url source code grab was successful. If not then print and return.
        if self.soup is None:
            print("Could not soup parse html")
            return 

#Function to get request instructions from json file and prepare them based on different search methods 
    def get_html_data_from_request_json(self):
        data_dict = {}
        html_text_example = self.gameslantern_request["html_text"]
        for html in html_text_example:
            html_text = html["search"]
            html_header = html["header"]
            html_method = html["method"]

            html_list = self.find_in_html(self.soup, html_text, method = html_method)
            if "subsearch" in list(html.keys()):
                subsearch = html["subsearch"]
                subsearch_method = html["subsearch_method"]
                data_dict[html_header] = [[b.text for b in self.find_in_html(a, subsearch, method = subsearch_method)] for a in html_list]
            
            else: 
                data_dict[html_header] = [txt.text for txt in html_list]

            
            #Also, get keep some meta data for each line. 
            #data_dict[html_header + " HTML Search text"]=[html_text]*len(html_list)
            #data_dict[html_header + " HTML Search Method"]=[html_method]*len(html_list)

        return data_dict

    def find_in_html(self, html, search_text, method = ""):
        if method == "by_class_text":
            html_search = html.find(text=search_text)
            html_class = ' '.join(html_search.parent["class"])
            html_list = html.find_all(class_=html_class)
            return html_list

        if method == "by_class":
            html_list = html.find_all(class_=search_text)
            return html_list

        elif method == "by_sibling_text":
            html_search = html.find(text=search_text)
            html_list = [sib for sib in html_search.parent.find_previous_siblings()] + [html_search.parent] + [sib for sib in html_search.parent.find_next_siblings()]
            return html_list

        elif method == "by_element":
            html_list = html.find_all(search_text)
            return html_list

        else: 
            print("Must specify valid method")


