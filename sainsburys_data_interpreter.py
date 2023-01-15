from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
import requests
import validators

SCRAPE_DELAY = 5

def get_refs_and_urls_from_excel(inputData, ref_column, url_columns):
    # The columns var should only contain the reference column, and the columns containing urls
    df = pd.read_excel(inputData, usecols=f"{ref_column},{url_columns}")
    data = []
    for index, row in df.iterrows():
        rowDict = {}
        rowDict['ref'] = row[0]
        urls = []
        # For each url column
        for col in range(1, len(row)):
            if is_url(row[col]):
                urls.append(row[col])
        rowDict['urls'] = urls
        data.append(rowDict)
    return data

def is_url(inputString):
    inputString = str(inputString)
    if not isinstance(inputString, str) or inputString == 'nan': # 'nan' is a value that pandas puts into a dataframe when a cell is empty
        return False
    return validators.url(inputString)

def get_balance_from_url(url):
    # return 4.30 # For testing purposes
    flag = False
    while True:
        try:
            sleep(SCRAPE_DELAY) # Reduces the chance of 'Too many requests' being received
            # Get the contents of webpage
            result = requests.get(url)
            doc = BeautifulSoup(result.text, "html.parser")
            raise NotImplementedError
            account_div = doc.find("div", id="accountnumber_pin")
            account_div_content = account_div.contents
            print(".")
            break
        except:
            print(f"Too many requests. Waiting {30*flag} seconds to retry.")
            # If for this url, we receive 'Too many requests' error, sleep for 20
            sleep(20 + 15*flag)
            flag = True # Increases sleep time to 35 seconds
            print("Retrying. Please wait...")
    
    return balance
        
def save_data_to_excel(data, outputFile="result.xlsx"):
    # Data should be in the form: [{ref: 'xx', balances: ['xx', ...]}, ...]
    for row in data:
        row['balances'] = ', '.join(row['balances'])
    df = pd.DataFrame(data)
    print(df)
    df.to_excel(outputFile, index=False)