import streamlit as st
from agent import ask_nutrition_coach as nutritional_agent

st.set_page_config(
    page_title="🍏 Nutritional Coach with Mistral AI",
    page_icon="🥗",
    layout="centered",
)

st.title("🍏 Nutritional Coach with Mistral AI")
st.markdown("Ask me anything about your diet, calories, or nutrition!")

# Input box with placeholder text
query = st.text_input("Your question or request:", placeholder="e.g. 'Suggest a 2000 calorie vegan meal plan'")

# Add some vertical spacing
st.write("")

if st.button("Get Advice"):
    if not query.strip():
        st.warning("Please enter a question or request before submitting.")
    else:
        with st.spinner("Thinking... 🤔"):
            result = nutritional_agent(query)
        st.success("Here's your personalized advice:")
        st.write(result)
