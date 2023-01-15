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

def get_voucher_details_from_url(url):
    #return {'voucherNumber': '123456789', 'pin': '1234'} # For testing purposes
    flag = False
    while True:
        try:
            sleep(SCRAPE_DELAY) # Reduces the chance of 'Too many requests' being received
            # Get the contents of webpage
            result = requests.get(url)
            doc = BeautifulSoup(result.text, "html.parser")
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
    
    voucher_details = {}
    for child in account_div_content:
        extracted_number = extract_numbers(child)
        if extracted_number != None:
            if not 'voucherNumber' in voucher_details.keys():
                voucher_details['voucherNumber'] = extracted_number
            else: 
                voucher_details['pin'] = extracted_number
    return voucher_details

def extract_numbers(string):
    string = str(string).strip()
    for i in range(len(string)):
        if string[i].isdigit():
            number = str(string[i:]).replace(' ', '')
            return str(number)
        
def save_data_to_excel(data, outputFile="result.xlsx"):
    # Data should be in the form: [{ref: 'xx', vouchers: ['xx', ...]}, {...}]
    for row in data:
        # Sometimes one reference can have multiple vouchers so each voucher need to be in a new column
        voucher_col = 1
        for voucher in row['vouchers']:
            heading_name = f"Voucher{voucher_col}"
            row[heading_name] = f"{voucher['voucherNumber']} : {voucher['pin']}"
            voucher_col += 1
        row.pop('vouchers', None) # We no longer need the list of vouchers as each voucher now has it's own column
    df = pd.DataFrame(data)
    print(df)
    df.to_excel(outputFile, index=False)