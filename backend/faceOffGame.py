import streamlit as st
import pandas as pd

def playfaceOffGame():
    """
    Launches the Horizontal Analysis Battle game where working professionals can compare
    financial metrics of two companies side by side.
    
    Features:
    - Two columns: one for each company.
    - Each column shows a simple financial statement, a dropdown to select a metric ("Profit" or "Growth"),
      and a line chart plotting quarterly data (Q1-Q4) for the chosen metric.
    - A bottom section displays a question prompt and four multiple choice buttons.
    
    Note: This is a dummy prototype. The buttons do not process answers yet.
    """
    # Game header and description
    st.title("Horizontal Analysis Battle: Predict the Trend 📊🔮")
    st.write("Employees analyze financial metrics over time to spot trends & anomalies.")
    st.write("**Challenge Mode:** Predict next-quarter revenue & profitability based on trends.")
    st.write("**Gamification:** Correct predictions earn badges; top performers unlock VIP access to advanced reports.")

    # Dummy data for two companies
    companies = {
        "Company A": {
            "Financials": {
                "Revenue": "$1M",
                "Net Income": "$100K",
                "Profit": "$150K",
                "Growth": "5%"
            },
            "Quarterly": {
                # Quarterly numbers (e.g., in thousands for profit, percentages for growth)
                "Profit": [100, 120, 130, 140],
                "Growth": [5, 7, 6, 8]
            }
        },
        "Company B": {
            "Financials": {
                "Revenue": "$1.2M",
                "Net Income": "$110K",
                "Profit": "$160K",
                "Growth": "6%"
            },
            "Quarterly": {
                "Profit": [90, 115, 125, 135],
                "Growth": [4, 6, 7, 9]
            }
        }
    }

    st.markdown("## Compare the Companies Side by Side")
    # Create two columns for the companies
    col1, col2 = st.columns(2)
    
    # Labels for the four quarters
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    
    # --- Company A Column ---
    with col1:
        st.subheader("Company A")
        st.write("**Financial Statement:**")
        # Display key financial metrics
        for key, value in companies["Company A"]["Financials"].items():
            st.write(f"**{key}:** {value}")
            
        # Dropdown to select which metric's quarterly data to view
        metric_a = st.selectbox("Select Metric", options=["Profit", "Growth"], key="metric_a")
        st.write(f"Displaying quarterly **{metric_a}** data:")
        
        # Prepare and display a line chart for the selected metric
        data_a = companies["Company A"]["Quarterly"][metric_a]
        df_a = pd.DataFrame({metric_a: data_a}, index=quarters)
        st.line_chart(df_a)
    
    # --- Company B Column ---
    with col2:
        st.subheader("Company B")
        st.write("**Financial Statement:**")
        for key, value in companies["Company B"]["Financials"].items():
            st.write(f"**{key}:** {value}")
            
        metric_b = st.selectbox("Select Metric", options=["Profit", "Growth"], key="metric_b")
        st.write(f"Displaying quarterly **{metric_b}** data:")
        
        data_b = companies["Company B"]["Quarterly"][metric_b]
        df_b = pd.DataFrame({metric_b: data_b}, index=quarters)
        st.line_chart(df_b)
    
    st.markdown("---")  # Separator
    
    # --- Bottom Question and Multiple Choice Section ---
    st.markdown("## Question")
    # This is where you can add your custom question text later
    question_text = "Based on the trends shown above, which company is expected to have a higher next-quarter profit?"
    st.write(question_text)
    
    # Create four columns for multiple choice options (A-D)
    option_cols = st.columns(4)
    # Option A
    with option_cols[0]:
        if st.button("A: Company A", key="option_a"):
            st.info("Option A selected.")
    # Option B
    with option_cols[1]:
        if st.button("B: Company B", key="option_b"):
            st.info("Option B selected.")
    # Option C
    with option_cols[2]:
        if st.button("C: Both will grow similarly", key="option_c"):
            st.info("Option C selected.")
    # Option D
    with option_cols[3]:
        if st.button("D: None of the above", key="option_d"):
            st.info("Option D selected.")
