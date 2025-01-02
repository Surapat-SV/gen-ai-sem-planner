import streamlit as st

def run_business_analyst():
    """
    Displays the Business Analyst page where users can input business details and target audience information.
    """
    st.header("Business Analyst")
    with st.form("sem_form"):
        user_input = st.text_area(
            "Describe your business and target audience:",
            placeholder="Provide business overview, audience details, and product/service info."
        )
        submitted = st.form_submit_button("Save")

    # Save the input into session state
    if submitted:
        st.session_state.user_input = user_input
        st.success("Business details saved successfully!")

