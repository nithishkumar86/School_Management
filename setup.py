from setuptools import find_packages,setup

setup(name="School Email Sender",
      version="0.0.1",
      author="nithishkumar",
      author_email="mnithish1231234@gmail.com",
      packages=find_packages(),
      install_requires=["crewai","crewai-tools","streamlit","python-dotenv"])