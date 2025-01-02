import streamlit as st

def run_keyword_planner():
    """
    Displays the Keyword Planner page where users can input keywords or topics to analyze.
    """
    st.header("Keyword Planner")
    # Input field for keyword query
    query_input = st.text_input(
        "Keyword Query Input:", placeholder="Enter keywords or topics to analyze."
    )

    # Save input into session state
    if st.button("Save Keywords"):
        st.session_state.query_input = query_input
        st.success("Keywords saved successfully!")
