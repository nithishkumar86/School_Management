from crewai import Crew
from crewai.process import Process
from CREWAI_AGENT.Crew_Agents.agents import agent1, agent2,agent3,agent4
from CREWAI_AGENT.Crewai_Tasks.crewai_tasks import task1, task2,task3,task4
from CREWAI_AGENT.Utils.Models import ModelLoader



def main():
    # Create crew with both agents
    model_loader = ModelLoader()
    llm1 = model_loader.model_loading1()
    llm2 = model_loader.model_loading2()

    crew = Crew(
        agents=[
            agent1(llm2),
            agent2(llm2),
            agent3(llm2),
            agent4(llm2)
        ],
        tasks=[
            task1(llm2),
            task2(llm2),
            task3(llm2),
            task4(llm2)
        ],
        process=Process.sequential,
        verbose=True
    )
    
    # Execute the crew
    print("="*60)
    print("STARTING SCHOOL EMAIL SENDER PROJECT")
    print("="*60)
    print("\n🤖 Agent 1: Analyzing student data...")
    print("📧 Agent 2: Will send emails after analysis...")
    print("📨 Agent 3: Sending summary reports...\n")
    
    result = crew.kickoff()
    
    print("\n" + "="*60)
    print("CREW EXECUTION COMPLETED")
    print("="*60)
    print(result)
    
    return result

