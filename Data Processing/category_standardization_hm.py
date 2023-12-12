# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 14:26:57 2023

@author: Usuario
"""

import pandas as pd

data = pd.read_csv("./hm_clean_data.csv")
df = pd.DataFrame(data)


# for all plus sizes get the name of the category
t = df[df['category']=='ladies_plus']['product_name']
def cant(name):
    prod = name.split(' ')
    return prod[-1]

df.loc[df['category']=='ladies_plus','category'] = t.apply(cant)


def categ_standardize(categ):
    categ = str(categ).lower()
    keywords = ['dress', 'tshirts', 'shirts', 'tops', 'knitwear', 'sweaters', 
                'hoodie', 'jeans', 'pants', 'trousers', 'cardigan', 'sweatshirts',
                'jumpsuit', 'sweatpants', 'coats', 'jackets', 'skirts', 'shorts', 'nightwear']
    
    for key in keywords:
        if key in categ:
            categ = key.lower()
            return categ
        elif 't-shirt' in categ or 'tee' in categ or 'tshirt' in categ or 'tank' in categ:
            categ = 'tshirts'
            return categ
        elif 'outerwear' in categ or 'blazer' in categ or 'jacket' in categ:
            categ = 'jackets'
            return categ
        elif 'leggings' in categ or 'joggers' in categ:
            categ = 'pants'
            return categ
        elif 'bodysuits' in categ or 'top' in categ:
            categ = 'tops'
            return categ
        elif 'blouse' in categ or 'shirt' in categ:
            categ = 'shirts'
            return categ
        elif 'romper' in categ:
            categ = 'jumpsuit'
            return categ
        elif 'sweater' in categ:
            categ = 'sweaters'
            return categ
        elif 'sweatshirt' in categ:
            categ = 'sweatshirts'
            return categ
        elif 'skirt' in categ:
            categ = 'skirts'
            return categ
        elif 'pyjamas' in categ or 'pajamas' in categ or 'underwear' in categ or 'lingerie' in categ or 'loungewear' in categ or 'pajama' in categ:
            categ = 'nightwear'
            return categ
        
        
df['category'] = df['category'].apply(categ_standardize).apply(pd.Series)

# we drop nan values for products that are irrelevant
df = df[~df['category'].isnull()]
# drop accessories
df = df[~df['max_size'].isnull()]

df.to_csv('.hm_clean_data.csv', index=False)

