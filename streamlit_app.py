__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from crewai import Crew
from sem_agents import SEMAgents, StreamToExpander
from sem_tasks import SEMTasks
import streamlit as st
import datetime
import sys

st.set_page_config(page_icon="📊", layout="wide")

def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )

class SEMCrew:

    def __init__(self, user_input, our_url, competitor_url, query_input):
        self.user_input = user_input
        self.our_url = our_url
        self.competitor_url = competitor_url
        self.query_input = query_input
        self.output_placeholder = st.empty()

    def run(self):
        agents = SEMAgents()
        tasks = SEMTasks()

        # Create agents
        business_analyst = agents.business_analyst_agent()
        web_analyst = agents.web_analyst_agent()
        keyword_planner = agents.keyword_planner_agent()
        ad_copywriter = agents.adcopy_writer_agent()

        # Create tasks
        business_analysis_task = tasks.business_analysis_task(business_analyst, self.user_input)
        website_scraping_task = tasks.website_scraping_task(web_analyst, self.our_url, self.competitor_url, [], [])
        keyword_planner_task = tasks.keyword_planner_task(keyword_planner, self.query_input)
        ad_copywriter_task = tasks.ad_copywriter_task(ad_copywriter)
        
        full_planner_task = tasks.full_planner_task(ad_copywriter)

        # Define Crew
        crew = Crew(
            agents=[business_analyst, web_analyst, keyword_planner, ad_copywriter],
            tasks=[business_analysis_task, website_scraping_task, keyword_planner_task, ad_copywriter_task, full_planner_task],
            verbose=True
        )

        # Run Crew
        result = crew.kickoff()
        self.output_placeholder.markdown(result)
        return result

if __name__ == "__main__":
    icon("📊 SEM Planner")

    st.subheader("Optimize Your SEM Strategies with AI Agents!",
                 divider="rainbow", anchor=False)

    # Sidebar Configuration
    with st.sidebar:
        st.header("👇 Enter Details")
        with st.form("sem_form"):
            user_input = st.text_area(
                "Describe your business and target audience:",
                placeholder="Provide business overview, audience details, and product/service info."
            )
            our_url = st.text_input(
                "Our Website URL:", placeholder="https://www.ourwebsite.com"
            )
            competitor_url = st.text_input(
                "Competitor Website URL:", placeholder="https://www.competitor.com"
            )
            query_input = st.text_input(
                "Keyword Query Input:", placeholder="Enter keywords or topics to analyze."
            )

            submitted = st.form_submit_button("Submit")

    if submitted:
        with st.status("🤖 **Agents at work...**", state="running", expanded=True) as status:
            with st.container(height=500, border=False):
                sys.stdout = StreamToExpander(st)
                sem_crew = SEMCrew(user_input, our_url, competitor_url, query_input)
                result = sem_crew.run()
            status.update(label="✅ SEM Plan Ready!",
                          state="complete", expanded=False)

        st.subheader("Here is your SEM Plan", anchor=False, divider="rainbow")
        st.markdown(result)
