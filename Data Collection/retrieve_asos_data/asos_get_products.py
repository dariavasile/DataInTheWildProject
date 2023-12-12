import requests
import csv

url = "https://asos2.p.rapidapi.com/products/v2/list"

# Brand IDs for men per region

# USA
category_ids = ["19953", "19971", "11039", "25595", "11674", "27633", "2038", "50577",
                "2592", "29352", "7071", "29408", "4562", "50997", "27628", "18764",
                "8982", "4280", "3246", "5247", "5715", "50580"
               ]  

# Asia
category_ids = ['19953', '19971', '11039', '11674', '14029', '27634', '8473', '14797', '28549',
                '8475', '29353', '10949', '29409', '8499', '10852', '51006', '27629', '11067',
                '19365', '16692', '50277', '17933', '50582', '9512', '26877'

] 

# Europe
category_ids = ['19953', '19971', '11039', '25595', '7551', '11674', '14029', '27633', '2038',
                '6579', '7071', '29408', '4562', '5884', '50997', '27628', '8982', '4280', '3246',
                '5715', '5247', '50580', '10125', '26876'
]

# Brand IDs for women (do not differ by region)
category_ids = ['7552', '19314', '2505', '6142', '11048', '50660', '27909','8439',
                '20848', '3336', '21378', '21571', '19899', '12949', '26768', '30058',
                '17371', '5651', '12812'
               ]

headers = {
	"X-RapidAPI-Key": "b7052635camsh4df1f14bbee8739p191246jsnd4ec4909beea",
	"X-RapidAPI-Host": "asos2.p.rapidapi.com"
}   

all_products = []

# Add product types to exclude
exclude_product_types = ['sneakers', 'bag', 'bags', 'boots', 'cap', 'card case', 'runners']  

# Dictionary of items to retrieve
keywords = ['t-shirt', 'shirt', 'top', 'knitwear', 'sweater', 'hoodie', 'jeans', 'pants', 
            'trousers', 'cardigan', 'sweatshirt', 'sweatpants', 'coat', 'jumper', 'jacket', 'shorts'
            'dress', 'skirt'] 

for category_id in category_ids:
    querystring = {
    "store": "US",
    "offset": "0",
    "categoryId": str(category_id),
    "limit": "400",
    "country": "US",
    "sort": "freshness",
    "currency": "USD",
    "sizeSchema": "US",
    "lang": "en-US"
    }

    response = requests.get(url, headers=headers, params=querystring)


    if response.status_code == 200:
       data = response.json()
       products = data.get("products", [])

       # Add only clothing items     
       filtered_products = [
           product for product in products
            if all(type not in product.get("name").lower() for type in exclude_product_types) and
               any(keyword in product.get("name").lower() for keyword in keywords)
        ]
       all_products.extend(filtered_products)

    else:
        print("id failed: ", category_id)
    

csv_filename = "./asos_raw_data.csv" 
fieldnames = ["id", "name", "price", "colour", "brandName", "url", "imageUrl"]

# Write the data to a CSV file
with open(csv_filename, "w", newline="") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
        
    for product in all_products:
        product_data = {
            "id": product.get("id"),
            "name": product.get("name"),
            "price": product.get("price").get("current").get("value"),
            "colour": product.get("colour"),
            "brandName": product.get("brandName"),
            "url": product.get("url"),
            "imageUrl": product.get("imageUrl"),
        }
        writer.writerow(product_data)
