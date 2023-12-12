import pandas as pd
import urllib.request

def download_and_save_images(csv_file_path, output_folder):
    # Read the CSV file into a pandas DataFrame with explicit encoding
    df = pd.read_csv(csv_file_path)
    unique_product_id = set()
        
    for _, row in df.iterrows():
        try:
            id = row['product_id']  # column name for the image id
            # Check if the product from csv file has already been downloaded
            if id in unique_product_id:
                continue
            # Form the image name
            image_name = f"{id}.jpg"

            # Combine the output folder path and image name to get the full path
            output_path = f"{output_folder}/{image_name}"

            # Check if the product already exists in the folder
            #if os.path.exists(output_path):
                    #continue

            # Check if the URL is complete, and if not, append the base URL
            if 'http' not in row['img_url']:
                image_url = 'https://'+ row['img_url']
            else:
                image_url = row['img_url']  #  column name containing image URLs

            # Download and save the image
            urllib.request.urlretrieve(image_url, output_path)
                
            unique_product_id.add(image_url)

        except Exception as e:
            print(f"Error processing product: {row['product_id']}. Error: {e}")

# Example usage:
csv_file_path = './all_data_clean.csv'
output_folder = 'images'
download_and_save_images(csv_file_path, output_folder)
print(f"Images downloaded successfully!")