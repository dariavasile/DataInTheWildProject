# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 15:11:40 2023

@author: Usuario
"""


import pandas as pd

# Sample data with a "sizes" column
data = pd.read_csv("./shein_raw_data.csv")
df = pd.DataFrame(data)
print(df.head())

remo = ['EUR36 to EUR43', '39-42 to 39-42','CN35 to CN40', 'one-size']
df = df[~df['sizes'].str.contains('|'.join(remo))]
df['sizes'] = df['sizes'].str.replace('W26 L32 to W32 L32','S to L')
df['sizes'] = df['sizes'].str.replace('W26 L32 to W31 L32','S to M')
df['sizes'] = df['sizes'].str.replace('to','')
df['sizes'] = df['sizes'].str.replace('Petite','')
df['sizes'] = df['sizes'].str.replace('Tall','')
df[['size 1', 'size 2', 'size 3', 'size 4']] = df['sizes'].str.split(r'  |-', expand=True)
df['converted_sizes'] = df[['size 1', 'size 2', 'size 3', 'size 4']].apply(
        lambda x: '/'.join(x.dropna().astype(str)), axis=1)
del df['size 1']
del df['size 2']
del df['size 3']
del df['size 4']

# Define a function to extract minimum and maximum sizes
def extract_min_max_sizes(sizes):
    size_list = sizes.split('/')
    size_list = [s.strip() for s in size_list]
    sizes_order = ['XXS','XS', 'S', 'M', 'L', 'XL', '1XL', 'XXL','2XL','3XL','4XL','5XL', '6XL']
    min_size = max_size = None

    for size in size_list:
        if size in sizes_order:
            if min_size is None or sizes_order.index(size) < sizes_order.index(min_size):
                min_size = size
            if max_size is None or sizes_order.index(size) > sizes_order.index(max_size):
                max_size = size

    return min_size, max_size

# Apply the function to create new columns
df[['min_size', 'max_size']] = df['converted_sizes'].apply(extract_min_max_sizes).apply(pd.Series)

# Size converter
def size_converter(sizes,categ):
    size_list = sizes.split('/')
    conversion = ''
    size_list = [s.strip() for s in size_list]
    benchmark = ['XXS','XS', 'S', 'M', 'L', 'XL', 'XXL','2XL','3XL','4XL','5XL']
    if size_list[0] in benchmark:
        return sizes
    if 'Jeans' in categ or 'Pants' in categ or 'Shorts' in categ or 'Skirts' in categ:
        for size in size_list:
            if size=='22' or size=='23':
                conversion += 'XXS/'
            elif size=='24' or size=='25':
                conversion += 'XS/'
            elif (size=='26' or size=='27' or size=='28'):
                conversion += 'S/'
            elif (size=='29' or size =='30' or size=='31'):
                conversion += 'M/'
            elif (size=='32' or size =='33' or size=='34' or size =='35'):
                conversion += 'L/'
            elif (size=='36' or size =='37' or size=='38' or size =='39' or size=='40'):
                conversion += 'XL/'
            elif (size=='41' or size =='42' or size=='43' or size =='44' or size=='45'):
                conversion += 'XXL/'

    return conversion

t = df[df['min_size'].isnull()]
t['converted_sizes1'] = t.apply(lambda x: size_converter(x['converted_sizes'],x['categ_name']), axis=1)
print(t['converted_sizes1'])

# Assuming you have a DataFrame 'df' and another DataFrame 't' with a column 'converted_sizes1'
df.loc[df['min_size'].isnull(), 'converted_sizes'] = t['converted_sizes1']

# Apply the function to create new columns
df[['min_size', 'max_size']] = df['converted_sizes'].apply(extract_min_max_sizes).apply(pd.Series)


df.loc[df['min_size'].isnull(), 'converted_sizes'] = df[df['min_size'].isnull()]['sizes'].str.split(r'  |-', expand=True).apply(
        lambda x: '/'.join(x.dropna().astype(str)), axis=1)


df.loc[df['min_size'].isnull(), 'converted_sizes'] = df[df['min_size'].isnull()]['converted_sizes'].str.replace('0XL/US22/US32/34','XL/5XL')
df.loc[df['min_size'].isnull(), 'converted_sizes'] = df[df['min_size'].isnull()]['converted_sizes'].str.replace('0XL/US22/US28/30','XL/4XL')
df.loc[df['min_size'].isnull(), 'converted_sizes'] = df[df['min_size'].isnull()]['converted_sizes'].str.replace('8Y/13/14Y/US28/30','S/4XL')

# Apply the function to create new columns
df[['min_size', 'max_size']] = df['converted_sizes'].apply(extract_min_max_sizes).apply(pd.Series)

del df['Unnamed: 0']
df.to_csv('./shein_clean_data.csv')

print('done')