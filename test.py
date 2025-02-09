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

GEMINI_API_URL = "https://api.gemini.com/v1/pubticker/BTCUSD"  # Example API endpoint for Gemini
client1 = genai.Client(api_key="AIzaSyBHDvrG7RlUhkGPTuPG6LzUW8fG_Hqcbw8")

complete_prompt = f"Create a question and 4 answer choices about this balance sheet. Return the answer as only a json with the keys question, option_1, option_2, option_3, option_4, and correct_option"
    
        # Call the Gemini API model to generate content
responseText = client1.models.generate_content(
    model="gemini-2.0-flash",  # Replace with the desired model if different
    contents=complete_prompt
)

print(responseText)