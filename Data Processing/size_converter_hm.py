import pandas as pd

data = pd.read_csv("./hm_raw_data.csv")
df = pd.DataFrame(data)

# Size converter
def size_converter(sizes, sex, categ_id):
    size_list = sizes.split('/')
    conversion = ''
    size_list = [s.strip() for s in size_list]
    benchmark = ['XXS','XS', 'S', 'M', 'L', 'XL', 'XXL','2XL','3XL','4XL','5XL']
    if size_list[0] in benchmark:
        for size in size_list:
            conversion = '/'.join(size_list)
    elif sex=='female':
        for size in size_list:
            if size=='0' or size=='32':
                conversion += 'XXS/'
            elif size=='2' or size=='34':
                conversion += 'XS/'
            elif (size=='4' or size=='6') or (size=='36' or size=='38'):
                conversion += 'S/'
            elif (size=='8' or size=='10') or (size=='40' or size=='42'):
                conversion += 'M/'
            elif (size=='12' or size=='14') or (size=='44' or size=='46'):
                conversion += 'L/'
            elif (size=='16' or size=='18') or (size=='48' or size=='50'):
                conversion += 'XL/'
            elif (size=='20' or size=='22') or (size=='52' or size=='54'):
                conversion += 'XXL/'
            elif (size=='24' or size=='26') or (size=='56' or size=='58'):
                conversion += '3XL/'
            elif (size=='28' or size=='30') or (size=='60' or size=='62'):
                conversion += '4XL/'
    elif sex=='male':
        if categ_id=='jeans':
            for size in size_list:
                if (size=='27' or size=='28'):
                    conversion += 'XS/'
                elif (size=='29' or size=='30'):
                    conversion += 'S/'
                elif (size=='31' or size=='32'):
                    conversion += 'M/'
                elif (size=='33' or size=='34'):
                    conversion += 'L/'
                elif (size=='36' or size=='38'):
                    conversion += 'XL/'
                elif (size=='40' or size=='42'):
                    conversion += 'XXL/'
                elif (size=='44' or size=='46'):
                    conversion += '3XL/'
        
        else: 
            for size in size_list:
                if (size=='30R' or size=='32R') or (size=='40' or size=='42'):
                    conversion += 'XS/'
                elif (size=='34R' or size=='36R') or (size=='44' or size=='46'):
                    conversion += 'S/'
                elif (size=='38R' or size=='40R') or (size=='48' or size=='50'):
                    conversion += 'M/'
                elif (size=='42R' or size=='44R') or (size=='52' or size=='54'):
                    conversion += 'L/'
                elif (size=='46R' or size=='48R') or (size=='56' or size=='58'):
                    conversion += 'XL/'
                elif (size=='50R' or size=='52R') or (size=='60' or size=='62'):
                    conversion += 'XXL/'
                elif (size=='54R' or size=='56R') or (size=='64' or size=='66'):
                    conversion += '3XL/'
            
    return conversion

# Define a function to extract minimum and maximum sizes
def extract_min_max_sizes(sizes):
    size_list = sizes.split('/')
    size_list = [s.strip() for s in size_list]
    sizes_order = ['XXS','XS', 'S', 'M', 'L', 'XL', 'XXL','2XL','3XL','4XL','5XL']
    min_size = max_size = None

    for size in size_list:
        if size in sizes_order:
            if min_size is None or sizes_order.index(size) < sizes_order.index(min_size):
                min_size = size
            if max_size is None or sizes_order.index(size) > sizes_order.index(max_size):
                max_size = size

    return min_size, max_size

df['converted_sizes'] = df.apply(lambda x: size_converter(x['sizes'],x['sex'],x['categ_id']), axis=1)
# Apply the function to create new columns
df[['min_size', 'max_size']] = df['converted_sizes'].apply(extract_min_max_sizes).apply(pd.Series)

df.to_csv("./hm_clean_data.csv", index=False)