import streamlit as st
import requests
from datetime import datetime

# Simulated user data for login
simulated_user_data = {
    "username": "Vedaant", 
    "level": 1,
    "challenges_completed": 5
}

# Gemini API setup (for example)
GEMINI_API_URL = "https://api.gemini.com/v1/pubticker/BTCUSD"  # Example API endpoint for Gemini

# AlphaVantage API setup (for financial data)
ALPHA_VANTAGE_API_KEY = "YOUR_ALPHAVANTAGE_API_KEY"
ALPHA_VANTAGE_API_URL = "https://www.alphavantage.co/query"

def display_financial_data():
    """Displays the Gemini and AlphaVantage financial data"""
    st.write("Fetching Financial Data...")  # Debugging

    # Get BTC price from Gemini
    try:
        response = requests.get(GEMINI_API_URL)
        gemini_data = response.json()
        st.write(f"**BTC Price (Gemini):** {gemini_data['last']} USD")
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching Gemini data: {e}")
    
    # Get stock data from AlphaVantage
    symbol = st.text_input("Enter Stock Symbol", "AAPL")  # Example symbol
    if symbol:
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": ALPHA_VANTAGE_API_KEY
        }
        try:
            response = requests.get(ALPHA_VANTAGE_API_URL, params=params)
            alpha_data = response.json()
            if "Time Series (Daily)" in alpha_data:
                daily_data = alpha_data["Time Series (Daily)"]
                latest_day = list(daily_data.keys())[0]
                st.write(f"**Latest {symbol} Stock Price:** {daily_data[latest_day]['4. close']} USD")
            else:
                st.error("Error fetching AlphaVantage data.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching AlphaVantage data: {e}")

def show_dashboard(user_data):
    """Main dashboard view for authenticated users"""
    st.title(f"Welcome, {user_data['username']}!")
    st.write(f"Level: {user_data['level']} | Challenges Completed: {user_data['challenges_completed']}")

    # Display Financial Data
    display_financial_data()

    # Gamified Challenges Buttons
    st.subheader("Your Challenges")
    
    # Buttons for each challenge
    if st.button("Balance Sheet Challenge"):
        st.session_state.page = "balance_sheet"
        st.rerun()

    if st.button("EBITDA Speed Run"):
        st.session_state.page = "ebitda_speed_run"
        st.rerun()

    if st.button("Horizontal Analysis Battle"):
        st.session_state.page = "horizontal_analysis"
        st.rerun()

    if st.button("Company Face-Off"):
        st.session_state.page = "company_face_off"
        st.rerun()

def show_balance_sheet_challenge():
    st.subheader("Balance Sheet Challenge")
    st.write("This is the Balance Sheet Challenge page.")
    # Add your challenge logic here

def show_ebitda_speed_run():
    st.subheader("EBITDA Speed Run")
    st.write("This is the EBITDA Speed Run page.")
    # Add your challenge logic here

def show_horizontal_analysis():
    st.subheader("Horizontal Analysis Battle")
    st.write("This is the Horizontal Analysis Battle page.")
    # Add your challenge logic here

def show_company_face_off():
    st.subheader("Company Face-Off")
    st.write("This is the Company Face-Off page.")
    # Add your challenge logic here

def main():
    """Main app function"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False  # Initialize session state for login status
    
    if 'page' not in st.session_state:
        st.session_state.page = "home"  # Initialize page state
    
    if not st.session_state.logged_in:
        # User login form
        st.subheader("Login to Your Account")
        username = st.text_input("Username", "")
        
        if st.button("Login"):
            if username == simulated_user_data['username']:
                st.session_state.logged_in = True  # Set logged_in to True
                st.session_state.username = username  # Store the username in session state
                st.rerun()  # Refresh the page
            else:
                st.error("User not found or incorrect username.")
    else:
        # Display the main page/dashboard for authenticated users
        if st.session_state.page == "home":
            show_dashboard(simulated_user_data)
        elif st.session_state.page == "balance_sheet":
            show_balance_sheet_challenge()
        elif st.session_state.page == "ebitda_speed_run":
            show_ebitda_speed_run()
        elif st.session_state.page == "horizontal_analysis":
            show_horizontal_analysis()
        elif st.session_state.page == "company_face_off":
            show_company_face_off()

if __name__ == "__main__":
    main()
