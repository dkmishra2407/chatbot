import streamlit as st
from google import genai
from google.genai import types
from utils import API_KEY

# Initialize the GenAI client
client = genai.Client(api_key=API_KEY)

# Define the model
MODEL_NAME = 'gemini-2.0-flash-exp'

# App UI and functionality
st.title("Stock Market Chatbot 💬")
st.write("Ask me about the top-performing stocks in specific sectors!")

# Sidebar for user instructions
with st.sidebar:
    st.header("How to Use")
    st.write("""
    - Type your question about the stock market.
    - Example: **"Top 5 stocks in the semiconductor sector of India stock market."**
    - I will analyze and fetch the data for you.
    """)

# Input from the user
user_input = st.text_input("Ask a stock-related question:", "")

# Response generation and display
if user_input:
    try:
        with st.spinner("Fetching the latest stock information..."):
            # Generate content using the GenAI model
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=user_input,
                config=types.GenerateContentConfig(
                    system_instruction="""
* Retrieve up-to-date stock information using credible financial sources.
* Present data for top 5 stocks in a given sector or based on performance metrics (e.g., market cap, ROI, growth rate). 
* Simplify explanations so even a beginner investor can understand.
* Analyze stock trends and performance (e.g., price changes, volume, key ratios like P/E and EPS).
* Assess risk factors and provide an investment rating on a scale of 1-5.
* Highlight any major news, updates, or events affecting stock performance.
* Suggest alternatives if the requested stock is underperforming or risky.
* Provide evidence-based recommendations with reasoning.
* Use Search tool for gathering the most recent data and context.
""",
                    temperature=0.3,
                ),
            )

        # Display the response
        st.success("Here's what I found:")
        st.markdown(f"**Question:** {user_input}")
        st.markdown(f"**Response:** {response.text}")

    except Exception as e:
        st.error(f"Error generating content: {e}")
else:
    st.info("Type a question above to get started!")

# Footer
st.write("---")
