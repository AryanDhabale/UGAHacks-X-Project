import random
import pandas as pd
import streamlit as st

def generate_income_statement():
    """
    Generates a random income statement with logically consistent values.
    """
    # Generate Net Sales (in thousands)
    net_sales = random.randint(100000, 500000)

    # Generate Cost of Sales (in thousands, should be less than Net Sales)
    cost_of_sales = random.randint(int(net_sales * 0.4), int(net_sales * 0.8))

    # Gross Profit (Net Sales - Cost of Sales)
    gross_profit = net_sales - cost_of_sales

    # Selling and Operating Expenses (in thousands, reasonable percentage of Net Sales)
    selling_operating_expenses = random.randint(int(net_sales * 0.1), int(net_sales * 0.2))

    # General and Administrative Expenses (in thousands, less than Selling and Operating Expenses)
    g_and_a_expenses = random.randint(int(selling_operating_expenses * 0.5), int(selling_operating_expenses * 0.8))

    # Total Operating Expenses (Selling and Operating Expenses + G&A Expenses)
    total_operating_expenses = selling_operating_expenses + g_and_a_expenses

    # Operating Income (Gross Profit - Total Operating Expenses)
    operating_income = gross_profit - total_operating_expenses

    # Other Income (small relative to Operating Income)
    other_income = random.randint(-5000, 5000)

    # Gain (Loss) on Financial Instruments (can be negative)
    gain_loss_instruments = random.randint(-10000, 10000)

    # (Loss) Gain on Foreign Currency (can be negative)
    gain_loss_foreign_currency = random.randint(-5000, 5000)

    # Interest Expense (should not exceed Operating Income)
    interest_expense = random.randint(0, int(operating_income * 0.2))

    # Income Before Taxes (Operating Income + Other Income + Gain/Loss on Financial Instruments + Gain/Loss on Foreign Currency)
    income_before_taxes = operating_income + other_income + gain_loss_instruments + gain_loss_foreign_currency

    # Income Tax Expense (25% of Income Before Taxes)
    income_tax_expense = int(income_before_taxes * 0.25) if income_before_taxes > 0 else 0

    # Net Income (Income Before Taxes - Income Tax Expense)
    net_income = income_before_taxes - income_tax_expense

    # Depreciation (less than or equal to Operating Income)
    depreciation = random.randint(0, int(operating_income * 0.2))

    # Amortization (small value compared to Depreciation)
    amortization = random.randint(0, int(depreciation * 0.5))

    # Prepare the generated data into a dictionary
    data = {
        'Net Sales': net_sales,
        'Cost of Sales': cost_of_sales,
        'Gross Profit': gross_profit,
        'Selling and Operating Expenses': selling_operating_expenses,
        'General and Administrative Expenses': g_and_a_expenses,
        'Total Operating Expenses': total_operating_expenses,
        'Operating Income': operating_income,
        'Other Income': other_income,
        'Gain (Loss) on Financial Instruments': gain_loss_instruments,
        'Gain (Loss) on Foreign Currency': gain_loss_foreign_currency,
        'Interest Expense': interest_expense,
        'Income Before Taxes': income_before_taxes,
        'Income Tax Expense': income_tax_expense,
        'Net Income': net_income,
        'Depreciation': depreciation,
        'Amortization': amortization
    }

    # Convert to a pandas DataFrame for better display
    df = pd.DataFrame(list(data.items()), columns=['Metric', 'Value'])
    df['Value'] = df['Value'].apply(lambda x: f"${x:,.0f}K")  # Format the values to be in thousands
    
    return df, data  # Return both the DataFrame for display and the raw data for calculations

def playEbidtaGame():
    """
    Launches the EBITDA Challenge game with random income statement data.
    """
    st.title("EBITDA Challenge: Calculate the EBITDA")
    st.write("Review the income statement on the left and enter the corresponding "
             "values in the fields on the right that represent each letter of **EBITDA**. "
             "Finally, calculate and input the total EBITDA (which should be the sum of "
             "the five components). Please enter all values in thousands.")
    
    # Generate a random income statement
    df, actual_values = generate_income_statement()

    # Create two columns: left for the income statement, right for input fields.
    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("Income Statement")
        st.dataframe(df)  # Displaying the income statement

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
    all_correct = True  # Keep track of whether all inputs are correct

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

            # Check if each input field is correct
            feedback = []
            if abs(E_val - actual_values['Net Income']) < 1e-2:
                feedback.append("Earnings Before Taxes (Net Income): Correct!")
            else:
                feedback.append("Earnings Before Taxes (Net Income): Incorrect! Blank or wrong value.")

            if abs(I_val - actual_values['Interest Expense']) < 1e-2:
                feedback.append("Interest Expense: Correct!")
            else:
                feedback.append("Interest Expense: Incorrect! Blank or wrong value.")
                all_correct = False

            if abs(T_val - actual_values['Income Tax Expense']) < 1e-2:
                feedback.append("Taxes (Income Tax Expense): Correct!")
            else:
                feedback.append("Taxes (Income Tax Expense): Incorrect! Blank or wrong value.")
                all_correct = False

            if abs(D_val - actual_values['Depreciation']) < 1e-2:
                feedback.append("Depreciation: Correct!")
            else:
                feedback.append("Depreciation: Incorrect! Blank or wrong value.")
                all_correct = False

            if abs(A_val - actual_values['Amortization']) < 1e-2:
                feedback.append("Amortization: Correct!")
            else:
                feedback.append("Amortization: Incorrect! Blank or wrong value.")
                all_correct = False

            # Check if the total EBITDA matches
            if abs(calculated_total - total_input) < 1e-2:
                feedback.append(f"Total EBITDA: Correct! The sum of components is ${calculated_total:,.0f}K.")
            else:
                feedback.append(f"Total EBITDA: Incorrect! Your total input of ${total_input:,.0f}K doesn't match.")
                all_correct = False

            # Show feedback to the user
            for line in feedback:
                st.write(line)

            if all_correct:
                st.success("Congratulations! You've got all the components right!")
            else:
                st.warning("Please correct the errors before submitting again.")
                
        except ValueError:
            st.error("Please ensure that all fields are filled in with valid numeric values.")
