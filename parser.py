
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS145 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

users_file = "Users.dat_raw"
categories_file = "Categories.dat_raw"
items_file = "Items.dat_raw"
bid_file = "Bid.dat_raw"
item_seller_file = "Item_Seller.dat_raw"
item_category_file = "Item_Category.dat_raw"

f = open('Items.dat_raw', 'w')
f.close()
f = open('Users.dat_raw', 'w')
f.close()
f = open('Categories.dat_raw', 'w')
f.close()
f = open('Item_Seller.dat_raw', 'w')
f.close()
f = open('Item_Category.dat_raw', 'w')
f.close()
f = open('Bid.dat_raw', 'w')
f.close()

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

def processString(str):
    res = str.replace('"', '""')
    return '"' + res + '"'

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    """
    open file
    """
    global users_file
    global categories_file
    global items_file
    global item_category_file
    global item_seller_file
    global bid_file

    users_file_h = open(users_file, 'a')
    categories_file_h = open(categories_file, 'a')
    items_file_h = open(items_file, 'a')
    item_category_file_h = open(item_category_file, 'a')
    item_seller_file_h = open(item_seller_file, 'a')
    bid_file_h = open(bid_file, 'a')


    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            item_id = str(item['ItemID'])
            # print item_id

            name = str(item['Name'])
            name = processString(name)
            # print Name

            started = transformDttm(str(item['Started']))
            # print started
            # print type(started)

            ends = transformDttm(str(item['Ends']))
            # print ends

            currently = transformDollar(str(item['Currently']))
            # print currently

            first_bid = transformDollar(str(item['First_Bid']))

            buy_price = ""
            if 'Buy_Price' in item:
                buy_price = transformDollar(str(item['Buy_Price']))
            else:
                buy_price = -1

            number_of_bids =  str(item['Number_of_Bids'])
            # print number_of_bids
            description = str(item['Description'])
            # print type(description)
            description = processString(description)

            items_entry = (item_id, name, started, ends, currently, first_bid, buy_price, number_of_bids, description)
            items_entry = columnSeparator.join(items_entry) + '\n'
            items_file_h.write(items_entry)

            for cate in item['Category']:
                categories_file_h.write(cate + '\n')
                item_category_entry = (item_id, cate)
                item_category_entry = columnSeparator.join(item_category_entry) + '\n'
                item_category_file_h.write(item_category_entry)

            seller_id = processString(str(item['Seller']['UserID']))
            seller_rating = str(item['Seller']['Rating'])
            seller_location = processString(str(item['Location']))
            seller_country = processString(str(item['Country']))

            seller_entry = (seller_id, seller_rating, seller_location, seller_country)
            seller_entry = columnSeparator.join(seller_entry) + '\n'
            users_file_h.write(seller_entry)

            item_seller_entry = (item_id, seller_id)
            item_seller_entry = columnSeparator.join(item_seller_entry) + '\n'
            item_seller_file_h.write(item_seller_entry)

            bids = item['Bids']
            #print type(bids)
            if bids is None:
                continue

            for bid in bids:
                bid_time = transformDttm(str(bid['Bid']['Time']))
                bid_amount = transformDollar(str(bid['Bid']['Amount']))
                bidder_id = processString(str(bid['Bid']['Bidder']['UserID']))
                bidder_rating = str(bid['Bid']['Bidder']['Rating'])
                bidder_location = ""
                bidder_country = ""

                bidder = bid['Bid']['Bidder']
                if 'Location' in bidder:
                    bidder_location = processString(str(bidder['Location']))
                else:
                    bidder_location = 'NULL'

                if 'Country' in bidder:
                    bidder_country = processString(str(bidder['Country']))
                    #print bidder_country
                else:
                    bidder_country = 'NULL'
                    #print bidder_country

                bidder_entry = (bidder_id, bidder_rating, bidder_location, bidder_country)
                bidder_entry = columnSeparator.join(bidder_entry) + '\n'
                users_file_h.write(bidder_entry)

                bid_entry = (bidder_id, item_id, bid_time, bid_amount)
                bid_entry = columnSeparator.join(bid_entry) + '\n'
                bid_file_h.write(bid_entry)

    users_file_h.close()
    categories_file_h.close()
    items_file_h.close()
    item_category_file_h.close()
    item_seller_file_h.close()
    bid_file_h.close()










"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print "Success parsing " + f

if __name__ == '__main__':
    main(sys.argv)
