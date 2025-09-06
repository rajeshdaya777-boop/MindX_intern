# src/latest_ai_development/crew.py
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
# from crewai_tools import (DirectoryReadTool,FileReadTool,SerperDevTool,WebsiteSearchTool) # Not used, can be removed for clarity
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


@CrewBase
class LatestAiDevelopmentCrew():
    """LatestAiDevelopment crew"""

    # --- CRITICAL FIX: Define config paths for CrewBase to load them ---
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    # -----------------------------------------------------------------

    # agents: List[BaseAgent] # This is typically handled internally by CrewBase
    # tasks: List[Task]      # This is also handled internally

    # --- CRITICAL FIX: Add __init__ to call super() for CrewBase setup ---
    def __init__(self):
        super().__init__() # Call super().__init__() for CrewBase to initialize and load configs
    # ---------------------------------------------------------------------

    @agent
    def content_researcher(self) -> Agent:
        return Agent(
            # Pass the loaded configuration from self.agents_config
            config=self.agents_config['content_researcher'],
            llm=LLM(model="azure/gpt-4o", base_url="https://cloud-m9qwdilm-swedencentral.cognitiveservices.azure.com/"),
            tools=[SerperDevTool()],
            verbose=True
        )

    @agent
    def content_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['content_planner'],
            llm=LLM(model="azure/gpt-4o", base_url="https://cloud-m9qwdilm-swedencentral.cognitiveservices.azure.com/"),
            verbose=True,
            allow_delegation=False
        )

    @agent
    def copy_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['copy_writer'],
            llm=LLM(model="azure/gpt-4o", base_url="https://cloud-m9qwdilm-swedencentral.cognitiveservices.azure.com/"),
            verbose=True,
            allow_delegation=False
        )

    @agent
    def content_refiner(self) -> Agent:
        return Agent(
            config=self.agents_config['content_refiner'],
            llm=LLM(model="azure/gpt-4o", base_url="https://cloud-m9qwdilm-swedencentral.cognitiveservices.azure.com/"),
            verbose=True,
            allow_delegation=False
        )

    @agent
    def seo_optimzer(self) -> Agent:
        return Agent(
            config=self.agents_config['seo_optimzer'],
            llm=LLM(model="azure/gpt-4o", base_url="https://cloud-m9qwdilm-swedencentral.cognitiveservices.azure.com/"),
            tools=[SerperDevTool()],
            verbose=True,
            allow_delegation=False
        )

    @agent
    def content_evaluator(self) -> Agent:
        return Agent(
            config=self.agents_config['content_evaluator'],
            llm=LLM(model="azure/gpt-4o", base_url="https://cloud-m9qwdilm-swedencentral.cognitiveservices.azure.com/"),
            verbose=True,
            allow_delegation=False
        )

    @agent
    def content_formatter(self) -> Agent:
        return Agent(
            config=self.agents_config['content_formatter'],
            llm=LLM(model="azure/gpt-4o", base_url="https://cloud-m9qwdilm-swedencentral.cognitiveservices.azure.com/"),
            verbose=True,
            allow_delegation=False
        )

    @task
    def research_task(self) -> Task:
        return Task(
            agent=self.content_researcher(),
            **self.tasks_config['research_task'], # Unpack config dictionary here
            #output_file='output/research_summary.md'
        )

    @task
    def planning_task(self) -> Task:
        return Task(
            agent=self.content_planner(),
            context=[self.research_task()],
            **self.tasks_config['planning_task'],
            #output_file='output/content_plan.md'
        )

    @task
    def drafting_task(self) -> Task:
        return Task(
            agent=self.copy_writer(),
            context=[self.planning_task()],
            **self.tasks_config['drafting_task'],
            #output_file='output/first_draft.md'
        )

    @task
    def refining_task(self) -> Task:
        return Task(
            agent=self.content_refiner(),
            context=[self.drafting_task()],
            **self.tasks_config['refining_task'],
            #output_file='output/refined_content.md'
        )

    @task
    def seo_optimization_task(self) -> Task:
        return Task(
            agent=self.seo_optimzer(),
            context=[self.refining_task(), self.research_task()],
            **self.tasks_config['seo_optimization_task'],
            #output_file='output/seo_optimized_content.md'
        )

    @task
    def evaluation_task(self) -> Task:
        return Task(
            agent=self.content_evaluator(),
            context=[self.seo_optimization_task(), self.planning_task()],
            **self.tasks_config['evaluation_task'],
            #output_file='output/evaluation_report.md'
        )

    @task
    def final_formatting_task(self) -> Task:
        return Task(
            agent=self.content_formatter(),
            context=[self.seo_optimization_task(), self.evaluation_task()],
            **self.tasks_config['final_formatting_task'],
            #output_file='output/final_content_for_{content_type}.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the LatestAiDevelopment crew"""
        # self.agents and self.tasks are automatically populated by CrewBase
        # from the @agent and @task decorators, which in turn use the loaded configs.
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )