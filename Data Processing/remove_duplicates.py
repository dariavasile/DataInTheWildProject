import pandas as pd 

file ='./all_data_clean.csv'
df = pd.read_csv(file)

columns_to_check_duplicates = ["product_id", "region", "shop"]
df_no_duplicates = df.drop_duplicates(subset=columns_to_check_duplicates, keep="first")

print("removed: ", len(df) - len(df_no_duplicates))

df_no_duplicates.to_csv('./all_data_clean.csv', index=False)