# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 11:31:15 2023

@author: Usuario
"""


import requests
import json
import pandas as pd 

url = "https://apidojo-hm-hennes-mauritz-v1.p.rapidapi.com/products/list"
url_det = "https://apidojo-hm-hennes-mauritz-v1.p.rapidapi.com/products/detail"

# Dictionary of clothing items to retreive per gender 
keywords_ladies = ['dresses', 'tops_tshirts', 'shirtsblouses', 'cardigansjumpers_jumpers', 
            'hoodiesswetshirts_hoodies', 'jeans', 'basics_trousersleggings', 
              'trousers',
               'cardigansjumpers_cardigans', 'hoodiesswetshirts_sweatshirts',
            'jumpsuits', 'jacketscoats_coats', 'jacketscoats_jackets',
             'skirts', 'shorts']\
             
keywords_men = ['tshirtstanks', 'shirts', 'cardigansjumpers', 
            'hoodiessweatshirts', 'jeans','trousers', 'hoodiesswetshirts_sweatshirts',
            'blazerssuits', 'jacketscoats', 'jacketscoats_jackets', 
              'sport_bottoms_trousers','sport_bottoms_shorts']


# Dictionary of goods
products = {'prod_id': [], 'prod_name':[],'img_url1': [], 
            'img_url2': [], 'categ_id':[], 'categ_name': [], 'color': [],
            'currency': [],'prod_price': [],'prod_label': [], 'sizes':[],
             'style':[], 'sleeve': [], 'waist': [], 'length': [],
             'fit': [],'composition':[], 'sex':[]
            }


df = pd.DataFrame(products)

gender = 'ladies_'  # Change desired gender ('ladies_' or 'men_')

for key in keywords_ladies:
    keyg = gender + key   
    print(keyg)
    for page in range(3):
        querystring = {"country":"us","lang":"en","currentpage": str(page),"pagesize":"30",
                       "categories": str(keyg)}
        
        headers = {
            	"X-RapidAPI-Key": "5b454c715bmsh1d2bca73b441e21p1bd757jsn5e453d92447c",   # Add your credentials here
            	"X-RapidAPI-Host": "apidojo-hm-hennes-mauritz-v1.p.rapidapi.com"
            } 
        
        response = requests.get(url, headers=headers, params=querystring)
        response_json = json.loads(response.text) 
                       
        for i in range(len(response_json['results'])):
            prod_id = response_json['results'][i]['articles'][0]['code']
            prod_name = response_json['results'][i]['name']
            im1 = response_json['results'][i]['images'][0]['baseUrl']
            im2 = response_json['results'][i]['articles'][0]['normalPicture'][0]['baseUrl']
            curr = response_json['results'][i]['price']['currencyIso']
            saleprice = response_json['results'][i]['price']['value']
            color = response_json['results'][i]['articles'][0]['color']['text']
            sizes = response_json['results'][i]['variantSizes']
            size = ''

            for it in sizes:
                size += it["filterCode"] + '/'

            # Get details for each product
            querystring_det = {"lang":"en","country":"us","productcode":str(prod_id)}
            response_det = requests.get(url_det, headers=headers, params=querystring_det)
            json_det =  json.loads(response_det.text) 

            # Details   
            sle =  None
            waist =  None
            le =  None
            fit = None
            st = None
            label = None
            comp = ''

            if 'fits' in json_det['product']:
                fit = json_det['product']['fits'][0]
            
            prod_mes = json_det['product']['lengthCollection']

            for item in prod_mes:
                if 'sleeve' in item['code']:
                    sle = item['value'][0]
                elif 'waist' in item['code']:
                    wa = item['value'][0]
                else:
                    le = item['value'][0]

            catname = json_det['product']['mainCategory']['name']
            catid = json_det['product']['mainCategory']['code']

            if 'compositions' in json_det['product']['articlesList'][0]:
                com = json_det['product']['articlesList'][0]['compositions'][0]['materials']
                for mate in com:
                    comp += mate['name'] + ' '

            prod_st = json_det['product']['styleCollection']

            for item in prod_st:
                if 'clothing' in item['code']:
                    style = item['value'][0]
            
            if 'concepts' in json_det['product']['articlesList'][0]:
                labi = json_det['product']['articlesList'][0]['concepts']
                label = ''
                for u in labi:
                    label += labi + ' '
            else:
                label = json_det['product']['supercategories'][0]['name']

            # Append data for each product
            data = {
                'prod_id': [prod_id],
                'prod_name': [prod_name],
                'img_url1': [im1],
                'img_url2': [im2],
                'categ_id': [catid],
                'categ_name': [catname],
                'color': [color],
                'currency': [curr],
                'prod_price': [saleprice],
                'prod_label': [label],
                'sizes': [size],
                'style': [st],
                'sleeve': [sle],
                'waist': [waist],
                'length': [le],
                'fit': [fit],
                'composition': [comp],
                'sex': [gender]
                }
            df = df.append(pd.DataFrame(data), ignore_index=True)


df.to_csv("hm_raw_data.csv", index=False)  
    
print('Done')
