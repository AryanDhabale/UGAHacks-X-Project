import yfinance as yf
import streamlit as st
import pandas as pd
import random

# List of popular stock tickers
popular_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NFLX', 'NVDA', 'SPY', 'GOOG', 'BABA', 'AMZN', 'INTC', 'TSM', 'DIS']

def get_dynamic_data(ticker):
    """
    Fetches financial data for the given ticker from yfinance and returns the top metrics for Q1.
    It will also store the EBITDA value, but it will not be displayed in the table.
    If data is missing, it will not be included in the table.
    """
    # Fetch company data using yfinance
    company = yf.Ticker(ticker)

    # Fetching the financials (Income Statement)
    income_statement = company.financials

    # Initialize an empty dictionary to store the data
    data_dict = {}
    
    # Attempt to get required metrics and handle missing data
    try:
        ebitda = income_statement.loc['EBITDA'].iloc[0] / 1000  # Convert to thousands
        data_dict['EBITDA'] = ebitda
    except KeyError:
        pass
    
    try:
        net_income = income_statement.loc['Net Income'].iloc[0] / 1000  # Convert to thousands
        data_dict['Net Income'] = net_income
    except KeyError:
        pass
    
    try:
        depreciation = income_statement.loc['Depreciation'].iloc[0] / 1000  # Convert to thousands
        data_dict['Depreciation'] = depreciation
    except KeyError:
        pass
    
    try:
        interest_expense = income_statement.loc['Interest Expense'].iloc[0] / 1000  # Convert to thousands
        data_dict['Interest Expense'] = interest_expense
    except KeyError:
        pass
    
    try:
        taxes = income_statement.loc['Income Tax Expense'].iloc[0] / 1000  # Convert to thousands
        data_dict['Taxes'] = taxes
    except KeyError:
        pass

    try:
        operating_income = income_statement.loc['Operating Income'].iloc[0] / 1000  # Convert to thousands
        data_dict['Operating Income'] = operating_income
    except KeyError:
        pass

    try:
        gross_profit = income_statement.loc['Gross Profit'].iloc[0] / 1000  # Convert to thousands
        data_dict['Gross Profit'] = gross_profit
    except KeyError:
        pass

    try:
        total_revenue = income_statement.loc['Total Revenue'].iloc[0] / 1000  # Convert to thousands
        data_dict['Total Revenue'] = total_revenue
    except KeyError:
        pass

    try:
        ebit = income_statement.loc['EBIT'].iloc[0] / 1000  # Convert to thousands
        data_dict['EBIT'] = ebit
    except KeyError:
        pass

    try:
        operating_expenses = income_statement.loc['Operating Expenses'].iloc[0] / 1000  # Convert to thousands
        data_dict['Operating Expenses'] = operating_expenses
    except KeyError:
        pass

    try:
        interest_income = income_statement.loc['Interest Income'].iloc[0] / 1000  # Convert to thousands
        data_dict['Interest Income'] = interest_income
    except KeyError:
        pass

    # Create DataFrame for Q1 metrics
    data = {
        'Metric': [
            'Earnings Before Interest and Taxes (EBIT)', 'Net Income', 'Depreciation',
            'Interest Expense', 'Taxes', 'Operating Income', 'Gross Profit', 
            'Total Revenue', 'EBIT', 'Operating Expenses', 'Interest Income'
        ],
        'Q1': [
            data_dict.get('EBITDA', 'N/A'), 
            data_dict.get('Net Income', 'N/A'),
            data_dict.get('Depreciation', 'N/A'),
            data_dict.get('Interest Expense', 'N/A'),
            data_dict.get('Taxes', 'N/A'),
            data_dict.get('Operating Income', 'N/A'),
            data_dict.get('Gross Profit', 'N/A'),
            data_dict.get('Total Revenue', 'N/A'),
            data_dict.get('EBIT', 'N/A'),
            data_dict.get('Operating Expenses', 'N/A'),
            data_dict.get('Interest Income', 'N/A')
        ]
    }
    
    # Create DataFrame from the data
    df = pd.DataFrame(data)
    
    return df, data_dict  # Return both the table and the data for user input comparison

def playEbidtaGame():
    """
    Launches the EBITDA Challenge game.
    """
    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    st.title("EBITDA Challenge: Calculate the EBITDA")
    st.write("Review the income statement on the left and enter the corresponding "
             "values in the fields on the right that represent each letter of **EBITDA**. "
             "Finally, calculate and input the total EBITDA (which should be the sum of "
             "the five components). Please enter all values in thousands.")

    # Randomly select a stock ticker from the list
    ticker = random.choice(popular_stocks)

    # Get dynamic data based on the ticker
    data, actual_values = get_dynamic_data(ticker)

    # Create two columns: left for the income statement, right for input fields.
    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader(f"Income Statement for {ticker}")
        st.dataframe(data)  # Displaying the income statement without EBITDA

    # --- Right Column: User Input Fields for EBITDA Components ---
    with right_col:
        st.subheader("Enter the EBITDA Components")
        st.write("Please input the following values in thousands:")

        # Input fields for each EBITDA component.
        input_E = st.text_input("E: Earnings Before Taxes (Net Income)", placeholder="e.g., 200")
        input_I = st.text_input("I: Interest Expense", placeholder="e.g., 20")
        input_T = st.text_input("T: Taxes", placeholder="e.g., 30")
        input_D = st.text_input("D: Depreciation", placeholder="e.g., 40")
        input_A = st.text_input("A: Amortization", placeholder="e.g., 10")

        st.markdown("### Total EBITDA")
        input_total = st.text_input("Enter Total EBITDA", placeholder="e.g., 300")

    st.markdown("---")

    # --- Check the User's Input ---
    if st.button("Check EBITDA"):
        try:
            # Convert inputs to floats.
            E_val = float(input_E) if input_E else 0.0
            I_val = float(input_I) if input_I else 0.0
            T_val = float(input_T) if input_T else 0.0
            D_val = float(input_D) if input_D else 0.0
            A_val = float(input_A) if input_A else 0.0
            total_input = float(input_total) if input_total else 0.0

            # Calculate the sum of the individual components.
            calculated_total = E_val + I_val + T_val + D_val + A_val

            # Compare the calculated total with the user-entered total.
            if abs(calculated_total - total_input) < 1e-2:
                st.success(f"Correct! The total EBITDA is ${calculated_total:,.0f}K.")
            else:
                st.error(f"Incorrect. The sum of your components is ${calculated_total:,.0f}K, "
                         f"which does not match your total EBITDA input of ${total_input:,.0f}K.")
            
            # Now compare user input to actual values
            st.subheader(f"Comparing Your Input to Actual Values:")

            # For each metric, compare the user input with the actual value
            feedback = []
            for metric, actual in actual_values.items():
                user_input = locals().get(f"input_{metric[0]}", 0)
                if user_input:
                    if abs(user_input - actual) < 1e-2:
                        feedback.append(f"{metric}: Correct! Your input matches the actual value of ${actual:,.0f}K.")
                    else:
                        feedback.append(f"{metric}: Incorrect. Your input of ${user_input:,.0f}K does not match the actual value of ${actual:,.0f}K.")
                else:
                    feedback.append(f"{metric}: You did not provide an input for this metric.")
            
            # Display the feedback for each metric
            for line in feedback:
                st.write(line)

        except ValueError:
            st.error("Please ensure that all fields are filled in with valid numeric values.")
