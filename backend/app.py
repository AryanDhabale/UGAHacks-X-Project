import streamlit as st
import pandas as pd
import requests
import pymongo
import json
import os
from datetime import datetime
from random import sample
from google import genai
import fitz
import PyPDF2
from io import BytesIO
import base64;
from faceOffGame import playfaceOffGame
from balanceSheet import playBalanceSheetGame
from horizontalGame import playHorizontalAnalysisGame
from ebidtaGame import playEbidtaGame
st.set_page_config(layout="wide")

# Simulated user data for login
simulated_user_data = {
    "username": "JohnDoe",  
    "level": 1,
    "challenges_completed": 5
}

# Gemini API setup (for example)
GEMINI_API_URL = "https://api.gemini.com/v1/pubticker/BTCUSD"  # Example API endpoint for Gemini
client1 = genai.Client(api_key="AIzaSyBHDvrG7RlUhkGPTuPG6LzUW8fG_Hqcbw8")

# AlphaVantage API setup (for financial data)
ALPHA_VANTAGE_API_KEY = "IJ3GJBXDGDD3FQ1X"
ALPHA_VANTAGE_API_URL = "https://www.alphavantage.co/query"

# MongoDB Connection
MONGO_URI = "mongodb+srv://samarjeetpurba:cyttZfEIUfkxEE9W@hacksxcluster.wm7pl.mongodb.net/datastorage?retryWrites=true&w=majority"
client = pymongo.MongoClient(MONGO_URI)
db = client["datastorage"]
questions_collection = db["gamedata1"]

def get_gemini_ai_response(prompt):
    # Add the preset instruction to the prompt
    complete_prompt = f"{prompt}\n\nPlease limit answers to financing, economics, accounting, or similar topics. Be detailed but not too long either."
    
    # Call the Gemini API model to generate content
    response = client1.models.generate_content(
        model="gemini-2.0-flash",  # Replace with the desired model if different
        contents=complete_prompt
    )
    
    # Return the generated response text
    return response.text

def extract_text_from_pdf(pdf_file):
    """Extract text using PyPDF2 as a backup."""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_text = ""
        
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
        
        return pdf_text
    except Exception as e:
        return f"Error using PyPDF2: {str(e)}"

def generate_balance_sheet(prompt):
    # Add the preset instruction to the prompt
    complete_prompt = f"clean and convert this into a table of just the balance sheet. Limit the answer to just a table of the balance sheet and a title of it above:{prompt}"
    
    # Call the Gemini API model to generate content
    response = client1.models.generate_content(
        model="gemini-2.0-flash",  # Replace with the desired model if different
        contents=complete_prompt
    )
    
    # Return the generated response text
    return response.text

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
            ["select", "Balance Sheet Challenge", "EBITDA Speed Run", "Horizontal Analysis Battle", "Company Face Off"]
        )

        if page_selection != "select":
            st.session_state.page = page_selection.lower().replace(" ", "_")
            st.rerun()

    with st.container():
        st.subheader("🔷 Questions? Ask here!")
        symbol1 = st.text_input("Enter a prompt", "What is finance?")  # Default prompt
    
        if st.button("Get Response"):
            # Get the AI response when the button is pressed
            ai_response = get_gemini_ai_response(symbol1)
        
            # Display the response in the Streamlit app
            st.write(ai_response)

    uploaded_pdf = st.file_uploader("Upload the Balance Sheet PDF", type=["pdf"])

    if uploaded_pdf is not None:
        # Extract text from the uploaded PDF
        text = extract_text_from_pdf(uploaded_pdf)
        sheet = generate_balance_sheet(text)
        # Display the extracted text
        st.subheader("Extracted Text from Balance Sheet")
        st.text_area("Balance Sheet Text", sheet, height=400)

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

