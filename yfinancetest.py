import yfinance as yf

# Replace 'AAPL' with the ticker symbol of the company you're interested in
ticker = 'AAPL'

# Get the company data
company = yf.Ticker(ticker)

# Fetch the income statement (usually in a DataFrame)
income_statement = company.financials

# Display the income statement
print(income_statement)
