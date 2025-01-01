from crewai import Task
from textwrap import dedent
from datetime import date


class SEMTasks():

    def business_analysis_task(self, agent, user_input):
        return Task(
            description=dedent(f"""
                Extract and analyze business details from the provided input.
                Focus on defining the business overview, target audience, and product/service details.
                Provide a concise summary in JSON format.

                User Input: {user_input}
            """),
            expected_output="JSON format with concise details about business overview, target audience, and product/service details.",
            agent=agent
        )

    def website_scraping_task(self, agent, our_meta, comp_meta, our_keywords, comp_keywords):
        return Task(
            description=dedent(f"""
                Scrape and analyze metadata and keywords from two websites (our website vs competitor).
                Provide insights, recommendations, and identify gaps to improve SEM strategies.

                Our Website:
                Title: {our_meta[0]}
                Description: {our_meta[1]}
                Keywords: {', '.join(our_keywords.index)}

                Competitor Website:
                Title: {comp_meta[0]}
                Description: {comp_meta[1]}
                Keywords: {', '.join(comp_keywords.index)}
            """),
            expected_output="Comparison insights, recommendations, and SEM strategy improvements.",
            agent=agent
        )

    def website_comparison_task(self, agent, our_keywords, comp_keywords):
        return Task(
            description=dedent(f"""
                Compare all keywords between our website and competitor's website using TF-IDF cosine similarity.
                Provide similarity values categorized as Low, Medium, or High.
            """),
            expected_output="Similarity values categorized as Low, Medium, or High.",
            agent=agent
        )

    def keyword_planner_task(self, agent, query_input):
        return Task(
            description=dedent(f"""
                Query keywords from BigQuery based on user input.
                Provide a comprehensive keyword planner focused on SEM strategy optimization.

                User Input: {query_input}
            """),
            expected_output="Keyword planner report based on database query and analysis.",
            agent=agent
        )

    def ad_copywriter_task(self, agent):
        return Task(
            description=dedent(f"""
                Generate Google Ads text copy, including headlines and descriptions.
                Ensure adherence to character limits and relevance to SEM strategy.
            """),
            expected_output="Headlines (30 characters) and descriptions (90 characters) suitable for Google Ads.",
            agent=agent
        )

    def full_planner_task(self, agent):
        return Task(
            description=dedent(f"""
                Compile a full SEM planner report.
                Integrate outputs from all agents including business analysis, website analysis, keyword planning, and ad copywriting.
                Present the final report in markdown format.
            """),
            expected_output="Complete SEM planner report formatted as markdown, integrating all agent outputs.",
            agent=agent
        )
