import sys
import os
import requests
import shutil
from bs4 import BeautifulSoup
from datetime import datetime

now = datetime.now()
time = now.strftime("%Y-%m-%dT%H:%M:%S+00:00")
# 2019-10-14T05:14:40+00:00

base_dir = os.getcwd()
site_name = input("Enter website url as 'https://www.example.com':\n")
file_name = input("Enter filename as 'sitemap.xml':\n")
if file_name == '':
    file_name = "sitemap.xml"

visited_links = []
error_links = []

def crawl(link):
    if "http://" not in link and "https://" not in link:
        link = site_name + link
    if site_name in link and link not in visited_links and '#' not in link and '.png' not in link and '.jpg' not in link and '(' not in link:
        print("Working with : {}".format(link))
        path_s = link.split("/")
        file_name = ""
        for i in range(3, len(path_s)):
            file_name = file_name + "/" + path_s[i]
        if file_name[len(file_name) - 1] != "/":
            file_name = file_name + "/"
        try:
            r = requests.get(link)
        except requests.exceptions.ConnectionError:
            print("Connection Error")
            sys.exit(1)
        if r.status_code != 200:
            error_links.append(link)
            print("Invalid Response")
            sys.exit(1)
        visited_links.append(link)

        soup = BeautifulSoup(r.text, "html.parser")
        for link in soup.find_all('a'):
            try:
                if len(visited_links) <= 50:
                    crawl(link.get("href"))
            except:
                error_links.append(link.get("href"))


crawl(site_name + "/")
print("Site has been crawled successfully.")
with open(file_name, "w") as file: 
    file.write('<?xml version="1.0" encoding="UTF-8"?>\n\t<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for link in visited_links:
        file.write("\n\t\t<url>\n\t\t\t<loc>{0}</loc>\n\t\t\t<lastmod>{1}</lastmod>\n\t\t</url>".format(link, time))
    file.write('\n\t</urlset>')

print("Link with errors: ")
for link in error_links:
    print("---- {}\n".format(link))
