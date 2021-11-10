import argparse
import json
import requests
from bs4 import BeautifulSoup
from requests.models import CONTENT_CHUNK_SIZE

def parse_itemssold(text):
    '''
    takes as input a string and returns the number of items sold, as specified in the string


    >>> parse_itemssold('38 sold')
    38
    >>> parse_itemssold('14 watchers')
    0
    >>> parse_itemssold('Almost gone')
    0
    
    '''
    numbers = ''
    for char in text:
        if char in '1234567890':
            numbers+= char
    if 'sold'in text:
        return int(numbers)
    else:
        return 0
def parse_shipping_price(text):
    '''
    takes input as string and returns price with no decimal
    
    >>> parse_shipping_price('+$24.34 shipping')
    2434
    >>> parse_shipping_price('Free shipping')
    0

    '''
    numbers = ''
    for char in text:
        if char in '1234567890':
            numbers+= char
    if "Free shipping" in text:
        return 0
    elif len(numbers)<2:
        return 0
    else:
        return int(numbers)

def parse_item_price(text):
    '''
    returns price with no $ and in cents

    >>>parse_item_price('$15.95')
    1595
    '''
    cents = ''
    for char in text:
        if char == 't':
            break
        if char in '1234567890':
            cents+= char
    if not cents:
        return None
    else:
        return int(cents)


if __name__ =='__main__':    

    #get command line arguements
    parser = argparse.ArgumentParser(description='download information from ebay and convert to JSON')
    parser.add_argument('search_term')
    parser.add_argument('--num_pages', default=10)
    args = parser.parse_args()
    print('args.search_terms', args.search_term)

    #list of all items in ebay webpages
    items=[]

    #loop over ebay webpages
    for page_number in range(1,int(args.num_pages)+1):
        
        #build url per page
        url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=' 
        url += args.search_term 
        url += '&_sacat=0LH_Title_Desc=0&_pgn='
        url += str(page_number)
        url += '&rt=nc'
        print('url=', url)
        
        #download the html
        r = requests.get(url)
        status = r.status_code
        print('status=', status)
        html =r.text

        #process the html
        soup = BeautifulSoup(html,'html.parser')

        #loop over the items in the page 
        tags_items = soup.select(".s-item")
        for tag_item in tags_items:
            
            #extract the name
            name = None
            tags_name = tag_item.select(".s-item__title")
            for tag in tags_name:
                name = tag.text
            
            #extract the free returns
            freereturns = False
            tags_free_returns = tag_item.select('.s-item__free-returns')
            for tag in tags_free_returns:
                freereturns = True
            
            items_sold=None
            tags_items_sold = tag_item.select('.s-item__hotness')
            for tag in tags_items_sold:
                items_sold = parse_itemssold(tag.text)

            status = None
            tags_status = tag_item.select(".SECONDARY_INFO")
            for tag in tags_status:
                status = tag.text
            
            shipping = None
            tags_shipping = tag_item.select(".s-item__shipping, .s-item__logisticsCost")
            for tag in tags_shipping:
                shipping = parse_shipping_price(tag.text)
            
            price = None
            tags_price = tag_item.select(".s-item__price")
            for tag in tags_price:
                price = parse_item_price(tag.text)

            

            
            #extract te
            
            item = {
                'name': name,
                'free_returns': freereturns,
                'items_sold': items_sold,
                'status': status,
                'shipping': shipping,
                'price': price
            }
            items.append(item)
            

        print("len(tags_items)=", len(tags_items))
        print( "len(items)=" ,len(items))

    #create the json file
    filename = args.search_term +'.json'
    with open (filename, 'w', encoding= 'ascii')as f:
        f.write(json.dumps(items))