import urllib.request
import json
import datetime
import pandas as pd
from bs4 import BeautifulSoup
import requests
from django.conf import settings
import csv
import ssl
import os


class NaverShoppingCrawler:
    def __init__(self, client_id, client_secret, keyWord):
        self.client_id = client_id
        self.client_secret = client_secret
        self.keyWord = keyWord

    def gen_search_url(self, api_node, start_num, disp_num):
        base = 'https://openapi.naver.com/v1/search'
        node = '/' + api_node + '.json'
        param_query = '?query=' + urllib.parse.quote(self.keyWord)
        param_start = '&start=' + str(start_num)
        param_disp = '&display=' + str(disp_num)
        return base + node + param_query + param_disp + param_start

    def get_result_onpage(self, url):
        request = urllib.request.Request(url)
        request.add_header('X-Naver-Client-Id', self.client_id)
        request.add_header('X-Naver-Client-Secret', self.client_secret)
        response = urllib.request.urlopen(request)
        print(f'{datetime.datetime.now()} Url Request Success')
        return json.loads(response.read().decode('utf-8'))

    def delete_tag(self, input_str):
        input_str = input_str.replace('<b>', '')
        input_str = input_str.replace('</b>', '')
        input_str = input_str.replace('\xa0', '')
        return input_str

    def get_fields(self, json_data):
        title = [self.delete_tag(each['title']) for each in json_data['items']]
        link = [each['link'] for each in json_data['items']]
        lprice = [each['lprice'] for each in json_data['items']]
        mall_name = [each['mallName'] for each in json_data['items']]
        result = pd.DataFrame({
            'title': title,
            'link': link,
            'lprice': lprice,
            'mall': mall_name,
        }, columns=['title','lprice','mall','link'])
        return result
    '''
    def run(self):
        result_datas = []
        for n in range(1, 1000, 100):
            url = self.gen_search_url('shop', n, 100)
            json_result = self.get_result_onpage(url)
            result = self.get_fields(json_result)
            result_datas.append(result)
        result_datas_concat = pd.concat(result_datas)
        result_datas_concat.reset_index(drop=True, inplace=True)
        #result_datas_concat['lprice'] = result_datas_concat['lprice'].str.replace(' ', '').astype(int)
        processed_dataframe = 'dataframes/data_processed.csv'
        processed_data_path = os.path.join(settings.MEDIA_ROOT, processed_dataframe)
        result_datas_concat.to_csv(processed_data_path, sep=',', encoding="utf-8")
    '''
    def run(self):
        result_datas = []
        for n in range(1, 1000, 100):
            url = self.gen_search_url('shop', n, 100)
            json_result = self.get_result_onpage(url)
            result = self.get_fields(json_result)
            result_datas.append(result)
        result_datas_concat = pd.concat(result_datas)
        result_datas_concat.reset_index(drop=True, inplace=True)
        #result_datas_concat['lprice'] = result_datas_concat['lprice'].str.replace(' ', '').astype(int)
        processed_dataframe = 'dataframes/naver_products.csv' # 크롤링 수정 (파일명 변경)
        processed_data_path = os.path.join(settings.MEDIA_ROOT, processed_dataframe)
        result_datas_concat.to_csv(processed_data_path, sep=',', encoding="utf-8")



class SsgCrawler:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

    def get_data(self, query):
        url = "https://www.ssg.com/search.ssg?target=all&query=" + query

        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'lxml')

        if response.status_code != 200:
            print(response.status_code)
            return None  # 데이터 수집 실패 시 None 반환

        product_names = []
        prices = []
        product_urls = []

        for li in soup.find_all('li', class_='cunit_t232'):
            product_name = None  # 초기화
            price = None  # 초기화
            product_url = None  # 초기화
            
            if li.find('div', class_='title'):
                product_name = li.find('div', class_='title').text.strip()
            
            if li.find('em', class_='ssg_price'):
                price = li.find('em', class_='ssg_price').text.strip()
            
            if li.find('a', class_='clickable'):
                product_url = 'https://www.ssg.com' + li.find('a', class_='clickable')['href']

            product_names.append(product_name)
            prices.append(price)
            product_urls.append(product_url)

        # 데이터를 데이터프레임으로 반환
        data = {
            'product_names': product_names,
            'prices': prices,
            'product_urls': product_urls
        }
        df = pd.DataFrame(data)
        df = df.sort_values(by='prices')  # 가격순으로 정렬

        return df  # 크롤링 수정 (데이터 프레임 리턴으로 변경)


class MusinsaCrawler:
    def __init__(self, query):
        self.query = query
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        self.url = "https://www.musinsa.com/search/musinsa/integration?q=" + self.query

    def scrape(self):
        response = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'lxml')

        result = []
        goods_links = soup.find_all('a', attrs={'name': 'goods_link'})
        prices = soup.find_all('p', attrs={'class': 'price'})

        for link, price in zip(goods_links, prices):
            title = link.get('title')
            price_text = price.find('del')

            if price_text is not None:
                price_text.extract()

            price_text = price.text.strip().replace('원', '').replace(',', '')
            link = link.get('href')

            result.append((title, price_text, link))

        df = pd.DataFrame(result, columns=['Product_Name', 'Price', 'Product_Link'])
        df['Price'] = df['Price'].str.replace(',', '').astype(int)
        return df