# web-scraper - HTML product listing to CSV
Python2 script for scraping product listing data to CSV file

This is a basic script that can be modified to scrape product listing websites. This will work for websites that use HTTP Redirects - inc ase there are Javascript redirects, you will need to use something else like [Selenium](http://www.seleniumhq.org/). 

Right now it only scrapes data from one page, "go to next page and continue scraping" capability is To-do

### Usage

- Specify the output using -o or --output argument  (Right now only "csv", without quotes, is supported)
- Specify the output filename using -f or --filename argument. If not specified "out.csv" will be used

### Dependencies

- lxml:

  pip install lxml
  
- cssselect:

  pip install cssselect

### Note

- Product listing is assumed to be in the href of an `<a>` tag
- Image URL is assumed to be in an <img> tag
- Product title, price and availability are assumed to be present as the content of a `<span>` or similar tag

### Errata

- urllib2 is used to read pages and handle redirects
- lxml's CSSSelector is used to specify HTML element - these are similar to jQuery CSS selectors
- Python's csv module is used to write to CSV file
- The script looks for product details link and searches in that page for title, image, price and availability info - this takes longer than reading the information directly from the product listing page but it allows you to read detailed info
- All CSS selectors, anchor tags etc. can specified in the beginning of the script

### To-do

"go to next page and continue scraping"

