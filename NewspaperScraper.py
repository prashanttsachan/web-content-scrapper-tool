import os
import requests
import time
import csv
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime, timedelta
from pytz import timezone
from newspaper import Article

class NewspaperScraper:
    def __init__ (self, newspaper, searchTerm, dateStart, dateEnd):
        self.newspaper = newspaper
        self.searchTerm = searchTerm
        self.dateStart = parse(dateStart)
        self.dateEnd = parse(dateEnd)
        self.links = []

    def get_newspaper_name (self):
        return self.newspaper

    def get_pages (self):
        print ('Unimplemented for ' + self.newspaper + ' scraper')
        return

    def check_dates (self, date):
        page_date = parse(date)
        if page_date >= self.dateStart and page_date <= self.dateEnd:
            return True
        return False

    def newspaper_parser (self, sleep_time=0):
        print ('\nrunning newspaper_parser()...')
        results = []
        count = 0
        for l in self.links:
        	try:
        		r = requests.get(l)
        	except requests.exceptions.ConnectionError:
        		print("Connection Error")
        		time.sleep(sleep_time)
        		continue
        	if r.status_code != 200:
        		print("Invalid Response")
        		time.sleep(sleep_time)
        		continue
        	soup = BeautifulSoup(r.text, "html.parser")
        	title = soup.find('h1')
        	author = soup.find('a', {'rel':'author'})
        	if not title or not author:
        		continue
        	data = [title.text, author.get('aria-label'), l]
        	results.append(data)
        	count += 1
        	time.sleep(sleep_time)
        return results


    def write_to_csv (self, data, file_name):
    	print ('writing to CSV...')
    	with open(self.newspaper + ".csv",'w', newline='') as f_output:
    		csv_output = csv.writer(f_output)
    		csv_output.writerows(data)
        # keys = data[0].keys()
        # with open(file_name, 'wb') as output_file:
        #     dict_writer = csv.DictWriter(output_file, keys)
        #     dict_writer.writeheader()
        #     dict_writer.writerows(data)

class ChicagoTribuneScraper(NewspaperScraper):
    def get_pages (self, sleep_time=3):
        print ('Fetching links ...')

        links = []
        stop = False
        index = 1

        while not stop:
            link = 'http://www.chicagotribune.com/search/dispatcher.front?page=' + str(index)+ '&sortby=display_time%20descending&target=stories&spell=on&Query=' + self.searchTerm + '#trb_search'
            try:
                r = requests.get(link)
            except requests.exceptions.ConnectionError:
                print("Connection Error")
                time.sleep(sleep_time)
                continue
            if r.status_code != 200:
                print("Invalid Response")
                time.sleep(sleep_time)
                continue

            soup = BeautifulSoup(r.text, "html.parser")

            if not soup.find('div', class_='trb_search_results'):
                stop = True

            for result in soup.find_all('div', class_="trb_search_result_wrapper"):
                pub_date = result.find('time', class_='trb_search_result_datetime').get('data-dt')
                if ':' in pub_date:
                    pub_date = str(datetime.now(timezone('America/Chicago')).date())

                if self.check_dates(pub_date):
                    link = result.find('a', class_='trb_search_result_title')
                    ltext = 'http://www.chicagotribune.com' + link.get('href')

                    if ltext not in links:
                        print (ltext)
                        links.append(ltext)

                else:
                    stop = True
                    break

            index += 1
            time.sleep(sleep_time)

        self.links = links
        return links