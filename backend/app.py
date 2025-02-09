import streamlit as st
import pandas as pd
import requests
import pymongo
from pymongo import MongoClient
import re
import json
import os
from datetime import datetime
from random import sample
from google import genai
import fitz
import plotly.express as px
import random
import PyPDF2
from io import BytesIO
import base64;
import yfinance as yf
from faceOffGame import playfaceOffGame
from balanceSheet import playBalanceSheetGame
from horizontalGame import playHorizontalAnalysisGame
from ebidtaGame import playEbidtaGame
st.set_page_config(layout="wide")

# Simulated user data for login
simulated_user_data = {
    "username": "JohnDoe",  
    "level": 1,
    "challenges_completed": 5,
    "curXP" : 690,
    "fullXP" : 800

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
questions_collection2 = db["gamedata1"]

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
            <a href="#">Play Games to Learn More, and Level Up!!!</a>
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
        st.markdown("<div class='metric-box'>💰<br><b>XP to Next Level</b><br>" + str(simulated_user_data["curXP"]) + "/"+ str(simulated_user_data["fullXP"]) + "</div>", unsafe_allow_html=True)

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
        st.image(img, caption="Balance Sheet", width=700)

        # Extract text from the uploaded PDF
        text = extract_text_from_pdf(uploaded_pdf)
        sheet = generate_balance_sheet(text)
        complete_prompt = f'Give me a precise analysis of this balance sheet covering the most important topics and ratios: {sheet}'
        # Call the Gemini API model to generate content
        responseText = client1.models.generate_content(
            model="gemini-2.0-flash",  # Replace with the desired model if different
            contents=complete_prompt
        )
        st.write(responseText.candidates[0].content.parts[0].text)
        
        if st.button("Get Response"):
            # Get the AI response when the button is pressed
            responseText = client1.models.generate_content(
                model="gemini-2.0-flash",  # Replace with the desired model if different
                contents=complete_prompt
            )
            st.write(responseText.candidates[0].content.parts[0].text)

    # Load preloaded questions from JSON
    with open('preloadedQuestions.json', 'r') as file:
        PRELOADED_QUESTIONS = [
    {
        "question": "What is the primary purpose of a balance sheet?",
        "options": ["Show revenue", "Track financial position", "Record daily transactions", "Calculate profit"],
        "correct_option": "Track financial position"
    },
    {
        "question": "Which of the following represents liabilities in a balance sheet?",
        "options": ["Assets", "Equity", "Debt", "Revenue"],
        "correct_option": "Debt"
    },
    {
        "question": "Which ratio is calculated by dividing total liabilities by total assets?",
        "options": ["Current ratio", "Debt-to-equity ratio", "Debt ratio", "Quick ratio"],
        "correct_option": "Debt ratio"
    },
    {
        "question": "Which section of the balance sheet includes retained earnings?",
        "options": ["Assets", "Liabilities", "Equity", "Revenue"],
        "correct_option": "Equity"
    },
    {
        "question": "What does the current ratio measure?",
        "options": ["Liquidity", "Profitability", "Efficiency", "Leverage"],
        "correct_option": "Liquidity"
    },
    {
        "question": "Which of the following would be classified as a non-current asset?",
        "options": ["Inventory", "Accounts receivable", "Buildings", "Cash"],
        "correct_option": "Buildings"
    },
    {
        "question": "What is the formula for the return on equity (ROE) ratio?",
        "options": ["Net income / Total assets", "Net income / Shareholder's equity", "Operating income / Total liabilities", "Gross profit / Net revenue"],
        "correct_option": "Net income / Shareholder's equity"
    },
    {
        "question": "Which of the following is NOT a part of shareholder's equity?",
        "options": ["Common stock", "Retained earnings", "Accounts payable", "Additional paid-in capital"],
        "correct_option": "Accounts payable"
    },
    {
        "question": "What does the quick ratio exclude from current assets?",
        "options": ["Cash", "Inventory", "Receivables", "Prepaid expenses"],
        "correct_option": "Inventory"
    },
    {
        "question": "What does a high debt-to-equity ratio indicate?",
        "options": ["A company relies more on equity financing than debt", "A company relies more on debt financing than equity", "A company has low financial risk", "A company is highly liquid"],
        "correct_option": "A company relies more on debt financing than equity"
    },
    {
        "question": "Which of the following is an example of an intangible asset on the balance sheet?",
        "options": ["Buildings", "Goodwill", "Accounts receivable", "Inventory"],
        "correct_option": "Goodwill"
    },
    {
        "question": "Which item would most likely be found under current liabilities?",
        "options": ["Long-term debt", "Accounts payable", "Shareholder's equity", "Land"],
        "correct_option": "Accounts payable"
    },
    {
        "question": "Which financial ratio is used to assess a company's ability to pay off its short-term obligations?",
        "options": ["Current ratio", "Quick ratio", "Debt-to-equity ratio", "Gross margin ratio"],
        "correct_option": "Current ratio"
    },
    {
        "question": "What does the cash ratio measure?",
        "options": ["Liquidity", "Profitability", "Leverage", "Efficiency"],
        "correct_option": "Liquidity"
    },
    {
        "question": "Which of the following would be classified as an asset?",
        "options": ["Accounts payable", "Cash", "Loans payable", "Equity"],
        "correct_option": "Cash"
    },
    {
        "question": "What is the primary distinction between current and non-current assets?",
        "options": ["Timeframe for conversion to cash", "Amount of debt", "Nature of ownership", "Type of expense"],
        "correct_option": "Timeframe for conversion to cash"
    },
    {
        "question": "Which of the following would typically be classified as a non-current liability?",
        "options": ["Accounts payable", "Long-term debt", "Short-term loans", "Wages payable"],
        "correct_option": "Long-term debt"
    },
    {
        "question": "What is the formula for the acid-test ratio?",
        "options": ["(Current assets - Inventory) / Current liabilities", "Current assets / Current liabilities", "Cash / Current liabilities", "Net income / Total assets"],
        "correct_option": "(Current assets - Inventory) / Current liabilities"
    },
    {
        "question": "Which of the following best describes 'equity' on a balance sheet?",
        "options": ["The value of the company's assets", "The value of the company's liabilities", "The residual interest in assets after liabilities are deducted", "The total revenue earned by the company"],
        "correct_option": "The residual interest in assets after liabilities are deducted"
    },
    {
        "question": "What type of account is 'Accounts Receivable' on a balance sheet?",
        "options": ["Asset", "Liability", "Equity", "Revenue"],
        "correct_option": "Asset"
    },
    {
        "question": "How is owner's equity calculated on the balance sheet?",
        "options": ["Assets - Liabilities", "Assets + Liabilities", "Revenue - Expenses", "Current assets + Non-current assets"],
        "correct_option": "Assets - Liabilities"
    },
    {
        "question": "What does the debt-to-equity ratio measure?",
        "options": ["The proportion of a company’s financing that comes from debt", "The company’s ability to pay short-term liabilities", "The company's profitability", "The value of a company's equity relative to its assets"],
        "correct_option": "The proportion of a company’s financing that comes from debt"
    },
    {
        "question": "Which of the following items would typically be found under non-current liabilities?",
        "options": ["Accounts payable", "Wages payable", "Long-term debt", "Cash equivalents"],
        "correct_option": "Long-term debt"
    },
    {
        "question": "What is the 'return on assets' (ROA) ratio used to assess?",
        "options": ["How much profit is generated from the company's assets", "The company’s ability to meet its short-term obligations", "The company's debt levels", "The company's gross profit margin"],
        "correct_option": "How much profit is generated from the company's assets"
    },
    {
        "question": "Which of the following is an example of a tangible asset?",
        "options": ["Patent", "Goodwill", "Building", "Trademark"],
        "correct_option": "Building"
    },
    {
        "question": "What does the term 'working capital' refer to?",
        "options": ["Current assets - Current liabilities", "Net income - Dividends", "Cash available for capital expenditures", "Revenue - Expenses"],
        "correct_option": "Current assets - Current liabilities"
    },
    {
        "question": "What would be included in 'current liabilities'?",
        "options": ["Accounts payable", "Accounts receivable", "Long-term debt", "Common stock"],
        "correct_option": "Accounts payable"
    },
    {
        "question": "Which financial statement provides the details of a company's revenue and expenses?",
        "options": ["Balance sheet", "Income statement", "Statement of cash flows", "Statement of changes in equity"],
        "correct_option": "Income statement"
    },
    {
        "question": "How is the 'price-to-earnings' (P/E) ratio calculated?",
        "options": ["Market price per share / Earnings per share", "Earnings per share / Market price per share", "Market price per share / Book value per share", "Net income / Shareholder's equity"],
        "correct_option": "Market price per share / Earnings per share"
    },
    {
        "question": "What is the formula for calculating the net working capital?",
        "options": ["Current assets / Current liabilities", "Total liabilities / Shareholder's equity", "Current assets - Current liabilities", "Long-term assets - Long-term liabilities"],
        "correct_option": "Current assets - Current liabilities"
    },
    {
        "question": "Which of the following would be considered a liability on the balance sheet?",
        "options": ["Accounts payable", "Cash", "Goodwill", "Common stock"],
        "correct_option": "Accounts payable"
    },
    {
        "question": "What does the term 'solvency' refer to?",
        "options": ["The ability of a company to meet its long-term financial obligations", "The ability of a company to pay short-term obligations", "The company's profitability", "The company's liquidity"],
        "correct_option": "The ability of a company to meet its long-term financial obligations"
    },
    {
        "question": "Which of the following ratios measures a company's ability to pay its short-term liabilities?",
        "options": ["Current ratio", "Debt ratio", "Return on equity", "Gross margin ratio"],
        "correct_option": "Current ratio"
    },
    {
        "question": "What type of account is 'Inventory' on a balance sheet?",
        "options": ["Asset", "Liability", "Equity", "Revenue"],
        "correct_option": "Asset"
    },
    {
        "question": "What is the formula for calculating return on investment (ROI)?",
        "options": ["Net income / Total assets", "Net income / Shareholder's equity", "Net profit / Cost of investment", "Earnings before interest and taxes / Assets"],
        "correct_option": "Net profit / Cost of investment"
    },
    {
        "question": "Which of the following is considered a non-operating item on a balance sheet?",
        "options": ["Cash", "Accounts payable", "Interest income", "Inventory"],
        "correct_option": "Interest income"
    },
    {
        "question": "What does 'liquidity' refer to in financial analysis?",
        "options": ["A company's ability to pay its debts when they come due", "The profitability of a company", "The company's operating efficiency", "The value of a company’s long-term assets"],
        "correct_option": "A company's ability to pay its debts when they come due"
    },
    {
        "question": "Which section of the balance sheet would 'long-term investments' be classified?",
        "options": ["Assets", "Liabilities", "Equity", "Revenue"],
        "correct_option": "Assets"
    },
    {
        "question": "Which of the following is a characteristic of current liabilities?",
        "options": ["Due within one year or within the company's operating cycle", "Due after more than one year", "Represent ownership interest", "Include long-term debt"],
        "correct_option": "Due within one year or within the company's operating cycle"
    }
]

    # Initialize session state variables
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
        st.session_state.options = []
        st.session_state.correct_answer = None
        st.session_state.answer_submitted = False
        st.session_state.preloaded_index = 0  # Track preloaded questions

    use_preloaded = st.session_state.preloaded_index < len(PRELOADED_QUESTIONS)

    # Generate a new question if none exists
    if st.session_state.current_question is None:
        if use_preloaded:
            # Use preloaded question
            question_data = PRELOADED_QUESTIONS[st.session_state.preloaded_index]
            st.session_state.current_question = question_data["question"]
            st.session_state.options = question_data["options"]
            st.session_state.correct_answer = question_data["correct_option"]
        else:
            # Generate an AI question (Placeholder for now)
            generated_question = {
                "question": "Placeholder: What is the purpose of a balance sheet?",
                "options": ["Show revenue", "Track financial position", "Record daily transactions", "Calculate profit"],
                "correct_option": "Track financial position"
            }
            st.session_state.current_question = generated_question["question"]
            st.session_state.options = generated_question["options"]
            st.session_state.correct_answer = generated_question["correct_option"]

    # Display the question
    st.write("### Question:")
    st.write(st.session_state.current_question)

    # Multiple-choice options
    user_answer = st.radio("Select your answer:", st.session_state.options, key="user_answer")

    # Submit Answer
    if st.button("Submit Answer", key="submit_answer") and not st.session_state.answer_submitted:
        if user_answer == st.session_state.correct_answer:
            st.session_state.score += 1
            st.write("✅ Correct! Your score is:", st.session_state.score)
        else:
            st.write("❌ Incorrect. The correct answer was:", st.session_state.correct_answer)

        st.session_state.answer_submitted = True

    # Show "Next Question" button **only after** user submits an answer
    if st.session_state.answer_submitted:
        if st.button("Next Question", key="next_question"):
            if use_preloaded:
                st.session_state.preloaded_index += 1  # Move to next preloaded question
            st.session_state.current_question = None  # Reset question
            st.session_state.answer_submitted = False  # Reset submission status
            st.rerun()

    # Display the score
    st.write("### Your Score:", st.session_state.score)

    # Back to Home Button
    if st.button("Back to Home", key="back_home"):
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

def fetch_stock_data(ticker):
    """Fetch historical stock data for the given ticker."""
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y", interval="3mo")  # Quarterly data
    hist.reset_index(inplace=True)
    return hist

def plot_stock_chart(data, stock_name):
    """Generate a stock chart using Plotly."""
    fig = px.line(data, x="Date", y="Close", title=f"{stock_name} Stock Performance", markers=True)
    fig.update_layout(xaxis_title="Date", yaxis_title="Closing Price", template="plotly_dark")
    return fig

def display_questions():
    """Display multiple-choice questions related to the stock data."""
    # Fetch 5 random questions from MongoDB
    questions = list(questions_collection.aggregate([{"$sample": {"size": 5}}]))

    if not questions:
        st.warning("No questions available.")
        return

    # Display the questions
    for i, question in enumerate(questions, start=1):
        st.subheader(f"Q{i}: {question['question']}")
        
        options = question['options']
        correct_answer = question['correct_answer']
        
        answer = st.radio(f"Select an option for Q{i}", options)
        
        if answer:
            if answer == correct_answer:
                st.success(f"Correct! {correct_answer} is the right answer.")
            else:
                st.error(f"Incorrect! The correct answer was {correct_answer}.")

def show_company_face_off():
    """Display two user-input companies for the face-off game."""
    st.header("Company Face-Off!")

    stock1 = st.text_input("Enter first stock ticker (e.g., AAPL):", value="AAPL").upper()
    stock2 = st.text_input("Enter second stock ticker (e.g., MSFT):", value="MSFT").upper()

    if st.button("Compare Stocks"):
        data1 = fetch_stock_data(stock1)
        data2 = fetch_stock_data(stock2)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(stock1)
            chart1 = plot_stock_chart(data1, stock1)
            if chart1:
                st.plotly_chart(chart1)

        with col2:
            st.subheader(stock2)
            chart2 = plot_stock_chart(data2, stock2)
            if chart2:
                st.plotly_chart(chart2)

        # Show the questions after stock charts are displayed
        display_questions()

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
        "3. Make sure to use the graphs to answer the questions for specific companies."
    )
    stock1 = st.text_input("Enter first stock ticker (e.g., AAPL):", value="AAPL").upper()
    stock2 = st.text_input("Enter second stock ticker (e.g., MSFT):", value="MSFT").upper()

    if st.button("Compare Stocks"):
        data1 = fetch_stock_data(stock1)
        data2 = fetch_stock_data(stock2)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(stock1)
            chart1 = plot_stock_chart(data1, stock1)
            if chart1:
                st.plotly_chart(chart1)

        with col2:
            st.subheader(stock2)
            chart2 = plot_stock_chart(data2, stock2)
            if chart2:
                st.plotly_chart(chart2)

    display_questions()

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
            show_company_face_off()

if __name__ == "__main__":
    main()