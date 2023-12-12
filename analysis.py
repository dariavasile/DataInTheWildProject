import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm


size_df = pd.read_csv('./all_data_clean.csv')

benchmark = ['XXS','XS', 'S', 'M', 'L', 'XL', 'XXL','2XL','3XL','4XL','5XL', '6XL']
tot = len(benchmark)

columns = ['XXS', 'XS', 'S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL', '6XL']
 
def sizes(row, columns):

    lst = row['standard_sizes'].split('/')
    size_lst = [s.strip() for s in lst] 
    
    for i in range(len(size_lst)):
        if size_lst[i] == '0XL' or size_lst[i] == '1XL':
            size_lst[i] = 'XL'

        if size_lst[i] == 'XXL':
            size_lst[i] = '2XL'

        if size_lst[i] == 'XXXL':
            size_lst[i] = '3XL'

        if size_lst[i] == 'XXXXL':
            size_lst[i] = '4XL'
        
        if size_lst[i] == 'XXXXXL':
            size_lst[i] = '5XL'

        if size_lst[i] == '2XS':
            size_lst[i] = 'XXS'

        if size_lst[i] == 'XXXXXXL':
            size_lst[i] = '6XL'

        for col in columns:
            if col in size_lst:
                row[col] = 1
            else:
                row[col] = 0

        return row

size_df = pd.DataFrame(columns = columns)            

size_df = pd.concat([df, size_df])

for i, row in size_df.iterrows():
    size_df.loc[i] = sizes(row, columns)

colors = sns.cubehelix_palette(8)

### PLOT SIZE DISTRIBUTION PER SHOP ###
shein_data = size_df[size_df['shop'] == 'Shein']
asos_data = size_df[size_df['shop'] == 'Asos']
hm_data = size_df[size_df['shop'] == 'H&M']

size_counts_shein = shein_data[columns].sum()
size_counts_asos = asos_data[columns].sum()
size_counts_hm = hm_data[columns].sum()

# Set y-axis ticks consistently
yticks = [0, 1000, 2000, 3000, 4000]

# Plotting
plt.figure(figsize=(5, 7))

plt.subplot(3, 1, 1)
size_counts_shein.plot(kind='bar', color=colors[1], edgecolor='black')
plt.title('Shein')
plt.xticks(rotation=0)
plt.yticks([0, 500, 1500, 2500])  # Set consistent y-axis ticks

plt.subplot(3, 1, 2)
size_counts_asos.plot(kind='bar', color=colors[3], edgecolor='black')
plt.title('Asos')
plt.ylabel('Product Count')
plt.xticks(rotation=0)
plt.yticks([0, 500, 1500, 2500])  # Set consistent y-axis ticks

plt.subplot(3, 1, 3)
size_counts_hm.plot(kind='bar', color=colors[5], edgecolor='black')
plt.title('H&M')
plt.xlabel('Size')
plt.xticks(rotation=0)
plt.yticks(yticks)  # Set consistent y-axis ticks

plt.tight_layout()
plt.show()

### HEATMAP WITH SIZE & CATEGORY ###

columns.append('category')
cmap = sns.cubehelix_palette(as_cmap=True)

categ_shien = shein_data[columns].groupby('category').sum()
plt.figure(figsize=(12,8))
sns.heatmap(categ_shien, cmap=cmap, annot=True, fmt='d', cbar_kws={'label': 'Item Count'})
plt.title("Sizes and Categories in Shien")
plt.xlabel('Size')
plt.ylabel('Category')

categ_asos = asos_data[columns].groupby('category').sum()
plt.figure(figsize=(12,8))
sns.heatmap(categ_asos, cmap=cmap, annot=True, fmt='d', cbar_kws={'label': 'Item Count'})
plt.title("Sizes and Categories in Asos")
plt.xlabel('Size')
plt.ylabel('Category')

categ_hm = hm_data[columns].groupby('category').sum()
plt.figure(figsize=(12,8))
sns.heatmap(categ_hm, cmap=cmap, annot=True, fmt='d', cbar_kws={'label': 'Item Count'})
plt.title("Sizes and Categories in H&M")
plt.xlabel('Size')
plt.ylabel('Category')

