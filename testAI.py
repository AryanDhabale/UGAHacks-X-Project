import google.generativeai as genai

# Set API key
genai.configure(api_key="452609440479")

# Choose a model (e.g., gemini-pro)
model = genai.GenerativeModel("gemini-pro")

# Generate a response
response = model.generate_content("Explain quantum physics in simple terms.")

# Print the response
print(response.text)
