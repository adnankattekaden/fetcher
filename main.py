import requests
from bs4 import BeautifulSoup
import pandas as pd
from links_list import urls
import os
import time


products = {}

locations = {
    'kochi': {},
    'thiruvandapuram': {},
    "coimbatore": {},
}


def get_product_details(url):
    for product_name, url in url.items():
        product_name = product_name
        url = url

    vendor = url.split('.')[1]

    request = requests.get(url)
    soup = BeautifulSoup(request.content, 'lxml')

    if vendor == "luluhypermarket":
        price = soup.findAll('span', class_="item price")[0].text.split()[-1]
        product_mass = soup.findAll('h1', class_='product-name')[0].text.strip().split()[-1]
        location = "kochi"

    elif vendor == "klfresh":
        price_and_mass = soup.find('span', class_="t3-mainPrice mr-5").text.split()
        product_mass = price_and_mass[3]
        price = price_and_mass[1]
        location = "kochi"

    elif vendor == "kada":
        product_details = soup.find("div", "rightDetailHolder")
        product_mass = product_details.h2.get_text().split()[-1]
        price = product_details.find("span", class_="rupee_symbol").text
        location = "thiruvandapuram"

    elif vendor == "jiomart":
        product_mass = '1 kg'  # have to fix mass problem Jio Mart Beta
        price = soup.find_all("span", class_="final-price")
        for i in price:
            price = i.text.split(":")[-1].replace('₹', '')
        location = "kochi"

    elif vendor == "bigbasket":
        product_details = soup.find_all("h1", class_="GrE04")
        product_mass = product_details[0].text.split(',')[-1]
        price = soup.find_all("td", class_="IyLvo")
        price = price[0].get_text().split()[-1]
        location = "kochi"

    elif vendor == 'findfresh':
        price = soup.find('p', class_='reduced').text.split()[-1].replace('₹', '')
        product_mass = soup.find('div', 'single-right').h3.text.split('(')[-1].replace(')', '')
        location = 'kochi'

    if price == []:
        price = '0'

    return product_name,product_mass,float(price),location,vendor



for url in urls:
    product_name, product_mass, price, location, vendor = get_product_details(url)

    products[product_name] = product_mass

    details = {
        'price': price,
        'mass': product_mass,
    }

    if location in locations:
        if vendor in locations[location]:
            locations[location][vendor].update({product_name:details})
        else:
            locations[location][vendor] = {product_name:details}



my_list = []
my_list.append(['Name', 'Mass', '', 'Coimbatore', '', '', '', 'Tvm', '', '', '', '', 'Kochi', '', ''])
my_list.append(['', '', 'BigBasket', 'JioMart', 'VegRoot', '', 'kada.in', 'amneeds', 'JioMart', '', 'BigBasket', 'JioMart','KL Fresh', 'Lulu Hypermart', 'findfresh'])


print(products)

for product_name,mass in products.items():
    my_list.append([product_name,mass,
                    # locations['coimbatore']['bigbasket'][product_name]['price'],
                    0,
                    # locations['coimbatore']['bigbasket'][product_name]['price'],
                    0,
                    # locations['coimbatore']['bigbasket'][product_name]['price'],
                    0,
                    '',

                    # locations['thiruvandapuram']['kada'][product_name]['price'],
                    0,
                    # locations['thiruvandapuram']['jiomart'][product_name]['price'],
                    0,
                    # locations['thiruvandapuram']['jiomart'][product_name]['price'],
                    0,
                    '',

                    locations['kochi']['bigbasket'][product_name]['price'] if product_name in locations['kochi'][
                        'bigbasket'] else '0',
                    locations['kochi']['jiomart'][product_name]['price'] if product_name in locations['kochi'][
                        'jiomart'] else '0',
                    locations['kochi']['klfresh'][product_name]['price'] if product_name in locations['kochi'][
                        'klfresh'] else '0',
                    locations['kochi']['luluhypermarket'][product_name]['price'] if product_name in locations['kochi'][
                        'luluhypermarket'] else '0',
                    locations['kochi']['findfresh'][product_name]['price'] if product_name in locations['kochi'][
                        'findfresh'] else '0',

                    ])

filename = 'case_array.csv'
path = "/home/loki/CompanyProject/Fetcher"
fullpath = os.path.join(path,filename)
df=pd.DataFrame(my_list)
print(df)
df.to_csv(fullpath, header=False)