columns.remove('category')
plt.show()

### PLOT DISTRIBUTION BY GENDER ###

men_data = asos_data[asos_data['gender'] == 'male']
women_data = asos_data[asos_data['gender'] == 'female']

men_data_asia = men_data[men_data['region'] == 'asia']
women_data_asia = women_data[women_data['region'] == 'asia']

size_counts_men = men_data_asia[columns].sum()
size_counts_women = women_data_asia[columns].sum()

plt.figure(figsize=(10, 7))
plt.subplot(1, 2, 1)
size_counts_men.plot(kind='bar', color=colors[1], edgecolor='black')
plt.title('Men Size Distribution')
plt.xlabel('Size')
plt.ylabel('Count')
plt.xticks(rotation=0)  

plt.subplot(1, 2, 2)
size_counts_women.plot(kind='bar', color=colors[3], edgecolor='black')
plt.title('Women Size Distribution')
plt.xlabel('Size')
plt.ylabel('Count')
plt.xticks(rotation=0)  

plt.show()

### PLOT QUALITY PERCEIVEMENT VS PRICE PER SHOP ###

hm_data = hm_data[hm_data['standardised_price_eur'] < 300]

for df in [asos_data, shein_data, hm_data]:
    df['material quality label'] = pd.Categorical(df['material quality label'], categories=['low', 'medium', 'high'], ordered=True)

plt.figure(figsize=(10, 6))
plt.subplot(1, 3, 1)
sns.scatterplot(x='material quality label', y='standardised_price_eur', data=asos_data, color=colors[3], alpha=0.3)
plt.xlabel('')
plt.ylabel('Price (EUR)')
plt.title('Asos')

plt.subplot(1, 3, 2)
sns.scatterplot(x='material quality label', y='standardised_price_eur', data=shein_data, color=colors[5], alpha=0.3)
plt.xlabel('Quality')
plt.ylabel('')
plt.title('Shein')

plt.subplot(1, 3, 3)
sns.scatterplot(x='material quality label', y='standardised_price_eur', data=hm_data, color=colors[7], alpha=0.3)
plt.xlabel('')
plt.ylabel('')
plt.title('H&M')

plt.tight_layout()
plt.show()


### COMPUTE AVERAGE PRICE PER SIZE IN EACH SHOP###
asos_prices = []
hm_prices = []
shein_prices = []

for col in columns:
    filtered_shein = shein_data[shein_data[col] == 1]
    filtered_hm = hm_data[hm_data[col] == 1]
    filtered_asos = asos_data[asos_data[col] == 1]

    shein_avg = filtered_shein['standardised_price_eur'].mean()
    hm_avg = filtered_hm['standardised_price_eur'].mean()
    asos_avg = filtered_asos['standardised_price_eur'].mean()

    shein_prices.append(shein_avg)
    asos_prices.append(asos_avg)
    hm_prices.append(hm_avg)


yticks = [0, 25, 50, 75, 100, 125, 150]

shop_colors = {'Shein': colors[5], 'Asos': colors[3], 'H&M': colors[7]}

print(asos_prices)

plt.figure(figsize=(6, 3))
plt.bar(columns, hm_prices, color=colors[5])
plt.title('H&M')
plt.ylabel('Average Price (EUR)')
plt.xticks(rotation=0)
plt.xlabel('Size')
plt.yticks([0, 15, 30, 45])

plt.subplot(3, 1, 2)
plt.bar(columns, asos_prices, color=colors[5])
plt.title('Asos')
plt.ylabel('Average Price (EUR)')
plt.xticks(rotation=0)
plt.yticks([0, 50, 100, 150])

plt.subplot(3, 1, 3)
plt.bar(columns, hm_prices, color=colors[7])
plt.title('H&M')
plt.xlabel('Size')
plt.xticks(rotation=0)
plt.yticks([0, 50, 100, 150])
# plt.yticks([0, 15, 30, 45])

plt.tight_layout()
plt.show() 