from bs4 import BeautifulSoup
import requests
import re
import json


class Scraper:
    def __init__(self, start_site, crawler):
        self.site_arr = [start_site]
        self.visited_num = 0
        self.visited_links = []
        self.content_html = []
        self.file_name = "scrapedInfo.json"
        self.crawler = crawler
        self.run_bool = True

        self.stick_url = "domain name"
        self.stick_url_bool = True
        # stick_url : a domain for the scraper to stick with
        # stick_url_bool : whether to stick with a domain

        self.find_specify = [
            ["tag","tag id or class"], ["tag", "tag id or class"]]
        # find_specify put in the wanted html items, [html tag, tag id or class name ]

        self.find_specify_bool = [False, False]
        # whether to specify to get children inside of the first pick

        self.find_specific_child = ["children tag","children tag"]
        # get a specific child of the html items

        self.searchby = ["class or id", "class or id"]
        # search by class or id of the html tag

        self.json_input = ["", ""]
        # how the JSON file will be organized and information will be inputted

        self.json_place_name = "data"
        # the array in the JSON file that you are putting scraped information information into

    def run(self):
        result = requests.get(self.site_arr[0])
        soup = BeautifulSoup(result.content, "html.parser")
        self.visited_links.append(self.site_arr.pop(0))
        self.grab_links(soup)
        self.grab_content(soup)
        if self.run_bool:
            self.store_data()
        else:
            self.run_bool = True

    def get_info(self, site):
        return requests.get(site)

    def grab_links(self, soup):
        for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
            if self.stick_url in str(link) or stick_url_bool == False:
                self.crawler.site_append(link.get('href'))

    def grab_content(self, soup):
        for i in range(len(self.find_specify)):
            if self.searchby[i] == "class":
                found_soup = soup.find(
                    self.find_specify[i][0],  class_=self.find_specify[i][1])
            elif self.searchby[i] == "id":
                found_soup = soup.find(
                    self.find_specify[i][0],  id=self.find_specify[i][1])

            if found_soup != None and self.find_specify_bool:
                self.content_html.append(str(found_soup.find_all(
                    self.find_specific_child_1).text))
            elif found_soup != None:
                self.content_html.append(str(found_soup.text))

        self.crawler.remove_links()
        self.run_bool = False

    def store_data(self):
        # Put recipes into a JSON file
        # add another json input when you make more json inputs, self.content_html will also need to be given another item
        with open(self.file_name) as json_file:
            data = json.load(json_file)
            temp = data[self.json_place_name]
            update_file = {json_input[0]: self.content_html[0],
                           json_input[1]: self.content_html[1]

                           }
            temp.append(update_file)
            write_json(data, self.file_name)


def write_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


class Crawler:
    def __init__(self, inital_site):
        self.sites_to_visit = [inital_site]
        self.sites_visited = []

    def site_append(self, link):
        if not link in self.sites_to_visit and not link in self.sites_visited:
            self.sites_to_visit.append(link)

    def site_read(self):
        print(self.sites_to_visit, "sites_to_visit")
        self.sites_visited.append(self.sites_to_visit[0])
        return self.sites_to_visit.pop(0)

    def remove_links(self):
        for i in range(2):
            if len(self.sites_visited) > 1:
                self.sites_visited.pop(0)


def main():
    inital_site = "site to begin from"

    crawler = Crawler(inital_site)

    counter = 0
    # how many times to run the crawler
    while counter < 10:
        counter += 1
        scraper = Scraper(crawler.site_read(), crawler)

        scraper.run()


main()
