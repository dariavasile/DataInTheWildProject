# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 20:15:56 2023

@author: Usuario
"""


import requests
import json
import pandas as pd 

url = "https://unofficial-shein.p.rapidapi.com/products/search"
url_det = "https://unofficial-shein.p.rapidapi.com/products/detail"

# Dictionary of clothing items to retrieve
keywords = ['dress', 'tshirt', 'shirt', 'top', 'knitwear', 'sweater', 
            'hoodie', 'jeans', 'pants', 'trousers', 'cardigan', 'sweatshirt',
            'jumpsuit', 'sweatpants', 'coat', 'jacket', 'skirt', 'shorts']


# Dictionary of goods
products = {'prod_id': [], 'prod_name':[],'img_url1': [], 
            'img_url2': [], 'categ_id':[], 'categ_name': [], 'color':[],
            'currency':[],'prod_price': [], 'prod_label': [],'sizes':[], 
            'style': [], 'pattern': [], 'sleeve': [], 'waist': [], 'length': [],
            'fit': [],'fabric': [], 'material': [], 'composition': [], 'sex': []}

df = pd.DataFrame(products)

gender = 'women' # Change desired gender (women or men)

for key in keywords:
    keyg = key + gender
  
    for page in range(3):
        querystring = {"keywords":str(keyg),"language":"en",
                       "country":"US","currency":"USD","sort":"0",
                       "limit":"30","page": str(page)}
        headers = {
                	"X-RapidAPI-Key": "4aaa0bbad6mshd8eb349af8605dap1d92d7jsn7101e64d9496",     # Add your credentials here
                	"X-RapidAPI-Host": "unofficial-shein.p.rapidapi.com"
                }   
        
        response = requests.get(url, headers=headers, params=querystring)
        response_json = json.loads(response.text) 
                
        
        for i in range(len(response_json['info']['products'])):
            prod_id = response_json['info']['products'][i]['goods_id']
            prod_name = response_json['info']['products'][i]['goods_name']
            im1 = response_json['info']['products'][i]['goods_img']
            im2 = response_json['info']['products'][i]['detail_image']
            catid = response_json['info']['products'][i]['cat_id']
            catname = response_json['info']['products'][i]['cate_name']
            curr = querystring['currency']
            saleprice = response_json['info']['products'][i]['salePrice']['amount']
            label = response_json['info']['products'][i]['series_badge']['name']
           
            
            # Get request using product ID
            querystring_det = {"goods_id":str(prod_id),"language":"en","country":"US","currency":"USD"}
            response_det = requests.get(url_det, headers=headers, params=querystring_det)
            json_det =  json.loads(response_det.text)

            # Get size range
            list_size = json_det['info']['multiLevelSaleAttribute']['skc_sale_attr'][0]['attr_value_list']
            prod_range = list_size[0]["attr_value_name"] + " to " + list_size[-1]["attr_value_name"]
            products['sizes'] = prod_range

            # Get product details
            dets = json_det['info']['productDetails']
            sle =  None
            pat = None
            col = None
            st = None
            waist =  None
            le =  None
            fit =  None
            fab =  None
            mat =  None
            com = None
            
            for item in dets:
                if item['attr_name']=='Color':
                    col = item['attr_value']
                elif item['attr_name']=='Style':
                    st = item['attr_value']
                elif item['attr_name']=='Pattern Type':
                    pat = item['attr_value']
                elif item['attr_name']=='Sleeve Length':
                    sle = item['attr_value']
                elif item['attr_name']=='Waist Line':
                    waist = item['attr_value']

                elif item['attr_name']=='Length':
                    le = item['attr_value']
      
                elif item['attr_name']=='Fit Type':
                    fit = item['attr_value']
                    
                elif item['attr_name']=='Fabric':
                    fab = item['attr_value']
                  
                elif item['attr_name']=='Material':
                    mat = item['attr_value']
                    
                elif item['attr_name']=='Composition':
                    com =  item['attr_value']

            # Append data for each product
            data = {
                'prod_id': [prod_id],
                'prod_name': [prod_name],
                'img_url1': [im1],
                'img_url2': [im2],
                'categ_id': [catid],
                'categ_name': [catname],
                'color': [col],
                'currency': [curr],
                'prod_price': [saleprice],
                'prod_label': [label],
                'sizes': [prod_range],
                'style': [st],
                'pattern': [pat],
                'sleeve': [sle],
                'waist': [waist],
                'length': [le],
                'fit': [fit],
                'fabric': [fab],
                'material': [mat],
                'composition': [com],
                'sex': [gender]    
                }
            df = df.append(pd.DataFrame(data), ignore_index=True)


df.to_csv("shein_raw_data.csv", index=False)  
    

print('Done')
