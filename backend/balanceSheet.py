import streamlit as st
import pandas as pd

def playBalanceSheetGame():
    """
    Launches the Balance Sheet Challenge game where users are presented with a company balance sheet 
    (with a hidden mistake) and a follow-up question. Users must identify the misclassified item.

    Features:
    - Displays a dummy company balance sheet with an intentional error (e.g., a liability misclassified as an asset).
    - Presents a question about the balance sheet.
    - Provides four multiple-choice answer buttons.
    
    Tech Stack:
    ✅ Streamlit – Provides an interactive balance sheet analysis game.
    ✅ MongoDB – (Placeholder) Would store past challenges, user attempts, and progress.
    ✅ Pinata – (Placeholder) Would host financial statement PDFs for reference.
    
    Note: This is a prototype. The buttons currently provide confirmation feedback only.
    """
    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    # App Title and Description
    st.title("⿢ Balance Sheet Challenge: Spot the Errors! 🔍")
    st.write("Employees get randomized company balance sheets with hidden mistakes.")

    
    st.markdown("## Company Balance Sheet")
    
    placeholder = st.empty()
    placeholder.text("Drop an image or PDF here later...")
    
    st.markdown("---")
    
    # Question Section
    st.markdown("## Question")
    question_text = (
        "Identify the misclassified item in the balance sheet above. "
        "Hint: One of the items is incorrectly listed as an Asset when it should be under Liabilities."
    )
    st.write(question_text)
    
    # Multiple-Choice Buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("A: Cash", key="option_a"):
            st.info("Option A selected.")
            
    with col2:
        if st.button("B: Accounts Receivable", key="option_b"):
            st.info("Option B selected.")
            
    with col3:
        if st.button("C: Inventory", key="option_c"):
            st.info("Option C selected.")
            
    with col4:
        if st.button("D: Accounts Payable", key="option_d"):
            st.info("Option D selected.")
    

# For standalone testing, you can uncomment the lines below:
# if __name__ == '__main__':
#     play_balance_sheet_challenge()
