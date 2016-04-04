import argparse
from urllib2 import Request, urlopen, URLError
from lxml.cssselect import CSSSelector
from lxml.html import fromstring, tostring
import sys
import csv

page_root = "" #enter page root here e.g. http://www.google.com - this is required in case of partial URLs for items
partial_product_link_url = False
root_url = "" #this is the URL which contains the listing of items/products
product_link_selector = "" #HTML element containing link e.g. href property of <a>
product_title_selector = "" #HTML element containing title
product_image_selector = "" #HTML element containing image usually <img> tag
product_price_selector = "" #HTML element containing price
product_availability_selector = "" #HTML element containing availability

product_header = ["title", "image", "price", "availability"] #this is the CSV file header - modify as required

class CSVWriter(object):

    wr = None

    def __init__(self, file_name, header):
        mycsvfile = open(file_name, 'wb')
        self.wr = csv.writer(mycsvfile, quoting=csv.QUOTE_ALL)
        self.wr.writerow(header)

    def write(self, write_list):
        self.wr.writerow(write_list)

class Crawler(object):

    file_name = "out.csv"
    output_type = "csv"

    def __init__(self):
        #print "entered init"
        parser = argparse.ArgumentParser()
        parser.add_argument("-o",
                            "--output",
                            help="output type",
                            type=str,
                            required=True)
        parser.add_argument("-f",
                            "--filename",
                            help="file name",
                            type=str)
        self.args = parser.parse_args()
        output_type = self.args.output

        if self.args.filename:
            self.file_name = self.args.filename

    def read_url(self, url):
        req = Request(url, headers={'User-Agent' : "Magic Browser"})
        try:
            response = urlopen(req)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
        else:
            return response.read()

    def run(self, root_url):

        print "reading: " + root_url
        page = c.read_url(root_url)

        selProductURL = CSSSelector(product_link_selector)
        r = selProductURL(fromstring(page))

        prod_links = []
        if len(r) > 0:
            for i in range(len(r)):
                href = r[i].get("href").strip()
                #print href
                prod_links.append(href)
        else:
            print "No product links found"
        #sys.exit()

        if self.output_type == "csv":
            writer = CSVWriter(self.file_name, product_header)

        for i in range(len(prod_links)):
            print "Fetching: " + str(i+1) + "/" + str(len(prod_links))

            if partial_product_link_url == True:
                u = page_root + prod_links[i]
            else:
                u = prod_links[i]
            page = self.read_url(u)
            page_str = fromstring(page)

            product_info = []

            selProductTitle = CSSSelector(product_title_selector)
            p = selProductTitle(page_str)
            if len(p) > 0:
                product_title = p[0].text_content()
                product_info.append(product_title)
                print product_title

            selProductImage = CSSSelector(product_image_selector)
            p = selProductImage(page_str)
            if len(p) > 0:
                product_image = p[0].get("data-old-hires")
                print product_image
                product_info.append(product_image)

            selProductPrice = CSSSelector(product_price_selector)
            p = selProductPrice(page_str)
            if len(p) > 0:
                product_price = p[0].text_content()
                print product_price
                product_info.append(product_price)

            selProductAvailability = CSSSelector(product_availability_selector)
            p = selProductAvailability(page_str)
            if len(p) > 0:
                product_availability = p[0].text_content().strip()
                print product_availability
                product_info.append(product_availability)

            writer.write(product_info)

c = Crawler()
c.run(root_url)
