# from crewai import Task,Agent,LLM,Process,Crew
# from CREWAI_AGENT.Config.configfile import load_config
# import os
# from dotenv import load_dotenv

# # def _load_environ():
# #     load_dotenv()
# #     OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
# #     if OPENROUTER_API_KEY:
# #         return OPENROUTER_API_KEY
# #     else:
# #         raise EnvironmentError("There is no OPENROUTER_API_KEY")

# # def load_model():
# #     config = load_config()
# #     llm = LLM(
# #         model =config['model1']['provider'] +" / "+config["model1"]["model"],
# #         base_url="https://openrouter.ai/api/v1",
# #         api_key=_load_environ(),
# #         # Add rate limiting parameters
# #         temperature=config['model1']['temperature'],
# #         max_tokens=config['model1']['max_tokens'],
# #         timeout=config['model1']['timeout']
# #     )


# # GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# # if GOOGLE_API_KEY:
# #     load_dotenv()
# #     os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY
# # else:
# #     raise EnvironmentError("there is no GOOGLE_API_KEY")

# config = load_config()

# llm = LLM(
#     model=config["model2"]["provider"] + "/" + config["model2"]["model"],
#     base_url=config["model2"]["baseurl"]
# )

# def agent4(llm) -> Agent:
#     return Agent(
#         role="ReportGeneratorAgent",
#         goal=(
#             "Generate a comprehensive student performance report with visualizations "
#             "and detailed analysis for submission to HOD/Principal."
#         ),
#         backstory=(
#             "You are an expert data analyst and report writer specializing in educational analytics. "
#             "Your role is to create professional, insightful reports for school management that combine "
#             "statistical analysis, visual representations, and actionable recommendations. "
#             "You have access to the original student data in the 'Inputs' directory (data.csv) "
#             "and the processed results in the 'Outputs' directory. You analyze this data to create "
#             "comprehensive reports that help school leadership make informed decisions about "
#             "student welfare, academic improvements, and resource allocation. "
#             "You create visualizations (charts, graphs) and write detailed narrative reports "
#             "that are clear, professional, and actionable."
#         ),
#         verbose=True,
#         llm=llm
#     )


# def task4(llm) -> Task:
#     return Task(
#         name="Comprehensive Report Generator",
#         description=(
#             "Create a detailed student performance report for HOD/Principal submission. "
#             "\n\n"
#             "striclty use this data soure DATA SOURCES AVAILABLE to analyze :\n"
#             "1. Original Data: E:\\SCHOOL_EMAIL_SENDER\\CREWAI_AGENT\\Inputs\\data.csv\n"
#             "YOUR TASK:\n"
#             " create a comprehensive report that includes:\n"
#             "\n"

#             "3.perform some analysis on the dataset and make some impactfull decisions"

#             "4. STUDENT CATEGORIZATION\n"
#             "   - High performers (>80% marks + >80% attendance) - List names\n"
#             "   - At-risk students (failed subjects or low attendance) - List names with specific issues\n"
#             "   - Borderline students (close to failing) - List names\n"
#             "\n"
#             "6. RECOMMENDATIONS\n"
#             "   - Immediate actions for struggling students\n"
#             "   - Subject-specific interventions needed\n"
#             "   - Attendance improvement strategies\n"
#             "   - Resource allocation suggestions\n"
#             "   - Parent-teacher meeting recommendations\n"
#             "\n"
#             "7. CONCLUSION\n"
#             "   - Overall assessment of class performance\n"
#             "   - Next steps and timeline\n"
#             "\n"
#             "FORMAT: Create a professional, well-structured report in a formal tone suitable for "
#             "school management review. Use proper headings, bullet points, and clear language. "
#             "Include specific numbers, percentages, and student names where appropriate."
#             "store the report in 'report.md' file"
#         ),
# expected_output=(
#             "A simple, clear report with:\n"
#             "1. Summary paragraph\n"
#             "2. Subject performance section\n"
#             "3. Attendance analysis\n"
#             "4. Actions taken summary\n"
#             "5. Simple recommendations list\n\n"
#             "Length: 500-800 words\n"
#             "Format: Markdown with headings\n"
#             "Tone: Professional but straightforward"
#         ),
#         agent=agent4(llm),
#         output_file="report.md"
#     )


# def main():

#     crew_kick= Crew(agents=[agent4(llm=llm)],
#                     tasks=[task4(llm=llm)],
#                     process=Process.sequential,
#                     verbose=True)

#     result = crew_kick.kickoff()
    
#     print("\n" + "="*80)
#     print("CREW EXECUTION COMPLETED - FINAL REPORT GENERATED")
#     print("="*80)
#     print("\n📄 FINAL MANAGEMENT REPORT:\n")
#     print(result)


# if __name__ == "__main__":
#     main()
    
