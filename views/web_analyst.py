import streamlit as st

def run_web_analyst():
    """
    Displays the Web Analyst page where users can input website URLs for analysis.
    """
    st.header("Web Analyst")
    # Input fields for website URLs
    our_url = st.text_input(
        "Our Website URL:", placeholder="https://www.ourwebsite.com"
    )
    competitor_url = st.text_input(
        "Competitor Website URL:", placeholder="https://www.competitor.com"
    )

    # Save inputs into session state
    if st.button("Save URLs"):
        st.session_state.our_url = our_url
        st.session_state.competitor_url = competitor_url
        st.success("Website URLs saved successfully!")

