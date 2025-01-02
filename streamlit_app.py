__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from crewai import Crew
from sem_agents import SEMAgents, StreamToExpander
from sem_tasks import SEMTasks
import streamlit as st
import datetime
import sys

 Initialize session state variables
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "our_url" not in st.session_state:
    st.session_state.our_url = ""
if "competitor_url" not in st.session_state:
    st.session_state.competitor_url = ""
if "query_input" not in st.session_state:
    st.session_state.query_input = ""

# Setup navigation menu
PAGES = {
    "Business Analyst": "business_analyst",
    "Web Analyst": "web_analyst",
    "Keyword Planner": "keyword_planner",
    "Ad Copywriter": "ad_copywriter"
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

# Load selected page
if selection == "Business Analyst":
    st.header("Business Analyst")
    with st.form("sem_form"):
        st.session_state.user_input = st.text_area(
            "Describe your business and target audience:",
            placeholder="Provide business overview, audience details, and product/service info."
        )
        submitted = st.form_submit_button("Save")

elif selection == "Web Analyst":
    st.header("Web Analyst")
    st.session_state.our_url = st.text_input(
        "Our Website URL:", placeholder="https://www.ourwebsite.com"
    )
    st.session_state.competitor_url = st.text_input(
        "Competitor Website URL:", placeholder="https://www.competitor.com"
    )

elif selection == "Keyword Planner":
    st.header("Keyword Planner")
    st.session_state.query_input = st.text_input(
        "Keyword Query Input:", placeholder="Enter keywords or topics to analyze."
    )

elif selection == "Ad Copywriter":
    st.header("Ad Copywriter")

    # Display generate button
    if st.button("Generate SEM Plan"):
        with st.status("🤖 **Agents at work...**", state="running", expanded=True) as status:
            with st.container(height=500, border=False):
                sys.stdout = StreamToExpander(st)

                # Initialize agents and tasks
                agents = SEMAgents()
                tasks = SEMTasks()

                business_analyst = agents.business_analyst_agent()
                web_analyst = agents.web_analyst_agent()
                keyword_planner = agents.keyword_planner_agent()
                ad_copywriter = agents.adcopy_writer_agent()

                business_analysis_task = tasks.business_analysis_task(business_analyst, st.session_state.user_input)
                website_scraping_task = tasks.website_scraping_task(
                    web_analyst, st.session_state.our_url, st.session_state.competitor_url, [], []
                )
                keyword_planner_task = tasks.keyword_planner_task(keyword_planner, st.session_state.query_input)
                ad_copywriter_task = tasks.ad_copywriter_task(ad_copywriter)
                full_planner_task = tasks.full_planner_task(ad_copywriter)

                # Combine all agents and tasks
                crew = Crew(
                    agents=[business_analyst, web_analyst, keyword_planner, ad_copywriter],
                    tasks=[
                        business_analysis_task, website_scraping_task,
                        keyword_planner_task, ad_copywriter_task, full_planner_task
                    ],
                    verbose=True
                )

                # Execute the tasks
                result = crew.kickoff()
            status.update(label="✅ SEM Plan Ready!", state="complete", expanded=False)

        st.subheader("Here is your SEM Plan", anchor=False, divider="rainbow")
        st.markdown(result)

# Instructions for future extensions
# - No additional files are needed since the agents and tasks are already in sem_agents.py and sem_tasks.py.
# - This file dynamically updates session state and connects inputs to agents and tasks.
# - UI design remains compatible with existing code logic and dependencies.
