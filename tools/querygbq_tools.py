import os
import json
from google.cloud import bigquery
from google.oauth2 import service_account
import streamlit as st
from langchain.tools import tool

class BigQueryTools:
    """
    A tool to fetch data from BigQuery using SQL queries. This tool is designed to work
    with Streamlit's secrets for storing Google credentials.
    """

    @tool("Query BigQuery")
    def run_bigquery(query: str):
        """
        Executes a SQL query against BigQuery and returns the results.

        Parameters:
        query (str): SQL query string to be executed.

        Returns:
        pandas.DataFrame: Query results in a DataFrame format.
        """
        try:
            # Load Google Cloud credentials from Streamlit secrets
            service_account_json = st.secrets["general"]["GOOGLE_APPLICATION_CREDENTIALS_JSON"]
            service_account_info = json.loads(service_account_json)

            # Initialize Google BigQuery client
            credentials = service_account.Credentials.from_service_account_info(service_account_info)
            client = bigquery.Client(credentials=credentials, project=service_account_info["project_id"])

            # Execute the query
            query_job = client.query(query)
            result = query_job.result()

            # Convert to a DataFrame
            df = result.to_dataframe()
            return df
        except Exception as e:
            return f"Error executing query: {e}"
