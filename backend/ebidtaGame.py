import streamlit as st
import pandas as pd

def playEbidtaGame():
    """
    Launches the EBIDTA Challenge game.

    The game displays a company's income statement on the left side and,
    on the right side, text boxes for the user to input:
      - E: Earnings (Net Income)
      - I: Interest Expense
      - T: Taxes
      - D: Depreciation
      - A: Amortization
    Additionally, the user must input the Total EBIDTA (which should equal
    the sum of the five components above).

    When the user clicks "Check EBITDA", the app will compare the sum of the
    entered components with the user‑entered total EBIDTA and provide feedback.
    
    This function encapsulates all functionality and can be imported and
    called from another main file.
    """
    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    st.title("EBIDTA Challenge: Calculate the EBITDA")
    st.write("Review the income statement on the left and enter the corresponding "
             "values in the fields on the right that represent each letter of **EBIDTA**. "
             "Finally, calculate and input the total EBIDTA (which should be the sum of "
             "the five components).")

    # Create two columns: left for the income statement, right for input fields.
    left_col, right_col = st.columns(2)

    # --- Left Column: Display the Income Statement ---
    # Dummy income statement data.
    income_data = {
        "Item": [
            "Revenue",
            "Cost of Goods Sold",
            "Gross Profit",
            "Operating Expenses",
            "Net Income",            # This will serve as the 'E' in EBIDTA.
            "Interest Expense",      # 'I'
            "Taxes",                 # 'T'
            "Depreciation",          # 'D'
            "Amortization"           # 'A'
        ],
        "Amount ($)": [
            1000000,
            600000,
            400000,
            150000,
            200000,   # Net Income (Earnings)
            20000,    # Interest Expense
            30000,    # Taxes
            40000,    # Depreciation
            10000     # Amortization
        ]
    }
    income_df = pd.DataFrame(income_data)

    with left_col:
        st.subheader("Income Statement")
        st.table(income_df)

    # --- Right Column: User Input Fields for EBIDTA Components ---
    with right_col:
        st.subheader("Enter the EBIDTA Components")
        st.write("Please input the following values in dollars:")

        # Input fields for each EBIDTA component.
        input_E = st.text_input("E: Earnings Before Taxes(Net Income)", placeholder="e.g., 200000")
        input_I = st.text_input("I: Interest Expense", placeholder="e.g., 20000")
        input_T = st.text_input("T: Taxes", placeholder="e.g., 30000")
        input_D = st.text_input("D: Depreciation", placeholder="e.g., 40000")
        input_A = st.text_input("A: Amortization", placeholder="e.g., 10000")

        st.markdown("### Total EBIDTA")
        input_total = st.text_input("Enter Total EBIDTA", placeholder="e.g., 300000")

    st.markdown("---")

    # --- Check the User's Input ---
    if st.button("Check EBITDA"):
        try:
            # Convert inputs to floats.
            E_val = float(input_E)
            I_val = float(input_I)
            T_val = float(input_T)
            D_val = float(input_D)
            A_val = float(input_A)
            total_input = float(input_total)

            # Calculate the sum of the individual components.
            calculated_total = E_val + I_val + T_val + D_val + A_val

            # Compare the calculated total with the user-entered total.
            if abs(calculated_total - total_input) < 1e-2:
                st.success(f"Correct! The total EBIDTA is ${calculated_total:,.2f}.")
            else:
                st.error(f"Incorrect. The sum of your components is ${calculated_total:,.2f}, "
                         f"which does not match your total EBIDTA input of ${total_input:,.2f}.")
        except ValueError:
            st.error("Please ensure that all fields are filled in with valid numeric values.")

# For standalone testing, you can uncomment the following lines:
# if __name__ == '__main__':
#     play_ebidta_challenge()
