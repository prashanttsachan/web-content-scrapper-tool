import sys
from NewspaperScraper import *

def run_scraper (scraper):
    scraper.get_pages()
    data = scraper.newspaper_parser()
    scraper.write_to_csv(data, 'none.csv')

def initialize_scraper (args):
    if args[1] == 'Chicago Tribune':
        run_scraper(ChicagoTribuneScraper(args[1], args[2], args[3], args[4]))

if __name__ == "__main__":
    initialize_scraper(sys.argv)