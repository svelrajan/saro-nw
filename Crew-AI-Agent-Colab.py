!pip install crewai google-generativeai python-dotenv

import os

from rich.console import Console
import sys
import builtins

# Create a safe console for Jupyter (no ANSI, no recursion)
console = Console(force_terminal=False, file=sys.__stdout__)

# Optional: make all `print()` use the safe console
builtins.print = console.print

from google.colab import userdata
os.environ["GOOGLE_API_KEY"] = userdata.get('GOOGLE_API_KEY')

from crewai import Agent, Task, Crew, LLM

# Use LangChain-compatible Gemini
llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
    api_key=os.environ["GOOGLE_API_KEY"]
)
researcher = Agent(
    role="Network Security Administrator",
    goal="Find top network security vulnerabilities",
    backstory="You work at a network products company with rich networking experience.",
    verbose=True,
    llm=llm
)

# CERT - Computer Emergency Response Team

task = Task(
    description="Analyze the latest CERT recommendations about network security vulnerabilities.",
    expected_output="A concise report listing 3 top CERT recommendations from CERT for addressing network security vulnerabilities.",
    max_inter=5,
    agent=researcher
)

crew = Crew(agents=[researcher],
            tasks=[task], verbose=True)

result = crew.kickoff()

print("\n Final Output:\n", result)
