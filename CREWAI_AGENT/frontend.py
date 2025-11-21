import streamlit as st
from crewai import Crew
from crewai.process import Process
from CREWAI_AGENT.Crew_Agents.agents import agent1, agent2, agent3, agent4
from CREWAI_AGENT.Crewai_Tasks.crewai_tasks import task1, task2, task3, task4
from CREWAI_AGENT.Utils.Models import ModelLoader
import os

st.set_page_config(page_title="email sender", page_icon="📩", layout="centered")
st.header("📩 AI Multi-Agent System for Educational Management")

st.markdown("### ⚠️ Important Note")
st.markdown("Include these columns only:")
st.markdown("**roll_no, student_name, subject marks, total(optional), attendance_percentage, parent_email**")

school_name = st.text_input("School / College Name")
Exam_Name = st.text_input("Name of Examination")

file_upload = st.file_uploader(
    "Upload CSV File",
    accept_multiple_files=False,
    type=["csv"]       # Ensures only CSV files
)


# -------------------- MODEL LOADING --------------------
def model_loading():
    model_loader = ModelLoader()
    llm1 = model_loader.model_loading1()
    return llm1


# -------------------- CREW CREATION --------------------
def main():
    llm = model_loading()

    crew = Crew(
        agents=[
            agent1(llm),
            agent2(llm),
            agent3(llm),
            agent4(llm)
        ],
        tasks=[
            task1(llm),
            task2(llm),
            task3(llm),
            task4(llm)
        ],
        process=Process.sequential,
        verbose=True
    )
    return crew


# -------------------- PROCESS BUTTON --------------------
if st.button("Click to Process"):
    if not school_name or not Exam_Name:
        st.error("School name or Examination name is missing.")
        st.stop()

    if file_upload is None:
        st.error("Please upload a CSV file.")
        st.stop()

    try:
        # Save uploaded CSV
        UPLOAD_PATH = "E:\\SCHOOL_EMAIL_SENDER\\CREWAI_AGENT\\Inputs\\data.csv"
        with open(UPLOAD_PATH, "wb") as f:
            f.write(file_upload.getbuffer())

        st.success("✔ CSV file saved successfully!")

        # Run Crew
        crew = main()
        result = crew.kickoff(inputs={
            "school_name": school_name,
            "examination": Exam_Name
        })

        st.success(result)

        result = crew.kickoff(inputs={"school_name": school_name, "examination": Exam_Name})
        st.success(result)

        # # ADD DOWNLOAD OPTION HERE
        # report_path = "E:\\SCHOOL_EMAIL_SENDER\\CREWAI_AGENT\\report.md"
        # if os.path.exists(report_path):
        #     with open(report_path, "r", encoding="utf-8") as f:
        #         report_content = f.read()

        #     st.download_button(
        #         label="📥 Download Performance Report",
        #         data=report_content,
        #         file_name="student_performance_report.md",
        #         mime="text/markdown"
        #     )

    except Exception as e:
        st.error(f"Error occurred: {str(e)}")
