# agentts.py

import json
from crewai import Crew, Agent, Task,Process
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from pydantic import BaseModel,Field
from typing import List
import os
from crewai_tools import FileReadTool

load_dotenv()

llm = ChatGroq(
    model="groq/llama3-70b-8192",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

# Define output schema
class ActionItem(BaseModel):
    task: str = Field(..., description="Description of the task to be completed")
    owner: str = Field(..., description="Person responsible for the task")
    due_date: str = Field(..., description="Deadline for the task in YYYY-MM-DD format")

class MeetingSummary(BaseModel):
    date: str = Field(..., description="Meeting date in YYYY-MM-DD format")
    time: str = Field(..., description="Meeting time (e.g., '10:00 AM')")
    attendees: List[str] = Field(..., description="List of people who attended the meeting")
    project: str = Field(..., description="Name of the project discussed")
    agenda: List[str] = Field(..., description="List of agenda items covered")
    key_discussions: List[str] = Field(..., description="Important discussion points")
    decisions_made: List[str] = Field(..., description="List of decisions taken in the meeting")
    action_items: List[ActionItem] = Field(..., description="Actionable tasks assigned during the meeting")

# Crew Runner
def run_summary_agent(file_path: str):
    file_tool = FileReadTool(file_path=file_path)

    #agent 1 transcript interpreter
    interpreter = Agent(
        role = 'Transcript Interpreter',
        goal = 'Extract human-readable meeting summary from transcript',
        backstory="You are a language expert skilled in understanding and summarizing complex conversations into structured summaries.",
        tools =[file_tool],
        verbose=True,
        llm=llm

    )

    #agent 2 structuring into json format
    summarizer = Agent(
        role='JSON Structuring Agent',
        goal='Transform a human-readable meeting summary into strict JSON format based on schema.',
        backstory="You are a formatting specialist who always outputs structured, schema-valid JSON for downstream systems.",
        verbose=True,
        llm=llm
    )

    #task 1 interpret the transcript
    interpret_task = Task(
        description=(
            "Use the tool to read the meeting transcript from file.\n"
            "Then summarize the meeting into bullet-point format with the following sections:\n"
            "- Date\n- Time\n- Attendees\n- Project\n- Agenda\n"
            "- Key Discussions\n- Decisions Made\n- Action Items (with task, owner, due date)"
        ),
        expected_output=(
            "A clearly structured summary with bullet points grouped by section. "
            "Keep it concise but complete."
        ),
        tools=[file_tool],
        agent=interpreter,
        
    )
    
    #task 2

    structure_task = Task(
        description=(
            """Take the previous summary and convert it into a strict JSON format matching the schema:\n
            - date (str)\n
            - time (str)\n
            - attendees (list of str)\n
            - project (str)\n
            - agenda (list of str)\n
            - key_discussions (list of str)\n
            - decisions_made (list of str)\n
            - action_items (list of dicts with task, owner, due_date)\n\n
            -**Return only the valid JSON**. No extra commentary, no markdown. If something is missing, use placeholders."""
        ),
        expected_output="Valid JSON matching the MeetingSummary schema",
        output_json=MeetingSummary,
        agent=summarizer,
        context=[interpret_task])

    crew = Crew(
        agents=[interpreter,summarizer],
        tasks=[interpret_task,structure_task],
        process =Process.sequential,
        verbose=True
    )

    result = crew.kickoff()

    return result.raw