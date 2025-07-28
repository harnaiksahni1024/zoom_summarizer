
from crewai import Crew, Agent, Task, Process
from dotenv import load_dotenv
from crewai import LLM
import os

load_dotenv()
llm = LLM(
        model="openrouter/deepseek/deepseek-chat-v3-0324",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        max_tokens=2048
    )
    
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

   
    #agent 2:markdown agent
    markdown_formatter =Agent(
        role = "Markdown Formatter",
        goal = "Convert structured meeting summary into Markdown",
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


    markdown_task = Task(
    description=(
         "You're given a meeting summary:\n\n"
        "{{ tasks.interpret_task.output }}\n\n"
        "Convert it into well-formatted Markdown with relevant emojis. Use this structure:\n\n"
        "#  Meeting Summary\n"
        "- ** Date**: <date>\n"
        "- ** Time**: <time>\n"
        "- ** Project**: <project>\n"
        "- **👥 Attendees**: Comma-separated list\n\n"
        "##  Agenda\n"
        "- Item 1\n- Item 2\n\n"
        "##  Key Discussions\n"
        "- Topic 1\n- Topic 2\n\n"
        "##  Decisions Made\n"
        "- Decision 1\n- Decision 2\n\n"
        "##  Action Items\n"
        "| Task | Owner | Due Date |\n"
        "|------|-------|----------|\n"
        "| ...  | ...   | ...      |\n\n"
        "Use emojis only in section headers and metadata (Date, Time, etc.). Format for clarity and readability. Output ONLY Markdown. No explanations or extra text."
    ),
    agent=markdown_formatter,
    expected_output="A professional Markdown summary with emojis in headings and key fields. Output only Markdown.")
    



    crew = Crew(
        agents=[interpreter,markdown_formatter],
        tasks=[interpret_task,markdown_task],
        process=Process.sequential,
        verbose=True
    )

    
    result = crew.kickoff(
    inputs={
        "transcript": transcript_text
    })
   
  
    return {'final_output':result}

   


