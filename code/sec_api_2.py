#Thuan Nguyen
#OMSBA5270- Week 3
#This script fetches financial data from the SEC EDGAR database for Alphabet Inc. (CIK: 0001045810)

import requests  # Import requests library for making HTTP requests
import pandas as pd  # Import pandas library for data manipulation and table creation

def get_edgar_data(cik, tag):
    # Construct URL for EDGAR API call using CIK and financial tag
    url = f'https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/{tag}.json'
    headers = {'User-Agent': "tnguyen65@seattleu.edu"}  
    response = requests.get(url, headers=headers)  # Send GET request to EDGAR API
    data = response.json()  # Try to parse JSON response
    units = data['units']['USD']  # Extract USD units from the response
    df = pd.DataFrame(units)  # Convert data to pandas DataFrame
    return df  # Return the DataFrame
    

cik = '0001045810'  # CIK number for NVDA
tags = {
    'Revenue': 'RevenueFromContractWithCustomerExcludingAssessedTax',  # Tag for revenue data
    'Assets': 'Assets',  # Tag for assets data
    'Net Income': 'NetIncomeLoss',  # Tag for net income data
    'Gross Profit': 'GrossProfit',  # Tag for gross profit data (may not be available)
    'Operating Expenses': 'OperatingExpenses'  # Tag for operating expenses data
}

for name, tag in tags.items():  # Iterate over each financial metric and its tag
    df = get_edgar_data(cik, tag)  # Fetch data for the current tag
    if df.empty:
        print(f"Skipping {name} due to API error.")
        continue
    df = df[(df['form'] == '10-K') & (df['fp'] == 'FY')]  # Filter for 10-K annual reports
    df = df.sort_values('fy', ascending=False).iloc[0:3]  # Sort by fiscal year and take last 3 years
    # Print available columns for debugging
    print(f"Available columns for {name}: {df.columns.tolist()}")
    # Select relevant columns, including 'start' if available
    base_columns = ['start', 'end', 'val', 'accn', 'fy', 'fp', 'form', 'filed', 'frame']
    selected_columns = [col for col in base_columns if col in df.columns]
    df = df[selected_columns]
    df = df.reset_index(drop=True)   
    print(f'### {name}')
    print(df.to_markdown())