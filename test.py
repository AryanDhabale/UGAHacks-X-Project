import requests
import pandas as pd

ALPHA_VANTAGE_API_KEY = "IJ3GJBXDGDD3FQ1X"
ALPHA_VANTAGE_API_URL = "https://www.alphavantage.co/query"

# Fetch balance sheet data for IBM
url = f"{ALPHA_VANTAGE_API_URL}?function=BALANCE_SHEET&symbol=IBM&apikey={ALPHA_VANTAGE_API_KEY}"
r = requests.get(url)
data = r.json()

# Extract annual balance sheets
if "annualReports" in data:
    balance_sheets = data["annualReports"]
    
    # Convert list of dictionaries into DataFrame
    df = pd.DataFrame(balance_sheets)
    
    # Set 'fiscalDateEnding' as the index and transpose so dates become columns
    df.set_index("fiscalDateEnding", inplace=True)
    df = df.T  # Transpose the DataFrame

    # Filter only dates before '2019-11-29'
    df = df.loc[:, df.columns > '2024-02-09']

    print(df)
else:
    print("Error retrieving balance sheet data.")
