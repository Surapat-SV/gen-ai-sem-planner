__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from crewai import Crew
from sem_agents import SEMAgents, StreamToExpander
from sem_tasks import SEMTasks
import streamlit as st
import datetime
import sys

def run_ad_copywriter():
    """
    Displays the Ad Copywriter page where users can generate SEM plans.
    """
    st.header("Ad Copywriter")
    # Generate button for SEM plan
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

    # Generate button for text ads
    if st.button("Generate Text Ads"):
        with st.status("✍️ **Generating Text Ads...**", state="running", expanded=True) as status:
            ad_copywriter = SEMAgents().adcopy_writer_agent()
            ad_copywriter_task = SEMTasks().ad_copywriter_task(ad_copywriter)
            result = ad_copywriter_task.execute()
            status.update(label="✅ Text Ads Ready!", state="complete", expanded=False)

        st.subheader("Here are your Text Ads", anchor=False, divider="rainbow")
        st.markdown(result)
