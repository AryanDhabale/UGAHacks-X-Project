import streamlit as st
import requests
from datetime import datetime

# Simulated user data for login
simulated_user_data = {
    "username": "JohnDoe", 
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

def show_dashboard(simulated_user_data):
    """Displays a visually enhanced user dashboard."""
    st.markdown(
        """
        <style>
        .big-font { font-size: 28px !important; text-align: center; color: #4A90E2; }
        .metric-box { background-color: #f5f5f5; padding: 15px; border-radius: 10px; text-align: center; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1); }
        .header { text-align: center; font-size: 32px; font-weight: bold; color: #333; padding: 20px; }
        .navbar { background-color: #4A90E2; padding: 10px 0; text-align: center; font-size: 18px; color: white; }
        .navbar a { color: white; margin: 0 15px; text-decoration: none; }
        .navbar a:hover { text-decoration: underline; }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Navbar
    st.markdown("""
        <div class="navbar">
            <a href="#">Home</a>
            <a href="#">Challenges</a>
            <a href="#">Market Data</a>
            <a href="#">Profile</a>
        </div>
        """, unsafe_allow_html=True)
    
    # Welcome Header
    st.markdown(f"<p class='header'>👋 Welcome, {st.session_state.username}!</p>", unsafe_allow_html=True)

    # User Stats Section
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='metric-box'>📈<br><b>Level</b><br>" + str(simulated_user_data["level"]) + "</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-box'>🏆<br><b>Challenges Completed</b><br>" + str(simulated_user_data["challenges_completed"]) + "</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-box'>💰<br><b>BTC Price</b><br>" + fetch_crypto_price() + "</div>", unsafe_allow_html=True)

    # Financial Data Section
    with st.container():
        st.subheader("📊 Market Data")
        symbol = st.text_input("Enter Stock Symbol", "AAPL")
        if st.button("Get Stock Price"):
            st.write(f"**{symbol} Price:** {fetch_stock_price(symbol)}")

    # Challenge Section
    with st.container():
        st.subheader("🎮 Select a Challenge")
        page_selection = st.selectbox(
            "Choose an option",
            ["select", "Balance Sheet Challenge", "EBITDA Speed Run", "Horizontal Analysis Battle", "Company Face-Off"]
        )

        if page_selection != "select":
            st.session_state.page = page_selection.lower().replace(" ", "_")
            st.rerun()

def fetch_crypto_price():
    """Fetches the BTC price from Gemini API."""
    try:
        response = requests.get(GEMINI_API_URL)
        gemini_data = response.json()
        return f"{gemini_data['last']} USD"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def fetch_stock_price(symbol):
    """Fetches stock price from AlphaVantage API."""
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
            return f"{daily_data[latest_day]['4. close']} USD"
        else:
            return "Error fetching data."
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

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