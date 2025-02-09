import streamlit as st
import pandas as pd

def playHorizontalAnalysisGame():
    """
    Launches the Horizontal Analysis Battle game for a single company.
    
    The game displays the company's financial performance over 4 quarters for two different years:
      - Left Column: Earlier Year (e.g., 2023)
      - Right Column: Later Year (e.g., 2024)
    
    Users can select which metric to visualize (Profit, Growth, Revenue, EBITDA) for each year.
    After reviewing the charts, a question is presented with multiple choice answers.
    
    Tech Stack:
    ✅ Streamlit – Trend visualizations & interactive charts.
    ✅ MongoDB – (Placeholder) Would store past financial data for comparisons.
    ✅ Pinata – (Placeholder) Would hold archived financial reports.
    
    Note: The multiple-choice buttons currently provide confirmation feedback only.
    """
    # App Title and Description
    st.title("Horizontal Analysis Battle: Predict the Trend 📊🔮")
    st.write("Employees analyze financial metrics over time to spot trends & anomalies.")
    st.write("**Challenge Mode:** Predict next-quarter revenue & profitability based on trends.")
    st.write("**Gamification:** Correct predictions earn badges; top performers unlock VIP access to advanced reports.")
    
    # Dummy data for a single company across two years
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    
    # Data for the earlier year (e.g., 2023)
    data_year1 = {
        "Profit": [100, 120, 110, 130],
        "Growth": [5, 6, 4, 7],
        "Revenue": [1000, 1100, 1050, 1150],
        "EBITDA": [200, 220, 210, 230]
    }
    
    # Data for the later year (e.g., 2024) with updated/different numbers
    data_year2 = {
        "Profit": [130, 140, 135, 150],
        "Growth": [6, 7, 5, 8],
        "Revenue": [1200, 1250, 1230, 1300],
        "EBITDA": [250, 260, 255, 270]
    }
    
    # Layout: Two columns side by side
    col1, col2 = st.columns(2)
    
    # Options for metrics to display
    metric_options = ["Profit", "Growth", "Revenue", "EBITDA"]
    
    # --- Left Column: Earlier Year Data ---
    with col1:
        st.subheader("Year: 2023")
        selected_metric_year1 = st.selectbox("Select Metric", options=metric_options, key="year1_metric")
        st.write(f"Displaying quarterly **{selected_metric_year1}** data for 2023:")
        df_year1 = pd.DataFrame({selected_metric_year1: data_year1[selected_metric_year1]}, index=quarters)
        st.line_chart(df_year1)
    
    # --- Right Column: Later Year Data ---
    with col2:
        st.subheader("Year: 2024")
        selected_metric_year2 = st.selectbox("Select Metric", options=metric_options, key="year2_metric")
        st.write(f"Displaying quarterly **{selected_metric_year2}** data for 2024:")
        df_year2 = pd.DataFrame({selected_metric_year2: data_year2[selected_metric_year2]}, index=quarters)
        st.line_chart(df_year2)
    
    st.markdown("---")
    
    # --- Question and Multiple-Choice Section ---
    st.markdown("## Question")
    question_text = (
        "Based on the horizontal analysis of the company's performance over these two years, "
        "which metric do you believe is the best indicator of its future performance?"
    )
    st.write(question_text)
    
    # Create four columns for the multiple-choice options
    option_cols = st.columns(4)
    
    with option_cols[0]:
        if st.button("A: Profit", key="option_profit"):
            st.info("Option A (Profit) selected.")
    
    with option_cols[1]:
        if st.button("B: Growth", key="option_growth"):
            st.info("Option B (Growth) selected.")
    
    with option_cols[2]:
        if st.button("C: Revenue", key="option_revenue"):
            st.info("Option C (Revenue) selected.")
    
    with option_cols[3]:
        if st.button("D: EBITDA", key="option_ebitda"):
            st.info("Option D (EBITDA) selected.")

    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()
# For standalone testing, you can uncomment the following lines:
# if __name__ == '__main__':
#     play_horizontal_analysis_battle()
