# Data In The Wild Project - Powerpuff Girls
- Ioana-Daria Vasile
- Kristiana Stefa
- Stela Arranz-Gheorghe

# Project Overview
In this project, we embark on a comprehensive data collection initiative from three distinct online shops, each operating in a different region. The primary objective of this project is to gather data systematically from these shops to conduct an in-depth analysis of inclusivity within their offerings.


## Instructions for Data Collection

Follow these step-by-step instructions to set up and run the project:

### 1. RapidAPI Account Setup

1. **Create an Account:**
   - Visit [RapidAPI](https://rapidapi.com/) and sign up for a new account.

2. **Subscribe to Shop APIs:**
   - After creating an account, navigate to each shop's API page on RapidAPI and subscribe to their API.
   
   > **Note:** The free version has limitations (500 requests in 30 days). [Shein](https://rapidapi.com/apidojo/api/unofficial-shein/), [H&M](https://rapidapi.com/apidojo/api/hm-hennes-mauritz), [ASOS](https://rapidapi.com/apidojo/api/asos2)

### 2. Update Script Credentials

#### For Shein Data Retrieval:

1. **Open `retrieve_shein_data.py` script in your preferred code editor.**

2. **Modify Query Parameters:**
   - Locate the `querystring` and `querystring_det` sections.
   - Change the parameters:
      - `country`: Set it to the desired region ('TW' for Taiwan, 'IE' for Ireland, 'US' for the USA).
      - `currency`: Set it to the appropriate currency ('USD' for Taiwan and USA, 'EUR' for Ireland).
      - `gender`: Manually change it to either 'women' or 'men'.
   
   > **Note:** These adjustments are necessary due to the limited number of requests and the need for multiple accounts.

#### For H&M Data Retrieval:

1. **Open `retrieve_hm_data.py`script in your preferred code editor.**

2. **Modify Query Parameters:**
   - Locate the `querystring` and `querystring_det` sections.
   - Change the parameters:
      - `country`: Set it to the desired region ('asia3' for Taiwan, 'ie' for Ireland, for 'us' the USA).
      - `gender`: Manually change it to either 'ladies_' or 'men_'.
      - Locate line 43 and manually change the keyword dictionary to the desired gender (`keywords_ladies` or `keywords_men`).
   
   > **Note:** These adjustments are necessary due to the limited number of requests and the need for multiple accounts.

#### For ASOS Data Retrieval:

1. **Open `asos_get_products.py` script in your code editor.**

2. **Uncomment Desired Category ID List:**
   - Locate the list of `category_id` and uncomment the one based on your desired gender or region.

3. **Modify Query Parameters:**
   - Go to line 49 and find the `querystring` variable.
   - Change the following parameters in the `querystring`:
      - `store`: Set it to the desired store (`US` for USA, `ROE` for Europe, `ROW` for Asia).
      - `country`: Set it to the desired country (`US` for USA, `CN` for China, `HK` for Hong Kong, `NO` for Norway).
      - `currency`: Set it to the desired currency (`EUR` for Norway, `USD` for USA, `HKD` for Hong Kong, `CNY` for China).
      - `language`: Set it to the desired language (en-US for USA ,  en-GB for Norway, Hong Kong, China).

4. **Open `asos_get_details.py` script in your code editor.**

5. **Modify Query Parameters:**
   - Locate line 23 and find the `querystring` variable.
   - Make the same changes as in Step 3 for the `store`, `country`, `currency`, and `language` parameters.

### 3. Run the Script

1. **Execute the Script:**
   - Execute the respective scripts (`retrieve_shien_data.py`, `retrieve_hm_data.py`, `asos_get_products.py`, and `asos_get_details.py`) 
2. **Review Output:**
   - Check the script outputs for the retrieved data.


## Instructions for Data Processing

To process the data obtained from ASOS, Shein, and H&M, follow the steps outlined below. These instructions guide you through running specific scripts in a particular order for data editing, color addition, size conversion, and final data merging.

### ASOS Data Processing:

1. **Run `edit_asos.py`.**

2. **Run `add_colors_asos.py`.**

3. **Run `size_converter_asos.py`.**
 

### Shein Data Processing:

1. **Run `size_converter_shein.py`.**

### H&M Data Processing:

1. **Run `size_converter_hm.py`.**
  

2. **Run `categories_standardization.py`.**
   
### Final Data Merging and Cleaning:

1. **Run `merge_and_clean_data.py`.**
  
2. **Run `remove_duplicates.py`.**

## Instructions for Downloading Product Images
1. **Run `image_downloader.py`.**

## Instructions to Obtain Analysis Plots
1. **Run `analysis.py`.**

  
## Additional Notes

- Ensure that you have the necessary permissions and access to the respective shop APIs.
- Stay within the API rate limits to avoid disruptions.

**Enjoy working with the data from the selected online shops!**
