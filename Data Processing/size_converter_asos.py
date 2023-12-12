import pandas as pd

# Sample data with a "sizes" column
data = pd.read_csv("./asos_clean_data.csv")
df = pd.DataFrame(data)

#size converter
def size_converter(sizes):
    size_list = sizes.split('/')
    conversion = ''
    size_list = [s.strip() for s in size_list]
    #benchmark = ['XXS','XS', 'S', 'M', 'L', 'XL', 'XXL','2XL','3XL','4XL','5XL', '6XL']
    
    for size in size_list:
        if size=='0' or size=='32':
            conversion += 'XXS/'
        elif size=='2' or size=='34':
            conversion += 'XS/'
        elif (size=='4' or size=='6') or (size=='36' or size=='34'):
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
    return conversion

# Define a function to extract minimum and maximum sizes
def extract_min_max_sizes(sizes):
    size_list = sizes.split('/')
    size_list = [s.strip() for s in size_list]
    sizes_order = ['XXS','XS', 'S', 'M', 'L', 'XL', 'XXL','2XL','3XL','4XL','5XL', '6XL']
    min_size = max_size = None

    for size in size_list:
        if size in sizes_order:
            if min_size is None or sizes_order.index(size) < sizes_order.index(min_size):
                min_size = size
            if max_size is None or sizes_order.index(size) > sizes_order.index(max_size):
                max_size = size

    return min_size, max_size

df['sizes'] = df['sizes'].apply(size_converter).apply(pd.Series)
# Apply the function to create new columns
df[['min_size', 'max_size']] = df['sizes'].apply(extract_min_max_sizes).apply(pd.Series)

df.to_csv("./asos_clean_data.csv")

print(df)
