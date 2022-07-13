from ast import Num
from operator import index
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


class productCompare:
    def __init__(self, search_query) -> None:
        self.header = {
                    'User-Agent': 'Chrome/51.0.2704.103 Safari/537.36',
                    'Accept-Language': 'en-US, en;q=0.5'
                }

        self.amazon_base_url = 'https://www.amazon.in/s?k='
#myntra_base_url = 'https://www.myntra.com/'
        self.flipkart_base_url = 'https://www.flipkart.com/search?q='
        self.search_query = search_query

    def get_input(self):
        #search_query = input('enter the fashion product to search: ')

        amazon_query = self.search_query.replace(' ', '+')
        #myntra_query = search_query.replace(' ', '-')
        flipkart_query = self.search_query.replace(' ', '%20')

        amazon_search = self.amazon_base_url+amazon_query
        #myntra_search = myntra_base_url + myntra_query
        flipkart_search = self.flipkart_base_url + flipkart_query
        return amazon_search, flipkart_search

#myntra_items = []

    def scrape_amazon(self,search_url):
        
        print('processing ', search_url)
        amazon_items = {}
        Brand = []
        Des = []
        Ratings = []
        Num_rating = []
        Price = []
        Product_link = []
        Image = []
        response = requests.get(search_url, headers=self.header)
        soup = BeautifulSoup(response.content, 'html.parser')
        #print(soup)
        tags = soup.find_all('div', {'class':'s-result-item', 'data-component-type':'s-search-result'})
        #print(tags)
        for tag in tags:
            try:
                brand = tag.h5.text
            except:
                brand = 'None'
            try:
                description = tag.h2.text
                ratings = tag.find('i', {'class': 'a-icon'}).text
                ratings = ratings[:3]
                num_rating = tag.find('span', {'class':'a-size-base'}).text
                num_rating = int(num_rating.replace(',',''))
                price = tag.find('span', {'class':'a-price-whole'}).text
                product_link = tag.find('a', {'class': 'a-link-normal s-no-outline', 'target':'_blank'})
                product_link = product_link['href']
                product_link = self.amazon_base_url[:-5] + product_link
            except:
                continue
            try:
                image = tag.find('img', {'class': 's-image'})
                image = image['src']
            except:
                image = ''
            Brand.append(brand)
            Des.append(description)
            Ratings.append(ratings)
            Num_rating.append(num_rating)
            Price.append(price)
            Product_link.append(product_link)
            Image.append(image)
        amazon_items = {'brand' : Brand, 'description': Des, 'price': Price, 'ratings': Ratings, 'num_rating': Num_rating,
        'product_link': Product_link, 'image': Image}
            #amazon_items.append(amazon_item)
        """print('brand: ', brand)
            print('description: ', description)
            print('rating: ', ratings)
            print('num_rating: ', num_rating)
            print('price: ', price)"""
            
        return amazon_items
#scrape_amazon(amazon_search, header)

    def scrape_flipkart(self,search_url):

        print('processing ', search_url)
        flipkart_items = {}
        Brand = []
        Des = []
        Ratings = []
        Num_rating = []
        Price = []
        Product_link = []
        Image = []
        response = requests.get(search_url, headers=self.header)
        soup = BeautifulSoup(response.content, 'html.parser')
        #print(soup)
        tags = soup.find_all('div', {'class':'_1xHGtK _373qXS'})
        for tag in tags:
            try:
                brand = tag.find('div', {'class':'_2WkVRV'}).text
                description = tag.find('a', {'class': 'IRpwTa'}).text
            except:
                continue
            try:
                href = tag.find('a', {'class': '_2UzuFa'}, href = True) 
                product_link = href['href']
                product_link = 'https://www.flipkart.com' + product_link
                product_resp = requests.get(product_link, self.header)
                soup = BeautifulSoup(product_resp.content, 'html.parser')
                ratings = soup.find('div', {'class': '_3LWZlK'}).text
                num_rating = soup.find('span', {'class':'_2_R_DZ'}).text
                num_rating = num_rating.split()
                num_rating = num_rating[0]
                num_rating = int(num_rating.replace(',',''))
                price = tag.find('div', {'class':'_30jeq3'}).text
                price = price[1:]
            except:
                continue
            try:
                image = tag.find('img', {'class': '_2r_T1I'})
                image = image['src']
            except: image = ''
            

            Brand.append(brand)
            Des.append(description)
            Ratings.append(ratings)
            Num_rating.append(num_rating)
            Price.append(price)
            Product_link.append(product_link)
            Image.append(image)
        flipkart_items = {'brand' : Brand, 'description': Des, 'price': Price, 'ratings': Ratings, 'num_rating': Num_rating,
        'product_link': Product_link, 'image': Image}
            #print(rating, num_rating)
        return flipkart_items

#scrape_flipkart(flipkart_search, header)

    def compare(self):
        amazon_url, flipkart_url = self.get_input()
        amazon_items = self.scrape_amazon(amazon_url)
        flipkart_items = self.scrape_flipkart(flipkart_url)
        print(amazon_items)
        print(flipkart_items)
        data = pd.DataFrame(amazon_items)
        data = pd.concat([data, pd.DataFrame(flipkart_items)], axis = 0)
        data.to_excel('compare.xlsx', index=False)
        
        data_sorted = data.sort_values(['num_rating','ratings', 'price'], ascending=[False,False,True])
        print(data_sorted.columns.values)
        best = data_sorted.iloc[0:1, -2:-1]
        
        return best['product_link'].to_list()[0]
        