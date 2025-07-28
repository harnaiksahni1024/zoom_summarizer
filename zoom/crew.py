from crewai import Crew, Agent, Task, Process
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List
import os
from crewai import LLM

load_dotenv()
llm = LLM(
model="openrouter/deepseek/deepseek-chat-v3-0324",
base_url="https://openrouter.ai/api/v1",
api_key=os.getenv("OPENROUTER_API_KEY"),
max_tokens = 2048 
)


# llm = ChatGroq(
#     model="groq/llama3-8b-8192",

#     api_key=os.getenv("GROQ_API_KEY")
# )

# Output schema
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

def run_summary_agent(file_path: str):
    #  Read the transcript content directly
    with open(file_path, 'r', encoding='utf-8') as f:
        transcript_text = f.read()

    #  Agent 1: Summary writer
    interpreter = Agent(
        role='Transcript Interpreter',
        goal='Extract a clean, structured human-readable meeting summary from a transcript',
        backstory=(
            "You're an expert at understanding messy conversations and extracting key points "
            "with clarity and precision."
        ),
        verbose=True,
        llm=llm
    )

    # Agent 2: JSON structurer
    summarizer = Agent(
        role='JSON Structuring Agent',
        goal='Transform a summary into a JSON that matches a strict schema',
        backstory=(
            "You specialize in structuring textual information into accurate JSON for "
            "downstream software pipelines."
        ),
        verbose=True,
        llm=llm
    )

    #agent 3:markdown agent
    markdown_formatter =Agent(
        role = "Markdown Formatter",
        goal = "Convert structured meeting summary JSON into Markdown",
        backstory=(
        "You're great at turning structured meeting information into beautiful, readable Markdown "
        "for human consumption. Your output will be used in reports and shared documentation."
    ),
    verbose=True,
    llm=llm
    )

    #  Task 1: Interpret the transcript
    interpret_task = Task(
        description=(
            "You are provided the transcript below.\n\n"
            "{transcript} \n\n"
            "Summarize the meeting into bullet points organized by the following sections:\n"
            "- Date\n- Time\n- Attendees\n- Project\n- Agenda\n"
            "- Key Discussions\n- Decisions Made\n- Action Items "
            "(with task, owner, due date)\n\n"
            "Be as clear and complete as possible, even if details are sparse."
        ),
        expected_output=(
            "A bullet-point summary of the above transcript."
        ),
        agent=interpreter
    )

    #  Task 2: Structure into JSON
    structure_task = Task(
    description=(
    "Given the summary :\n\n {{tasks.interpret_task.output}}.\n\n"
    "Your task is to convert it into a valid JSON object with the following fields:\n"
    "- date (YYYY-MM-DD)\n"
    "- time (e.g., 10:00 AM)\n"
    "- attendees (list of names)\n"
    "- project (project name)\n"
    "- agenda (list of agenda items)\n"
    "- key_discussions (list of discussion points)\n"
    "- decisions_made (list of decisions)\n"
    "- action_items (list of tasks with: task, owner, due_date in YYYY-MM-DD)\n\n"
    " Output ONLY the JSON. Do not include any extra text, explanation, or markdown.\n"
    " If any field is missing, use a placeholder or an empty list.\n"
    " Your output must start with '{' and end with '}'."
),
        
    expected_output="Respond with ONLY a valid JSON object that strictly matches the schema. "
  "DO NOT include any markdown, explanation, commentary, or extra text. "
  "Output MUST start with '{' and end with '}'.",
   
    output_class=MeetingSummary,
    agent=summarizer
    )

    markdown_task = Task(
    description=(
        "You're given a structured JSON meeting summary:\n\n {{tasks.structure_task.output}}\n\n "
        "Convert it into well-formatted Markdown using the following structure:\n\n"
        "###  Meeting Summary\n"
        "- **Date**: <date>\n"
        "- **Time**: <time>\n"
        "- **Project**: <project>\n"
        "- **Attendees**: Comma-separated list\n\n"
        "###  Agenda\n"
        "- Agenda item 1\n"
        "- Agenda item 2\n\n"
        "###  Key Discussions\n"
        "- Discussion point 1\n\n"
        "### Decisions Made\n"
        "- Decision 1\n\n"
        "###  Action Items\n"
        "| Task | Owner | Due Date |\n"
        "|------|-------|----------|\n"
        "| ...  | ...   | ...      |\n\n"
        "Use placeholders like 'TBD' if anything is missing.\n"
        "Respond ONLY with Markdown. No explanations or JSON."
    ),
    agent=markdown_formatter,
    expected_output="Markdown string of the formatted summary. No explanations.",)
    



    crew = Crew(
        agents=[interpreter,summarizer,markdown_formatter],
        tasks=[interpret_task,structure_task,markdown_task],
        process=Process.sequential,
        verbose=True
    )

    
    result = crew.kickoff(
    inputs={
        "transcript": transcript_text
    })
   
  
    return {'final_output':result}

   

