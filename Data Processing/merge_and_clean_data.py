import pandas as pd
import random

exchange_rates = {'USD': 0.93, 'CNY': 0.13, 'NOK': 0.084, 'EUR': 1, 'HKD': 0.12, 'TWD':0.029}

file1 = './asos_clean_data.csv'
file2 = './hm_clean_data.csv'
file3 = './shein_clean_data.csv'

df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)
df3 = pd.read_csv(file3)

columns = ['product_id', 'product_name', 'img_url', 'category', 'currency','price'
           , 'color', 'fit', 'composition', 'gender', 'country', 'region',
            'brand_name', 'shop', 'sizes', 'standard_sizes', 'min_size', 'max_size']

df = pd.merge(df1, df2, on=columns)
df = pd.merge(df, df3, on=columns)

def change_gender(x):
    if isinstance(x, str):
       x = str.lower(x)
    else:
        return x
    if 'm' in x:
        return 'male'
    elif 'w' in x or 'f' in x:
        return 'female'
    elif x == 'unisex':
        random_number = random.randint(0, 1)
        if random_number == 0:
            return 'male'
        else :
            return 'female'

def change_region(x):
    if isinstance(x, str):
       x = str.lower(x)
    else:
        return x
    
    if x == 'usa' or x == 'us':
        return 'usa'
    if x == 'asia':
        return 'asia'
    if x == 'eu' or x == 'europe':
        return 'eu'
    

def convert_price(row):
    if pd.isna(row['currency']):
        return None
    amount = row['price']
    currency = row['currency']

    exchange_rate = exchange_rates.get(currency)
    price_eur = amount * exchange_rate
    price_eur = round(price_eur, 3)

    return price_eur

def fill_country(row):
    if pd.isna(row['country']):
        if row['currency'] == 'USD':
            return 'usa'
        elif row['currency'] == 'CNY':
            return 'china'
        elif row['currency'] in ['NOK', 'EUR']:
            return 'norway'
        elif row['currency'] == 'HKD':
            return 'hong kong'
    
    return str.lower(str(row['country']))



df['color'] = df['color'].str.lower()

df['fit'] = df['fit'].str.lower()

df['composition'] = df['composition'].str.lower()
df['composition'] = df['composition'].str.replace(r'[%\d]+', '').str.replace(',', ' ')

df['gender'] = df['gender'].apply(change_gender)
df['region'] = df['region'].apply(change_region)

df['standard_sizes'] = df['standard_sizes'].str.replace(',', '/')

df['standardised_price_eur'] = df.apply(convert_price, axis=1)

df['country'] = df.apply(fill_country, axis=1)

df.to_csv('./all_data.csv', index=False)