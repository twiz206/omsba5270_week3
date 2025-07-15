#import modules
import requests
import pandas as pd

#create a request header
header = {'User-Agent': "tnguyen65@seattleu.edu"}


#get all company data
companyTickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers=header)

#print(companyTickers.json()['0']['cik_str'])

companyCIK = pd.DataFrame.from_dict(companyTickers.json(), orient ='index')

print(companyCIK)

companyCIK['cik_str']= companyCIK['cik_str'].astype(str).str.zfill(10)

print(companyCIK)


