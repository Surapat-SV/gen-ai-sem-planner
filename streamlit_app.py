__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from crewai import Crew
from sem_agents import SEMAgents, StreamToExpander
from sem_tasks import SEMTasks
from streamlit_option_menu import option_menu
import streamlit as st
import datetime
import sys

# Import view modules for modular design
from views.business_analyst import run_business_analyst
from views.web_analyst import run_web_analyst
from views.keyword_planner import run_keyword_planner
from views.ad_copywriter import run_ad_copywriter

# Set Streamlit page configuration
st.set_page_config(layout="wide", initial_sidebar_state="auto")

# Sidebar navigation menu
with st.sidebar:
    selected = option_menu(
        'Menu',
        ['Business Analyst', 'Web Analyst', 'Keyword Planner', 'Ad Copywriter'],
        icons=['briefcase', 'globe', 'key', 'pencil'],
        default_index=0
    )

# Route to appropriate views based on selection
if selected == 'Business Analyst':
    run_business_analyst()

elif selected == 'Web Analyst':
    run_web_analyst()

elif selected == 'Keyword Planner':
    run_keyword_planner()

elif selected == 'Ad Copywriter':
    run_ad_copywriter()