def show_balance_sheet_challenge():
    """Displays the Balance Sheet Challenge page."""
    st.subheader("📊 Balance Sheet Challenge")
    st.write(
        "Welcome to the Balance Sheet Challenge! In this challenge, you will analyze the "
        "balance sheet of a company and answer questions about its financial position."
    )

    # Frame for the challenge content
    st.write("### Instructions:")
    st.write(
        "1. Review the balance sheet provided.\n"
        "2. Answer the questions related to the company's assets, liabilities, and equity.\n"
        "3. Submit your answers to get feedback on your performance."
    )

    st.write("### Balance Sheet Data:")

    # Placeholder for the user-uploaded PDF file
    uploaded_pdf = st.file_uploader("Upload Balance Sheet PDF", type=["pdf"])
    
    if uploaded_pdf is not None:
        # Open the uploaded PDF with PyMuPDF (fitz)
        pdf_document = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
        
        # Extract the first page of the PDF as an image
        page = pdf_document.load_page(0)  # load the first page (0-indexed)
        pix = page.get_pixmap()  # render page to a pixmap (image)
        
        # Convert the pixmap to a PIL image
        img = pix.pil_image()  # PIL Image object
        
        # Display the image in Streamlit
        st.image(img, caption="Balance Sheet", use_container_width=True)

        # Extract text from the uploaded PDF
        text = extract_text_from_pdf(uploaded_pdf)
        sheet = generate_balance_sheet(text)
        complete_prompt = f"Create a question and 4 answer choices about this balance sheet. Return the answer as only a json with the keys question, option_1, option_2, option_3, option_4, and correct_option {sheet}"
    
        # Call the Gemini API model to generate content
        responseText = client1.models.generate_content(
            model="gemini-2.0-flash",  # Replace with the desired model if different
            contents=complete_prompt
        )

        raw_text = responseText.candidates[0].content.parts[0].text  

        # Remove the triple backticks and the "json" label
        json_match = re.search(r'```json\n(.*)\n```', raw_text, re.DOTALL)

        if json_match:
            json_string = json_match.group(1)  # Extract the actual JSON content
            try:
                response = json.loads(json_string)  # Parse as JSON
                
                # Define the question and options
                question = response["question"]
                options = [response["option_1"], response["option_2"], response["option_3"], response["option_4"]]
                correct_answer = response["correct_option"]

                # Display the question and multiple choice options
                st.write("### Question:")
                st.write(question)
                
                user_answer = st.radio("Select your answer:", options)
                
                # Placeholder for user input and score
                if 'score' not in st.session_state:
                    st.session_state.score = 0
                
                # Check if the user answer is correct and update the score
                if st.button("Submit Answer"):
                    if user_answer == correct_answer:
                        st.session_state.score += 1
                        st.write("Correct! Your score is:", st.session_state.score)
                    else:
                        st.write("Incorrect. The correct answer was:", correct_answer)
                
                # Display the current score
                st.write("### Your Score:", st.session_state.score)
                
                # Placeholder for additional user interaction (text analysis)
                user_input = st.text_area("Enter your analysis or comments here:")

            except json.JSONDecodeError:
                st.write("Error: The extracted text is not valid JSON.")
                st.write("Extracted Content:")
                st.write(json_string)

        else:
            st.write("Error: Could not extract JSON from the model response.")
            st.write("Raw Response:")
            st.write(raw_text)

    if st.button("Submit Answer"):
        st.write("You submitted the following analysis:")
        st.write(user_input)

    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()


def show_ebitda_speed_run():
    """Displays the EBITDA Speed Run page."""
    st.subheader("💨 EBITDA Speed Run")
    st.write(
        "Welcome to the EBITDA Speed Run! In this challenge, you will calculate the EBITDA of "
        "a company based on provided financial data. Your goal is to do it as quickly as possible."
    )
    # Frame for the challenge content
    st.write("### Instructions:")
    st.write(
        "1. Review the company's income statement.\n"
        "2. Calculate the EBITDA using the provided data.\n"
        "3. Submit your result to see how fast you can calculate it!"
    )
    
    # Placeholder for financial data (income statement)
    st.write("### Income Statement Data:")
    # Placeholder for income statement data (you can use tables, charts, or images here)
    st.write("Income Statement Data would appear here.")
    
    # Placeholder for user input (e.g., the EBITDA calculation)
    user_input = st.text_input("Enter your EBITDA calculation:")
    if st.button("Submit Answer"):
        st.write(f"You calculated EBITDA as: {user_input}")
    
    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()

def show_horizontal_analysis():
    """Displays the Horizontal Analysis Battle page."""
    st.subheader("📉 Horizontal Analysis Battle")
    st.write(
        "Welcome to the Horizontal Analysis Battle! In this challenge, you will analyze the "
        "financial performance of a company over multiple periods."
    )
    # Frame for the challenge content
    st.write("### Instructions:")
    st.write(
        "1. Review the financial data for multiple periods.\n"
        "2. Perform horizontal analysis by calculating growth rates.\n"
        "3. Answer questions about the company's performance over time."
    )
    
    # Placeholder for financial data (multiple periods)
    st.write("### Financial Data (Multiple Periods):")
    # Placeholder for financial data over periods
    st.write("Financial Data would appear here.")
    
    # Placeholder for user interaction (e.g., answer analysis)
    user_input = st.text_area("Enter your horizontal analysis results:")
    if st.button("Submit Answer"):
        st.write("Your analysis:")
        st.write(user_input)
    
    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()

def show_company_face_off():
    """Displays the Company Face-Off page."""
    st.subheader("🏢 Company Face-Off")
    st.write(
        "Welcome to the Company Face-Off! In this challenge, you will compare the financials "
        "of two companies and determine which one is performing better."
    )
    # Frame for the challenge content
    st.write("### Instructions:")
    st.write(
        "1. Compare the financial performance of two companies based on provided data.\n"
        "2. Make a decision on which company is performing better in terms of profitability, "
        "growth, and other financial metrics.\n"
        "3. Submit your results to see if you made the right choice!"
    )
    
    # Placeholder for financial data (company comparison)
    st.write("### Company Financial Data:")
    # Placeholder for financial data comparison between companies
    st.write("Company 1 and Company 2 data would appear here.")
    
    # Placeholder for user decision (e.g., which company performs better)
    user_input = st.radio(
        "Which company is performing better?",
        ("Company 1", "Company 2")
    )
    if st.button("Submit Decision"):
        st.write(f"You chose: {user_input}")
    
    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()

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
        elif st.session_state.page == "balance_sheet_challenge":
            show_balance_sheet_challenge()
        elif st.session_state.page == "ebitda_speed_run":
            playEbidtaGame()
        elif st.session_state.page == "horizontal_analysis_battle":
            playHorizontalAnalysisGame()
        elif st.session_state.page == "company_face_off":
            playfaceOffGame()

if __name__ == "__main__":
    main()