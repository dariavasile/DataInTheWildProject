import pandas as pd
import re
from bs4 import BeautifulSoup

# Read the CSV file into a DataFrame
df = pd.read_csv('./asos_raw_data.csv')

# Function to extract fabric and composition from the given column
def extract_fabric_and_composition(text):
    if pd.notna(text):
        # Remove HTML tags
        text = re.sub(r'<.*?>', '', text)
        
        fabric = re.search(r'([a-zA-Z\s-]+):\s', text)
        composition = re.findall(r'(\d+%?\s?[a-zA-Z-]+)', text)
        return fabric.group(1) if fabric else None, ', '.join(composition) if composition else None
    else:
        return None, None


def extract_product_and_fit(description):
    if pd.notna(description):
        # Remove HTML tags
        description_text = re.sub(r'<.*?>', '', str(description))
        
        # Extract product from the strong tag
        soup = BeautifulSoup(description, 'html.parser')
        strong_tag = soup.find('strong')
        product = strong_tag.text if strong_tag else None
        
        # Extract fit from the tag containing the keyword "fit"
        fit_tag = soup.find(lambda tag: tag.name == 'li' and 'fit' in tag.text.lower())
        fit = fit_tag.text if fit_tag else None

        print(f"Original: {description_text}")
        print(f"Product: {product}")
        print(f"Fit: {fit}")
        print("=" * 50)
        
        return product, fit
    else:
        return None, None

# extract fabric and composition
df['fabric'], df['composition'] = zip(*df['aboutMe'].apply(extract_fabric_and_composition))
df = df.drop(columns=['aboutMe'])

df['product'], df['fit'] = zip(*df['description'].apply(extract_product_and_fit))
df = df.drop(columns=['description'])

def extract_min_max_sizes(sizes):
    sizes_str = str(sizes)
    size_list = [size.strip() for size in sizes_str.split(',')] 


    sizes_order = ['XXS','XS', 'S', 'M', 'L', 'XL', '2XL','3XL','4XL','5XL', '6XL', '7XL']
    min_size = max_size = None

    for size in size_list:
        if size in sizes_order:
            if min_size is None or sizes_order.index(size) < sizes_order.index(min_size):
                min_size = size
            if max_size is None or sizes_order.index(size) > sizes_order.index(max_size):
                max_size = size

    return min_size, max_size


df[['min_size', 'max_size']] = df['universal_sizes'].apply(extract_min_max_sizes).apply(pd.Series)


df.to_csv('./asos_clean_data.csv', index=False)
