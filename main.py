import collections
import csv
import os
import re
from datetime import datetime

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from utils import *
collections.Callable = collections.abc.Callable                         # type: ignore

with open('./setup.json') as fin:        # type: ignore
    setup = json.load(fin)


def main():
    # open page
    url = 'https://www.facebook.com/marketplace/'
    years, names, prices, mileages, locs, links = [], [], [], [], [], []
    testfile = "tmp.mhtml"

    testfile = save_page(url, testfile)

    with open(testfile, 'r') as pg:
        content = pg.read().replace("=\n\n", "")                   # read html data
        # create soup object
        soup = BeautifulSoup(content, 'lxml')

        # find class for price
        # type: ignore
        re_price = re.compile("\$[0123456789,]+")
        prices_obj = soup.body.findAll(string=re_price)
        parent_list = []

        for price_obj in prices_obj:
            tmp = price_obj.parent.parent.parent.parent.parent
            if len(list(tmp.children)) == 4:
                parent_list.append(tmp)

        for p in parent_list:
            # get data in children
            pcl = list(p.children)
            # find details
            prices.append(get_price(pcl))
            names.append(pcl[1].get_text()[5:])
            years.append(pcl[1].get_text()[0:4])
            locs.append(pcl[2].get_text())
            mileages.append(get_mileage(pcl))
            links.append(get_link(p))

    # sort data
    us = list(zip(names, years, prices, mileages, locs, links))
    # x[1] refers to the 'years' in the tuple
    us = sorted(us, key=lambda x: x[1])

    years, names, prices, mileages, locs, links = [], [], [], [], [], []
    for u in us:
        names.append(u[0])
        years.append(u[1])
        prices.append(u[2])
        mileages.append(u[3])
        locs.append(u[4])
        links.append(u[5])

    # export data
    fname = str(datetime.now()).replace(
        ":", "-")[2:-5].replace(" ", "--")  # datetime file save name
    with open(f"sc_{fname}.csv", 'w', newline='') as f:

        headers = ["year", "name", "price", "mileage", "location", "link"]
        csw = csv.writer(f)
        # csw2 = csv.writer(fy)
        # csw3 = csv.writer(fz)
        csw.writerow(headers)

        for year, name, price, mileage, loc, link in zip(years, names, prices, mileages, locs, links):
            csw.writerow([year, name, price, mileage, loc, link])

            # if mileage is not available - lazy rn sorry
            if str(mileage) in ["Dealership", "N/A"]:
                pass
            elif int(mileage) < (setup['facebook']['max_mileage']) and int(year) > (setup['facebook']['min_year']) and (setup["facebook"]["make"].lower() in name.lower() and setup["facebook"]["model"].lower() in name.lower()):
                csw.writerow([year, name, price, mileage, loc, link])

                print(year, name, "\b,", price, "\b,",
                        mileage, "\b,", loc, "\b,", link)
    
    # remove the tmp.mhtml file
    os.remove(testfile)

if __name__ == "__main__":
    main()
