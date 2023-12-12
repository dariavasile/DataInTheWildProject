import requests
import csv 

url = "https://asos2.p.rapidapi.com/products/v3/detail"

headers = {
    "X-RapidAPI-Key": "b7052635camsh4df1f14bbee8739p191246jsnd4ec4909beea",
	"X-RapidAPI-Host": "asos2.p.rapidapi.com"
} 

existing_product_data = []

with open("./asos_raw_data.csv", "r") as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        existing_product_data.append(row)


product_ids = [row["id"] for row in existing_product_data]
product_details_dict = {}

for product_id in product_ids:
    querystring = {"id": str(product_id), "lang": "en-US", "store": "USA", "sizeSchema": "US", "currency": "USD"}

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        product_details = response.json()
        product_details_dict[str(product_id)] = product_details
        
# Update existing product data with new fields
for product_data in existing_product_data:
    product_id = product_data["id"]
    product_details = product_details_dict.get(product_id, {})

    product_data["description"] = product_details.get("description", "")
    product_data["gender"] = product_details.get("gender", "")
    product_data["sizeGuide"] = product_details.get("brand", {}).get("sizeGuide", "")
    product_data["aboutMe"] = product_details.get("info", {}).get("aboutMe", "")
    product_data["sizeAndFit"] = product_details.get("info", {}).get("sizeAndFit", "")
    product_data["currency"] = product_details.get("price", {}).get("currency", "")
    product_data["sizes"] = ", ".join([variant.get("brandSize", "") for variant in product_details.get("variants", [])])
    
    
output_file = "./asos_raw_data.csv" 
fields = ["id", "name", "price", "colour", "brandName", "url", "imageUrl","description",
           "gender", "sizeGuide", "aboutMe", "sizeAndFit", "currency", "sizes"]

with open(output_file, "w", newline="") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fields)
    
    writer.writeheader()
    writer.writerows(existing_product_data)