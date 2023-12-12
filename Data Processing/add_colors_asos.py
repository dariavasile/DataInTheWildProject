
import csv

colors = ['red', 'blue', 'orange', 'green', 'yellow', 'pink', 'purple', 'grey',
          'brown', 'white', 'black', 'navy', 'cream', 'teal', 'tan', 'camel',
          'beige', 'khaki']

with open('./asos_clean_data.csv', 'r', newline='') as file:
    reader = csv.DictReader(file)
    fieldnames = reader.fieldnames

    # Create a list to store the updated rows
    updated_rows = []

    for row in reader:
        name = row['name']
        colours = row['colour']

        for c in colors:
            if c in name:
                row['colour'] = c
                break

        updated_rows.append(row)

# Write the updated data back to the same CSV file
with open('./asos_clean_data.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_rows)





